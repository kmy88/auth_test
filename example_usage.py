#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.client.auth_client import create_client
import time

def main():
    print("=== 개인계정 관리 시스템 사용 예제 ===\n")
    
    # API 키를 환경변수나 직접 입력으로 설정
    api_key = input("API 키를 입력하세요: ")
    
    if not api_key:
        print("API 키가 필요합니다.")
        return
    
    try:
        # 클라이언트 생성
        print("\n1. 클라이언트 연결 중...")
        client = create_client(api_key)
        
        # 연결 테스트
        if client.is_connected():
            print("✓ API 서버 연결 성공")
        else:
            print("✗ API 서버 연결 실패 - API 키를 확인하세요")
            return
            
        # 계정 정보 조회 예제
        print("\n2. 계정 정보 조회 테스트")
        test_alias = input("조회할 계정 alias (없으면 'test'): ") or "test"
        
        credentials = client.get_credentials(test_alias)
        if credentials:
            print(f"✓ 계정 '{test_alias}' 정보:")
            print(f"  - Username: {credentials.username}")
            print(f"  - Password: {'*' * len(credentials.password)}")
        else:
            print(f"✗ 계정 '{test_alias}'을 찾을 수 없습니다.")
            
        # UI 자동화 시뮬레이션
        print("\n3. UI 자동화 시뮬레이션")
        if credentials:
            print("실제 UI 자동화 도구에서 사용하는 방법:")
            print("```python")
            print("from src.client.auth_client import create_client")
            print("")
            print("# 계정 정보 가져오기")
            print(f"client = create_client('{api_key[:8]}...')")
            print(f"creds = client.get_credentials('{test_alias}')")
            print("")
            print("# Selenium 예제")
            print("driver.find_element('id', 'username').send_keys(creds.username)")
            print("driver.find_element('id', 'password').send_keys(creds.password)")
            print("```")
            
        print("\n=== 사용 예제 완료 ===")
        
    except Exception as e:
        print(f"✗ 오류 발생: {e}")

def selenium_example():
    """Selenium 사용 예제 (주석 처리된 코드)"""
    print("\n=== Selenium 사용 예제 ===")
    print("""
# 필요한 패키지: pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.client.auth_client import create_client

def login_with_stored_credentials(site_alias, login_url):
    # 1. 계정 정보 가져오기
    client = create_client("your-api-key")
    credentials = client.get_credentials(site_alias)
    
    if not credentials:
        print(f"계정 '{site_alias}'을 찾을 수 없습니다.")
        return False
    
    # 2. 브라우저 시작
    driver = webdriver.Chrome()
    driver.get(login_url)
    
    # 3. 로그인 수행
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    # 평문 노출 없이 안전하게 입력
    username_field.send_keys(credentials.username)
    password_field.send_keys(credentials.password)
    
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    
    return True

# 사용법
# login_with_stored_credentials("google", "https://accounts.google.com")
    """)

if __name__ == "__main__":
    main()
    
    if input("\nSelenium 예제 코드를 보시겠습니까? (y/n): ").lower() == 'y':
        selenium_example()