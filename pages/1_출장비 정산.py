import streamlit as st
import pandas as pd
from io import BytesIO
from jungsan import summarize_trip_monthly  # 루트의 jungsan.py 사용

st.set_page_config(page_title="1) 정산", layout="wide")
st.title("1️⃣ 출장비 월별 자동 정산")

uploaded_file = st.file_uploader("📁 엑셀 (.xlsx) 업로드", type=["xlsx"])

def _month_key(m: str) -> int:
    try:
        return int(str(m).replace("월", "").strip())
    except:
        return 999

def _sum_total_amount(df_month: pd.DataFrame) -> int:
    s = df_month['총지급액']
    if pd.api.types.is_numeric_dtype(s):
        return int(s.sum())
    vals = pd.to_numeric(s.astype(str).str.replace(",", ""), errors="coerce").fillna(0)
    return int(vals.sum())

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=1)
    with st.spinner("🔍 정산 중..."):
        results = summarize_trip_monthly(df)
        st.session_state["results"] = results

    if not results:
        st.warning("❌ 분석 결과가 없습니다.")
        st.stop()

    sorted_keys = sorted(results.keys(), key=_month_key)

    # 다운로드
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as w:
        for m in sorted_keys:
            save_df = results[m].copy()
            if pd.api.types.is_numeric_dtype(save_df['총지급액']):
                save_df['총지급액'] = save_df['총지급액'].map('{:,}'.format)
            save_df.to_excel(w, sheet_name=m, index=False)
    output.seek(0)
    st.download_button("📥 월별 결과 엑셀 다운로드", output,
                       file_name="출장비_요약결과_월별.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # 탭 표시
    st.markdown("## 📊 월별 정산 상세")
    tabs = st.tabs(sorted_keys)
    for tab, m in zip(tabs, sorted_keys):
        with tab:
            df_m = results[m].copy()
            df_m.insert(0, "No.", range(1, len(df_m)+1))
            total_amt = _sum_total_amount(df_m)
            st.subheader(f"{m} (총 지급액: {total_amt:,.0f}원)")

            show_df = df_m.copy()
            if pd.api.types.is_numeric_dtype(show_df['총지급액']):
                show_df['총지급액'] = show_df['총지급액'].map('{:,}'.format)
            st.dataframe(show_df, use_container_width=True)
else:
    st.info("위에 엑셀 파일을 업로드하면 자동 분석됩니다.")
