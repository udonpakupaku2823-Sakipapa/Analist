import streamlit as st
import pandas as pd

st.title("Excel検索ツール（Web版）")

df = None

# --- ファイル読み込み ---
uploaded_file = st.file_uploader("umaData.xlsx", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Excelファイルを読み込みました。")
        st.dataframe(df)
    except Exception as e:
        st.error(f"読み込みに失敗しました：{e}")

# --- 検索 ---
keyword = st.text_input("検索キーワード")

if st.button("検索"):
    if df is None:
        st.warning("先に Excel ファイルを読み込んでください。")
    else:
        result = df[df.apply(
            lambda row: row.astype(str).str.contains(keyword, case=False).any(),
            axis=1
        )]

        st.write(f"検索結果：{len(result)} 件")
        st.dataframe(result)



from google.cloud import firestore
import datetime

db = firestore.Client()

st.title("レース観戦チャット")

# メッセージ入力
user = st.text_input("名前")
text = st.text_input("メッセージ")

if st.button("送信"):
    db.collection("chat").add({
        "user": user,
        "text": text,
        "time": datetime.datetime.now()
    })

# メッセージ表示
st.subheader("チャットログ")
messages = db.collection("chat").order_by("time").stream()

for m in messages:
    msg = m.to_dict()
    st.write(f"{msg['time'].strftime('%H:%M:%S')} {msg['user']}：{msg['text']}")
