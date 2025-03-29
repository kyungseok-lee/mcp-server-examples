import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_calculator_mcp():
    # 서버 파라미터 설정
    server_params = StdioServerParameters(
        command="python",
        args=["calculator_mcp_server.py"]
    )
    
    print("MCP 계산기 서버에 연결 중...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 서버 초기화
            print("서버 초기화 중...")
            await session.initialize()
            
            # 기본 계산 테스트
            print("\n기본 계산 테스트:")
            expressions = [
                "2 + 2",
                "sqrt(16)",
                "sin(pi/2)",
                "pow(2, 3)"
            ]
            
            for expr in expressions:
                result = await session.call_tool(
                    "calculate",
                    arguments={"expression": expr}
                )
                print(f"{expr} = {result.get('result', 'Error: ' + result.get('error', 'unknown error'))}")
            
            # 방정식 해결 테스트
            print("\n방정식 테스트:")
            
            # 1차 방정식: 2x + 3 = 0
            print("\n1차 방정식 (2x + 3 = 0):")
            linear = await session.call_tool(
                "solve_equation",
                arguments={"a": 2, "b": 3}
            )
            print("해:", linear)
            
            # 2차 방정식: x² - 5x + 6 = 0
            print("\n2차 방정식 (x² - 5x + 6 = 0):")
            quadratic = await session.call_tool(
                "solve_equation",
                arguments={"a": 1, "b": -5, "c": 6}
            )
            print("해:", quadratic)
            
            # 계산 기록 조회
            print("\n계산 기록:")
            history, _ = await session.read_resource("calculator://history")
            print(history)
            
            # 프롬프트 테스트
            print("\n계산기 프롬프트:")
            basic_prompt = await session.get_prompt(
                "calculator_prompt",
                arguments={"operation": "basic"}
            )
            print("\n기본 계산기 프롬프트:")
            print(basic_prompt.messages[0].content.text)
            
            equation_prompt = await session.get_prompt(
                "calculator_prompt",
                arguments={"operation": "equation"}
            )
            print("\n방정식 계산기 프롬프트:")
            print(equation_prompt.messages[0].content.text)

if __name__ == "__main__":
    asyncio.run(test_calculator_mcp())