
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.title("📑 구글 시트 탭별 데이터 확인")

# 인증
scope = ["https://www.googleapis.com/auth/spreadsheets"]
try:
    creds_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(credentials)
except Exception as e:
    st.error(f"❌ 인증 실패: {e}")
    st.stop()

# 전체 탭 이름 가져오기 + 선택
try:
    spreadsheet = gc.open_by_key("1KhDx1GdC9y1pPXWFSQG2r9Hnn2_wziymZsfznsQQsd0")
    worksheets = spreadsheet.worksheets()
    tab_names = [ws.title for ws in worksheets]
    selected_tab = st.selectbox("탭을 선택하세요", tab_names)
    worksheet = spreadsheet.worksheet(selected_tab)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    st.success(f"✅ '{selected_tab}' 시트 데이터")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ 시트 탭 불러오기 실패: {e}")
