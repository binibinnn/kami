
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import base64

# NanumGothicCoding base64 내장
font_data = """{encoded_font}"""
font_path = "NanumGothicCoding.ttf"
with open(font_path, "wb") as f:
    f.write(base64.b64decode(font_data))

font_prop = FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# 인증
scope = ["https://www.googleapis.com/auth/spreadsheets"]
try:
    creds_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(credentials)
except Exception as e:
    st.error(f"❌ 인증 실패: {e}")
    st.stop()

# 시트 불러오기
try:
    spreadsheet = gc.open_by_key("1KhDx1GdC9y1pPXWFSQG2r9Hnn2_wziymZsfznsQQsd0")
    worksheet = spreadsheet.sheet1
    values = worksheet.get_all_values()
    headers = values[0]
    rows = values[1:]
    df = pd.DataFrame(rows, columns=headers)
except Exception as e:
    st.error(f"❌ 시트 접근 실패: {e}")
    st.stop()

# 컬럼명 정리
from_col = "이름"
to_col = "관계 인물"
score_col = "수치"
df[score_col] = pd.to_numeric(df[score_col], errors="coerce")

# 플레이어 선택
players = sorted(df[from_col].dropna().unique())
players.insert(0, "admin")
input_player = st.selectbox("당신의 이름을 선택하세요", players)
secret_input = st.text_input(f"확인 키를 입력하세요", type="password")

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

# 시각화할 데이터 필터링
if input_player == "admin":
    filtered_df = df.dropna(subset=[score_col])
    labels = [f"{f}→{t}" for f, t in zip(filtered_df[from_col], filtered_df[to_col])]
else:
    filtered_df = df[df[from_col] == input_player].dropna(subset=[score_col])
    labels = filtered_df[to_col].tolist()

filtered_df = filtered_df.sort_values(score_col)
bar_colors = ["blue" if v < 0 else "red" for v in filtered_df[score_col]]

# 그래프 출력
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(filtered_df))
ax.bar(x, filtered_df[score_col], color=bar_colors, width=0.35)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=270, ha="center", fontproperties=font_prop)
ax.axhline(0, color="gray", linestyle="--")
ax.set_ylim(-100, 100)
ax.set_title(f"{input_player}의 감정 수치", fontproperties=font_prop)
ax.set_ylabel("감정 수치", fontproperties=font_prop)
plt.tight_layout()
st.pyplot(fig)
