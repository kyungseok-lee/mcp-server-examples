from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import asyncio

app = FastAPI()

class MCPResource(BaseModel):
    id: str
    type: str
    content: Dict
    metadata: Optional[Dict] = None

class MCPTool(BaseModel):
    name: str
    description: str
    parameters: Dict

class MCPServer:
    def __init__(self):
        self.resources: Dict[str, MCPResource] = {}
        self.tools: List[MCPTool] = []
        
        # 기본 도구 등록
        self.register_tool(
            MCPTool(
                name="echo",
                description="단순히 입력받은 메시지를 반환하는 도구",
                parameters={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            )
        )

    def register_tool(self, tool: MCPTool):
        self.tools.append(tool)

    def register_resource(self, resource: MCPResource):
        self.resources[resource.id] = resource

    async def handle_message(self, message: Dict) -> Dict:
        if message.get("type") == "tool_call":
            tool_name = message.get("tool", {}).get("name")
            if tool_name == "echo":
                params = message.get("tool", {}).get("parameters", {})
                return {
                    "type": "tool_response",
                    "id": message.get("id"),
                    "result": {"message": params.get("message", "")}
                }
        return {"type": "error", "message": "지원하지 않는 메시지 타입입니다."}

mcp_server = MCPServer()

@app.websocket("/mcp")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            try:
                message_data = json.loads(message)
                response = await mcp_server.handle_message(message_data)
                await websocket.send_json(response)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "잘못된 JSON 형식입니다."
                })
    except Exception as e:
        print(f"WebSocket 에러: {str(e)}")
    finally:
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "MCP 서버가 실행 중입니다."}

@app.get("/tools")
async def get_tools():
    return {"tools": [tool.dict() for tool in mcp_server.tools]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)