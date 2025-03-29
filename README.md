# MCP 서버 예제

이 프로젝트는 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 서버의 구현 예제를 포함하고 있습니다.

## 날씨 정보 MCP 서버

이 예제는 OpenWeatherMap API를 사용하여 날씨 정보를 제공하는 MCP 서버를 구현합니다.

### 기능

- **리소스 (Resources)**
  - `weather://{city}`: 특정 도시의 날씨 정보를 리소스로 제공

- **도구 (Tools)**
  - `get_current_weather`: 도시 이름과 국가 코드를 받아 현재 날씨 정보를 반환

- **프롬프트 (Prompts)**
  - `weather_prompt`: 날씨 정보 조회를 위한 프롬프트 템플릿 제공

### 설치 방법

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. OpenWeatherMap API 키 설정:
```bash
# .env 파일 생성
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
```

### Cursor에서 사용하기

1. `cursor-mcp-config.json` 파일을 Cursor의 MCP 설정으로 지정:
```json
{
  "mcpServers": {
    "weather-service": {
      "command": "python",
      "args": [
        "weather_mcp_server.py"
      ],
      "cwd": "/path/to/mcp-server-examples",
      "env": {
        "OPENWEATHER_API_KEY": "${OPENWEATHER_API_KEY}"
      }
    }
  }
}
```

2. 환경 변수 설정:
   - `OPENWEATHER_API_KEY` 환경 변수를 시스템에 설정하거나
   - Cursor의 환경 변수 설정에서 직접 지정

### MCP 서버 사용 예시

1. 리소스 사용:
```python
# 서울 날씨 정보 조회
weather_info = await session.read_resource("weather://Seoul")
```

2. 도구 사용:
```python
# 도쿄 날씨 정보 조회
weather_data = await session.call_tool(
    "get_current_weather",
    arguments={
        "city": "Tokyo",
        "country_code": "JP"
    }
)
```

3. 프롬프트 사용:
```python
# 뉴욕 날씨 프롬프트 생성
prompt = await session.get_prompt(
    "weather_prompt",
    arguments={
        "city": "New York",
        "country_code": "US"
    }
)
```

### 반환되는 날씨 정보

- 온도 (°C)
- 습도 (%)
- 날씨 설명
- 풍속 (m/s)

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 참고 자료

- [Model Context Protocol 문서](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OpenWeatherMap API](https://openweathermap.org/api)