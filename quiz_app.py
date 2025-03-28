# quiz_web_app.py (Streamlit Web化版)
import streamlit as st
import pandas as pd
import io

# 独立した状態管理用変数
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.correct_all_num = 0
    st.session_state.max_level = 11
    st.session_state.question_all_num = 0
    st.session_state.matrix = []


def read_setting(df):
    try:
        first_row_columns = df.iloc[0, :2].tolist()
        total_questions = int(first_row_columns[0])
        list_of_required = [int(num) for num in str(first_row_columns[1]).split(",")]
        list_of_required = [x - 1 for x in list_of_required]
        list_of_required.sort(reverse=True)
        return total_questions, list_of_required
    except Exception as e:
        st.error(f"エラー: {e}")
        return None, []


def extract_required_questions(selected_rows, list_of_required):
    indices = [i - 1 for i in list_of_required]
    filtered_rows = selected_rows.iloc[indices].reset_index(drop=True)
    remaining_rows = selected_rows.drop(indices).reset_index(drop=True)
    return filtered_rows, remaining_rows


def replenish_questions(output_questions, remaining_rows, num):
    random_selected = remaining_rows.sample(n=num, random_state=None)
    output_questions = pd.concat([output_questions, random_selected]).reset_index(drop=True)
    return output_questions


def read_excel_to_matrix(file):
    df = pd.read_excel(io.BytesIO(file.read()), engine="openpyxl", header=None)
    total_questions, list_of_required = read_setting(df)
    selected_rows = df.iloc[1:].reset_index(drop=True)
    output_questions, remaining_rows = extract_required_questions(selected_rows, list_of_required)
    add_num = total_questions - len(list_of_required)
    output_questions = replenish_questions(output_questions, remaining_rows, add_num)
    output_questions = output_questions.sample(frac=1, random_state=None).reset_index(drop=True)
    return output_questions.values.tolist()


def judge(user_input, correct_num, question_level):
    st.session_state.question_all_num += 1
    if user_input == correct_num:
        st.session_state.correct_all_num += 1
        if st.session_state.max_level < question_level:
            st.session_state.max_level = question_level


def display_result():
    grade = ["中学校1年生", "中学校2年生", "中学校3年生"]
    semester = ["1学期", "2学期", "3学期"]

    st.write(f"### 正解数 {st.session_state.correct_all_num} / {st.session_state.question_all_num}")

    grade_num = int(st.session_state.max_level) // 10
    semester_num = int(st.session_state.max_level) % 10

    st.write(f"あなたは **{grade[grade_num - 1]} の {semester[semester_num - 1]}** レベルです。")


# メイン
st.title("クイズアプリ")

uploaded_file = st.file_uploader("Excelファイルをアップロード", type="xlsx")

if uploaded_file and not st.session_state.matrix:
    try:
        st.session_state.matrix = read_excel_to_matrix(uploaded_file)
    except Exception as e:
        st.error(f"読み込み失敗: {e}")

if st.session_state.matrix and st.session_state.index < len(st.session_state.matrix):
    row = st.session_state.matrix[st.session_state.index]

    st.subheader(f"Q{st.session_state.index + 1}: {row[0]}")
    choice = st.radio("選択してください", options=[1, 2, 3, 4], format_func=lambda x: row[x])

    if st.button("回答"):  # 「回答」ボタン
        judge(choice, row[5], row[6])
        st.session_state.index += 1
        st.rerun()

elif st.session_state.index >= len(st.session_state.matrix):
    display_result()
    if st.button("もう一度やりなおす"):
        st.session_state.index = 0
        st.session_state.correct_all_num = 0
        st.session_state.question_all_num = 0
        st.session_state.max_level = 11
        st.session_state.matrix = []
