
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정
if os.name == 'nt':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# 🔐 구글 인증
try:
    creds_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(creds_dict)
    gc = gspread.authorize(credentials)
except Exception as e:
    st.error(f"❌ 인증 실패: {e}")
    st.stop()

# 📊 시트 접근
try:
    spreadsheet = gc.open_by_key("1KhDx1GdC9y1pPXWFSQG2r9Hnn2_wziymZsfznsQQsd0")
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
except Exception as e:
    st.error(f"❌ 시트 접근 실패: {e}")
    st.stop()

df = pd.DataFrame(data)

# 기본 감정 시각화만 테스트
from_col = "닉네임"
to_col = "메시지"
score_col = "감정 분석 결과"

df[score_col] = pd.to_numeric(df[score_col], errors="coerce")
df = df.dropna(subset=[score_col])
df = df.sort_values(score_col)
labels = [f"{f}→{t}" for f, t in zip(df[from_col], df[to_col])]
colors = ['red' if v >= 0 else 'blue' for v in df[score_col]]

fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(df))
ax.bar(x, df[score_col], color=colors, width=0.35)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=0, ha='center')
ax.axhline(0, color='gray', linestyle='--')
ax.set_ylim(-100, 100)
ax.set_title("전체 감정 수치 (디버그 모드)")
ax.set_ylabel("감정 수치")
plt.tight_layout()
st.pyplot(fig)
