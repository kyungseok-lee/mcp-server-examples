# MCP Server Examples

이 프로젝트는 Model Context Protocol (MCP) 서버 예제들을 포함하고 있습니다. BMI 계산과 날씨 정보 조회 기능을 제공하는 MCP 서버를 구현합니다.

## 프로젝트 구조

```
mcp-server-examples/
├── .venv/              # Python 가상환경
├── server.py           # MCP 서버 구현 (BMI 계산기, 날씨 정보 조회)
└── config.json         # 서버 설정 파일
```

## 제공하는 도구들

1. **BMI 계산기**
   - 키(m)와 몸무게(kg)를 입력받아 BMI 지수를 계산
   - `calculate_bmi` 도구 사용

2. **날씨 정보 조회**
   - 도시 이름을 입력받아 해당 도시의 날씨 정보를 조회
   - `fetch_weather` 도구 사용

## 프로젝트 설정 및 실행 방법

### 1. Python 가상환경 생성

```bash
# venv 모듈을 사용하여 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# Windows의 경우:
.venv\Scripts\activate
# macOS/Linux의 경우:
source .venv/bin/activate
```

### 2. 필요한 패키지 설치

```bash
# MCP 패키지 설치 (CLI 도구 포함)
pip install "mcp[cli]"

# HTTP 클라이언트 라이브러리 설치 (날씨 API 호출용)
pip install httpx
```

### 3. 서버 실행

개발 모드로 서버를 실행하거나 Claude Desktop에 설치할 수 있습니다:

```bash
# 개발 모드로 서버 실행
mcp dev server.py

# Claude Desktop에 서버 설치
mcp install server.py
```

## 의존성 패키지

- `mcp`: Model Context Protocol 구현을 위한 핵심 패키지
- `httpx`: 비동기 HTTP 클라이언트 라이브러리 (날씨 API 호출용)

## 서버 사용 방법

서버가 실행되면 Claude Desktop에서 다음과 같은 도구들을 사용할 수 있습니다:

1. BMI 계산하기:
   - 키(미터)와 몸무게(킬로그램)를 입력하면 BMI 지수를 계산해줍니다
   - 예: 키 1.79m, 몸무게 80kg → BMI 25.0

2. 날씨 정보 조회하기:
   - 도시 이름을 입력하면 해당 도시의 현재 날씨 정보를 조회합니다
   - API를 통해 실시간 날씨 데이터를 제공합니다



