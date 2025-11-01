import streamlit as st
st.set_page_config(page_title="출장비 홈", layout="wide")

st.title("🚗 출장비 자동 정산 홈")
st.write("좌측 사이드바에서 **1_정산**, **2_챗봇** 페이지로 이동하세요.")

# (Streamlit 1.28+ 이면 바로 페이지 링크도 가능)
try:
    st.page_link("pages/1_정산.py", label="📊 정산으로 이동")
    st.page_link("pages/2_챗봇.py", label="🤖 챗봇 열기")
except Exception:
    pass
