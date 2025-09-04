@echo off
set API_KEY=ReKXNjwXZYwgwtVhc9SBkGrHE0fdxtc2AmzF8I46MTbT2BgHoSkkbmqV8yIqe2Rn
set SERVER_URL=http://127.0.0.1:8000

echo API 키 검증 중...
curl -X POST "%SERVER_URL%/auth/validate" -H "X-API-Key: %API_KEY%"

echo.
echo 계정 목록 조회 중...
curl -X GET "%SERVER_URL%/accounts" -H "X-API-Key: %API_KEY%"

echo.
echo 특정 계정 조회 중...
set /p ALIAS=조회할 계정 별칭을 입력하세요:
curl -X GET "%SERVER_URL%/accounts/%ALIAS%" -H "X-API-Key: %API_KEY%"