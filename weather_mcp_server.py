from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# OpenWeatherMap API 키 설정
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
BASE_URL = "http://api.openweathermap.org/data/2.5"

class MCPTool(BaseModel):
    name: str
    description: str
    parameters: Dict

class WeatherMCPServer:
    def __init__(self):
        self.tools: List[MCPTool] = []
        
        # 날씨 조회 도구 등록
        self.register_tool(
            MCPTool(
                name="get_current_weather",
                description="도시 이름으로 현재 날씨 정보를 조회합니다",
                parameters={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "날씨를 조회할 도시 이름"},
                        "country_code": {"type": "string", "description": "국가 코드 (예: KR, US)"}
                    },
                    "required": ["city"]
                }
            )
        )

    def register_tool(self, tool: MCPTool):
        self.tools.append(tool)

    async def get_weather(self, city: str, country_code: str = None) -> Dict:
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
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "description": data["weather"][0]["description"],
                        "wind_speed": data["wind"]["speed"]
                    }
                else:
                    return {"error": "날씨 정보를 가져오는데 실패했습니다"}

    async def handle_message(self, message: Dict) -> Dict:
        if message.get("type") == "tool_call":
            tool_name = message.get("tool", {}).get("name")
            if tool_name == "get_current_weather":
                params = message.get("tool", {}).get("parameters", {})
                city = params.get("city")
                country_code = params.get("country_code")
                
                if not city:
                    return {
                        "type": "error",
                        "message": "도시 이름이 필요합니다"
                    }
                
                weather_data = await self.get_weather(city, country_code)
                return {
                    "type": "tool_response",
                    "id": message.get("id"),
                    "result": weather_data
                }
        return {"type": "error", "message": "지원하지 않는 메시지 타입입니다"}

weather_server = WeatherMCPServer()

@app.websocket("/mcp")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            try:
                message_data = json.loads(message)
                response = await weather_server.handle_message(message_data)
                await websocket.send_json(response)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "잘못된 JSON 형식입니다"
                })
    except Exception as e:
        print(f"WebSocket 에러: {str(e)}")
    finally:
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "날씨 MCP 서버가 실행 중입니다"}

@app.get("/tools")
async def get_tools():
    return {"tools": [tool.dict() for tool in weather_server.tools]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)