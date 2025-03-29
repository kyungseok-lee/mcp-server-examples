# MCP 서버 예제

이 프로젝트는 Model Context Protocol (MCP)의 기본적인 서버 구현 예제를 포함하고 있습니다.

## 설치 방법

1. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 실행 방법

서버를 시작하려면 다음 명령어를 실행하세요:

```bash
python simple_mcp_server.py
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

## 엔드포인트

- `GET /`: 서버 상태 확인
- `GET /tools`: 사용 가능한 도구 목록 조회
- `WebSocket /mcp`: MCP 프로토콜 통신을 위한 WebSocket 엔드포인트

## 기능

현재 구현된 기능:
- 기본적인 WebSocket 연결 처리
- 간단한 "echo" 도구 구현
- 도구 및 리소스 관리 기능

## 예제 사용법

WebSocket 클라이언트를 사용하여 다음과 같은 메시지를 보낼 수 있습니다:

```json
{
    "type": "tool_call",
    "id": "1234",
    "tool": {
        "name": "echo",
        "parameters": {
            "message": "안녕하세요!"
        }
    }
}
```

서버는 다음과 같이 응답합니다:

```json
{
    "type": "tool_response",
    "id": "1234",
    "result": {
        "message": "안녕하세요!"
    }
}
```