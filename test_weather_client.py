import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_weather_client():
    # 서버 파라미터 설정
    server_params = StdioServerParameters(
        command="python",
        args=["weather_mcp_server.py"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 서버 초기화
            await session.initialize()
            
            # 사용 가능한 도구 목록 조회
            tools = await session.list_tools()
            print("사용 가능한 도구:", [tool.name for tool in tools])
            
            # 날씨 도구 호출 - 서울
            seoul_weather = await session.call_tool(
                "get_current_weather",
                arguments={"city": "Seoul", "country_code": "KR"}
            )
            print("\n서울 날씨:", seoul_weather)
            
            # 날씨 리소스 읽기 - 도쿄
            tokyo_weather, _ = await session.read_resource("weather://Tokyo")
            print("\n도쿄 날씨 (리소스):", tokyo_weather)
            
            # 사용 가능한 프롬프트 목록 조회
            prompts = await session.list_prompts()
            print("\n사용 가능한 프롬프트:", [prompt.name for prompt in prompts])
            
            # 날씨 프롬프트 가져오기 - 뉴욕
            prompt = await session.get_prompt(
                "weather_prompt",
                arguments={"city": "New York", "country_code": "US"}
            )
            print("\n뉴욕 날씨 프롬프트:", prompt.messages[0].content.text)

if __name__ == "__main__":
    asyncio.run(test_weather_client())