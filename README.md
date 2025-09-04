# 개인계정 관리 시스템

UI 자동화 도구에서 계정 정보를 안전하게 관리하고 API를 통해 제공하는 시스템입니다.

## 주요 기능

- **강력한 암호화**: Fernet(AES) 방식으로 계정 정보 암호화
- **API 인증**: 64자리 API 키 기반 보안 접근 제어  
- **사용자 친화적 UI**: Tkinter 기반 직관적인 관리 화면
- **RESTful API**: FastAPI 기반으로 UI 자동화 도구와 연동

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택사항)
```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 설정 변경
```

### 3. API 서버 실행
```bash
python run_server.py
```

### 4. 관리자 UI 실행
```bash
python run_ui.py
```

## 사용 방법

### 1. 첫 실행 시
1. `python run_ui.py`로 관리 UI 실행
2. "API 키 관리" 탭에서 새 API 키 생성
3. "계정 관리" 탭에서 계정 정보 등록

### 2. UI 자동화 도구에서 사용
```python
from src.client.auth_client import create_client

# API 키로 클라이언트 생성
client = create_client("your-api-key-here")

# 계정 정보 가져오기
credentials = client.get_credentials("myservice")
if credentials:
    print(f"Username: {credentials.username}")
    print(f"Password: {credentials.password}")
```

### 3. Selenium 예제
```python
from selenium import webdriver
from src.client.auth_client import create_client

# 계정 정보 가져오기
client = create_client("your-api-key")
creds = client.get_credentials("myservice")

# Selenium에서 사용
driver = webdriver.Chrome()
driver.find_element("id", "username").send_keys(creds.username)
driver.find_element("id", "password").send_keys(creds.password)
```

## API 엔드포인트

### 인증
- `POST /auth/validate` - API 키 검증

### 계정 관리
- `GET /accounts/{alias}` - 계정 정보 조회
- `POST /accounts` - 계정 정보 저장
- `PUT /accounts/{alias}` - 계정 정보 수정
- `DELETE /accounts/{alias}` - 계정 정보 삭제
- `GET /accounts` - 계정 목록 조회

### API 키 관리 (관리자)
- `POST /admin/api-keys` - API 키 생성
- `GET /admin/api-keys` - API 키 목록 조회
- `POST /admin/api-keys/{key_name}/activate` - API 키 활성화
- `POST /admin/api-keys/{key_name}/deactivate` - API 키 비활성화
- `DELETE /admin/api-keys/{key_name}` - API 키 삭제

## 보안 주의사항

1. **API 키 보안**: 생성된 API 키를 안전한 곳에 보관하세요
2. **암호화 키**: `encryption.key` 파일을 백업하고 안전하게 보관하세요
3. **데이터베이스**: `auth_tool.db` 파일에 대한 접근을 제한하세요
4. **네트워크**: 프로덕션 환경에서는 HTTPS 사용을 권장합니다

## 프로젝트 구조

```
auth_tool/
├── src/
│   ├── models/          # 데이터베이스 모델
│   ├── services/        # 비즈니스 로직
│   ├── api/             # FastAPI 서버
│   ├── ui/              # Tkinter UI
│   └── client/          # 클라이언트 라이브러리
├── config.py            # 설정 관리
├── run_server.py        # API 서버 실행
├── run_ui.py           # UI 실행
└── requirements.txt     # 의존성
```

## 문제 해결

### 일반적인 오류
1. **ImportError**: `pip install -r requirements.txt`로 의존성 재설치
2. **API 연결 실패**: API 서버가 실행 중인지 확인
3. **암호화 오류**: `encryption.key` 파일이 존재하는지 확인

### 개발자 정보
- Python 3.8+ 필요
- SQLite 데이터베이스 사용
- FastAPI + Tkinter 기반