import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_calculator():
    server_params = StdioServerParameters(
        command="python",
        args=["calculator_mcp_server.py"]
    )
    
    print("계산기 서버에 연결 중...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 테스트할 수식들
            expressions = [
                "100 / 10 * 3.14",  # 기본 사칙연산
                "sqrt(16)",         # 제곱근
                "sin(pi/2)",        # 삼각함수와 파이
                "2 ** 3",          # 거듭제곱
                "10 + 5 * 2",       # 연산자 우선순위
                "(10 + 5) * 2"      # 괄호 사용
            ]
            
            print("\n=== 기본 계산 테스트 ===")
            for expr in expressions:
                try:
                    result = await session.call_tool(
                        "calculate",
                        arguments={"expression": expr}
                    )
                    if result.get("success", False):
                        print(f"{expr} = {result['result']}")
                    else:
                        print(f"오류 ({expr}): {result.get('error', '알 수 없는 오류')}")
                except Exception as e:
                    print(f"예외 발생 ({expr}): {str(e)}")
            
            print("\n=== 방정식 테스트 ===")
            equations = [
                {"a": 2, "b": -3},                    # 2x - 3 = 0
                {"a": 1, "b": -5, "c": 6},           # x² - 5x + 6 = 0
                {"a": 1, "b": 2, "c": 1},            # x² + 2x + 1 = 0
                {"a": 1, "b": 0, "c": 1}             # x² + 1 = 0
            ]
            
            for eq in equations:
                try:
                    result = await session.call_tool(
                        "solve_equation",
                        arguments=eq
                    )
                    if result.get("success", False):
                        print(f"방정식 (계수: {eq}) 해: {result['solution']}")
                        if "equation_type" in result:
                            print(f"방정식 유형: {result['equation_type']}")
                    else:
                        print(f"오류 (계수: {eq}): {result.get('error', '알 수 없는 오류')}")
                except Exception as e:
                    print(f"예외 발생 (계수: {eq}): {str(e)}")
            
            print("\n=== 계산 기록 테스트 ===")
            try:
                history, _ = await session.read_resource("calculator://history")
                print("계산 기록:")
                print(history)
            except Exception as e:
                print(f"계산 기록 조회 오류: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_calculator()) 