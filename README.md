# quiz_app
# クイズアプリ（Streamlit版）

このアプリは、Excelファイルから読み込んだ問題を使ってクイズを出題するWebアプリです。  
Python + Streamlit で構成されています。

---

## 📦 必要なファイル

- `quiz_app.py` : アプリ本体
- `requirements.txt` : 必要なライブラリ一覧

---

## 💻 実行方法（ローカル環境）

### 1. 必要なライブラリをインストール

```bash
pip install -r requirements.txt

### 2. アプリを起動
そのPC内のみで動かす場合「streamlit run quiz_app.py」
同じWi-Fi内の別の端末で動かす場合「streamlit run quiz_app.py --server.address 0.0.0.0」

### （3. 別端末からアクセス）
起動後、ターミナルに以下のような表示が出ます：
　Local URL: http://localhost:8501
  Network URL: http://192.168.1.5:8501
この Network URL を共有すれば、同じネットワーク上のスマートフォンや別のPCからアクセスできます！
アクセス可能なのは同じWi-Fi / ネットワーク内の端末のみです

ファイアウォールがブロックする場合は、解除が必要です
