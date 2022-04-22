import streamlit as st

st.title("Streamlit Test")

input_keyword = st.text_input(label="Search Keyword", value="검색 키워드를 입력해주세요")

if st.button("Search"):
  con = st.container()
  con.caption("Result")
  con.write(f"요청하신 키워드는 '{str(input_keyword)}' 입니다.")
