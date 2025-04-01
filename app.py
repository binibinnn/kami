
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정
try:
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = 'NanumGothic'
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'  # fallback
except:
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# 구글 인증 (스코프 최소화)
scope = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    creds_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(credentials)
except Exception as e:
    st.error(f"❌ 인증 실패: {e}")
    st.stop()

# 시트 접근
try:
    spreadsheet = gc.open_by_key("1KhDx1GdC9y1pPXWFSQG2r9Hnn2_wziymZsfznsQQsd0")
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
except Exception as e:
    st.error(f"❌ 시트 접근 실패: {e}")
    st.stop()

df = pd.DataFrame(data)

# 컬럼명 설정
from_col = "닉네임"
to_col = "메시지"
score_col = "감정 분석 결과"
df[score_col] = pd.to_numeric(df[score_col], errors="coerce")

# 플레이어 선택 및 비밀번호 입력
players = sorted(df[from_col].dropna().unique())
players.insert(0, "admin")
input_player = st.selectbox("당신의 이름을 선택하세요", players)
secret_input = st.text_input(f"{input_player}의 확인 키를 입력하세요", type="password")

secret_keys = {
    "레드": "red123",
    "블루": "blue123",
    "그린": "green123",
    "옐로우": "yellow123",
    "admin": "admin123"
}

if input_player not in secret_keys or secret_input != secret_keys[input_player]:
    st.warning("🔒 인증 키가 일치하지 않습니다.")
    st.stop()

# 본인 감정만 필터링
if input_player == "admin":
    filtered_df = df.dropna(subset=[score_col])
    labels = [f"{f}→{t}" for f, t in zip(filtered_df[from_col], filtered_df[to_col])]
else:
    filtered_df = df[df[from_col] == input_player].dropna(subset=[score_col])
    labels = filtered_df[to_col].tolist()

filtered_df = filtered_df.sort_values(score_col)
bar_colors = ['blue' if val < 0 else 'red' for val in filtered_df[score_col]]

# 시각화
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(filtered_df))
ax.bar(x, filtered_df[score_col], color=bar_colors, width=0.35)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90, ha='center')
ax.axhline(0, color='gray', linestyle='--')
ax.set_ylim(-100, 100)
ax.set_title(f"{input_player}의 감정 수치")
ax.set_ylabel("감정 수치")
plt.tight_layout()
st.pyplot(fig)
