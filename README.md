
# 감정 시각화 대시보드 (Streamlit Cloud 배포용)

Google Sheets에 저장된 감정 데이터를 시각화해주는 Streamlit 앱입니다.

## 배포 방법

1. 이 레포를 GitHub에 업로드
2. [Streamlit Cloud](https://streamlit.io/cloud) 에서 New App
3. secrets 설정창에 `secrets_ready_for_streamlit.toml` 내용을 붙여넣기
4. 배포 실행

## 필요한 Secrets (Streamlit Cloud에 붙여넣기)

아래와 같은 구조로 Secrets 설정창에 입력하세요.

```toml
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----"""
client_email = "..."
...
```
