# MCP 서버 예제

이 프로젝트는 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 서버의 구현 예제를 포함하고 있습니다.

## 계산기 MCP 서버

이 예제는 수학 계산과 방정식 해결을 제공하는 MCP 서버를 구현합니다.

### 기능

- **리소스 (Resources)**
  - `calculator://history`: 최근 계산 기록을 리소스로 제공

- **도구 (Tools)**
  - `calculate`: 수학 표현식 계산
    - 사칙연산
    - 수학 함수 (sqrt, pow, abs, sin, cos, tan)
    - 수학 상수 (pi, e)
  - `solve_equation`: 1차/2차 방정식 해결
    - 1차 방정식: ax + b = 0
    - 2차 방정식: ax² + bx + c = 0

- **프롬프트 (Prompts)**
  - `calculator_prompt`: 계산기 사용을 위한 프롬프트 템플릿
    - 기본 계산기 사용법
    - 방정식 계산기 사용법

### 설치 방법

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

### 실행 방법

1. 서버 실행:
```bash
python calculator_mcp_server.py
```

2. 테스트 실행:
```bash
python test_calculator.py
```

### Cursor에서 사용하기

`cursor-mcp-config.json` 파일을 Cursor의 MCP 설정으로 지정:
```json
{
  "mcpServers": {
    "calculator-service": {
      "command": "python",
      "args": [
        "calculator_mcp_server.py"
      ],
      "cwd": "/path/to/mcp-server-examples"
    }
  }
}
```

### 사용 예시

1. 기본 계산:
```python
result = await session.call_tool(
    "calculate",
    arguments={"expression": "2 + 2"}
)
# 결과: {"result": 4, "expression": "2 + 2", "success": true}
```

2. 방정식 해결:
```python
result = await session.call_tool(
    "solve_equation",
    arguments={"a": 1, "b": -5, "c": 6}
)
# 결과: {"solution": [3, 2], "equation_type": "quadratic", "success": true}
```

3. 계산 기록 조회:
```python
history, _ = await session.read_resource("calculator://history")
```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 참고 자료

- [Model Context Protocol 문서](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)