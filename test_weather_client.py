import asyncio
import websockets
import json

async def test_weather_server():
    uri = "ws://localhost:8001/mcp"
    async with websockets.connect(uri) as websocket:
        # 서울 날씨 조회
        message = {
            "type": "tool_call",
            "id": "test-1",
            "tool": {
                "name": "get_current_weather",
                "parameters": {
                    "city": "Seoul",
                    "country_code": "KR"
                }
            }
        }
        
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print("서울 날씨:", json.loads(response))
        
        # 도쿄 날씨 조회
        message["id"] = "test-2"
        message["tool"]["parameters"] = {
            "city": "Tokyo",
            "country_code": "JP"
        }
        
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print("도쿄 날씨:", json.loads(response))

if __name__ == "__main__":
    asyncio.run(test_weather_server())