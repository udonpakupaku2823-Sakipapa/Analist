import streamlit as st
import pandas as pd

st.title("Excel検索ツール（Web版）")

df = None

# --- ファイル読み込み ---
uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx"])

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
