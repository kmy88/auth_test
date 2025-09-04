#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_window import MainWindow

if __name__ == "__main__":
    try:
        print("개인계정 관리 UI를 시작합니다...")
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"UI 실행 중 오류 발생: {e}")
        input("아무 키나 누르세요...")