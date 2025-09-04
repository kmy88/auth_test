#!/usr/bin/env python3

import uvicorn
from config import config

if __name__ == "__main__":
    print(f"개인계정 관리 API 서버를 시작합니다...")
    print(f"주소: http://{config.API_HOST}:{config.API_PORT}")
    print("종료하려면 Ctrl+C를 누르세요.")
    
    uvicorn.run(
        "src.api.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG if hasattr(config, 'DEBUG') else False,
        log_level=config.LOG_LEVEL.lower()
    )