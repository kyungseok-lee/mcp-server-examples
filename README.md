# MCP 계산기 서버 예제

이 프로젝트는 [Model Context Protocol (MCP)](https://modelcontextprotocol.io)을 사용하여 구현된 계산기 서버 예제입니다.

## 기능

### 리소스 (Resources)
- `calculator://history`: 최근 계산 기록을 리소스로 제공

### 도구 (Tools)
- `calculate`: 수학 표현식 계산
  - 사칙연산 (+, -, *, /)
  - 수학 함수 (sqrt, pow, abs, sin, cos, tan)
  - 수학 상수 (pi, e)
- `solve_equation`: 1차/2차 방정식 해결
  - 1차 방정식: ax + b = 0
  - 2차 방정식: ax² + bx + c = 0

### 프롬프트 (Prompts)
- `calculator_prompt`: 계산기 사용을 위한 프롬프트 템플릿
  - 기본 계산기 사용법
  - 방정식 계산기 사용법

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 서버 실행:
```bash
python calculator_mcp_server.py
```

## Cursor에서 사용하기

1. Cursor의 MCP 설정 파일 위치에 `cursor-mcp-config.json` 파일을 복사하거나 내용을 추가:
   - macOS: `~/.cursor/mcp.json`
   - Windows: `%APPDATA%\Cursor\mcp.json`
   - Linux: `~/.config/cursor/mcp.json`

2. 설정 내용:
```json
{
  "mcpServers": {
    "calculator": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "calculator_mcp_server.py",
        "--key",
        "your_key_here"
      ],
      "cwd": "/path/to/mcp-server-examples"
    }
  }
}
```

## 사용 예시

1. 기본 계산:
```python
# 2 + 2 계산
result = await session.call_tool(
    "calculate",
    arguments={"expression": "2 + 2"}
)
# 결과: {"result": 4, "expression": "2 + 2", "success": true}

# 제곱근 계산
result = await session.call_tool(
    "calculate",
    arguments={"expression": "sqrt(16)"}
)
# 결과: {"result": 4.0, "expression": "sqrt(16)", "success": true}
```

2. 방정식 해결:
```python
# 1차 방정식: 2x + 3 = 0
result = await session.call_tool(
    "solve_equation",
    arguments={"a": 2, "b": 3}
)
# 결과: {"solution": [-1.5], "equation_type": "linear", "success": true}

# 2차 방정식: x² - 5x + 6 = 0
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