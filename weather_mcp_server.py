import os
from dotenv import load_dotenv
import aiohttp
from mcp.server.fastmcp import FastMCP
from typing import Dict, Optional

load_dotenv()

# OpenWeatherMap API 설정
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
BASE_URL = "http://api.openweathermap.org/data/2.5"

# MCP 서버 인스턴스 생성
mcp = FastMCP("Weather Service")

@mcp.resource("weather://{city}")
async def get_weather_resource(city: str) -> str:
    """도시의 현재 날씨 정보를 리소스로 제공합니다."""
    async with aiohttp.ClientSession() as session:
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        async with session.get(f"{BASE_URL}/weather", params=params) as response:
            if response.status == 200:
                data = await response.json()
                return f"""
도시: {city}
온도: {data['main']['temp']}°C
습도: {data['main']['humidity']}%
날씨: {data['weather'][0]['description']}
풍속: {data['wind']['speed']} m/s
"""
            else:
                return f"날씨 정보를 가져오는데 실패했습니다. 상태 코드: {response.status}"

@mcp.tool()
async def get_current_weather(city: str, country_code: Optional[str] = None) -> Dict:
    """
    현재 날씨 정보를 조회하는 도구입니다.
    
    Args:
        city: 날씨를 조회할 도시 이름
        country_code: 국가 코드 (예: KR, US) - 선택사항
    """
    location = f"{city},{country_code}" if country_code else city
    async with aiohttp.ClientSession() as session:
        params = {
            "q": location,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        async with session.get(f"{BASE_URL}/weather", params=params) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"]
                }
            else:
                return {"error": f"날씨 정보를 가져오는데 실패했습니다. 상태 코드: {response.status}"}

@mcp.prompt()
def weather_prompt(city: str, country_code: Optional[str] = None) -> str:
    """
    날씨 정보 조회를 위한 프롬프트 템플릿입니다.
    
    Args:
        city: 날씨를 조회할 도시 이름
        country_code: 국가 코드 (예: KR, US) - 선택사항
    """
    location = f"{city}, {country_code}" if country_code else city
    return f"""다음 도시의 현재 날씨 정보를 알려주세요:
도시: {location}

다음 정보를 포함해주세요:
1. 현재 기온
2. 습도
3. 날씨 상태
4. 풍속"""

if __name__ == "__main__":
    mcp.run()