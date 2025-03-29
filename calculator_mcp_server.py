from mcp.server.fastmcp import FastMCP
from typing import Dict, List, Union
import math
import operator

# MCP 서버 인스턴스 생성
mcp = FastMCP("Calculator Service")

@mcp.resource("calculator://history")
async def get_calculation_history() -> str:
    """최근 계산 기록을 리소스로 제공합니다."""
    return "\n".join([f"{calc['expression']} = {calc['result']}" for calc in calculation_history])

# 계산 기록 저장
calculation_history: List[Dict[str, Union[str, float]]] = []

@mcp.tool()
async def calculate(expression: str) -> Dict[str, Union[str, float]]:
    """
    수학 표현식을 계산하는 도구입니다.
    
    Args:
        expression: 계산할 수학 표현식 (예: "2 + 2", "10 * 5", "sqrt(16)")
    """
    try:
        # 안전한 계산을 위해 제한된 네임스페이스 사용
        safe_dict = {
            # 기본 산술 연산자
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '**': operator.pow,
            '%': operator.mod,
            
            # 수학 함수
            'abs': abs,
            'max': max,
            'min': min,
            'pow': pow,
            'round': round,
            'sum': sum,
            'sqrt': math.sqrt,
            
            # 삼각함수
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            
            # 상수
            'pi': math.pi,
            'e': math.e,
            
            # 괄호와 숫자를 허용하기 위한 추가 설정
            '(': '(',
            ')': ')',
            '.': '.',
        }
        
        # 표현식을 파싱하여 안전하게 계산
        # 숫자와 연산자를 분리하여 처리
        tokens = []
        current_token = ''
        
        for char in expression:
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
                continue
            elif char in '+-*/%()':
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
                tokens.append(char)
            else:
                current_token += char
        if current_token:
            tokens.append(current_token)
        
        # 토큰을 평가하여 계산
        result = eval(' '.join(tokens), {"__builtins__": None}, safe_dict)
        
        # 계산 기록 저장
        calc_entry = {
            "expression": expression,
            "result": result
        }
        calculation_history.append(calc_entry)
        if len(calculation_history) > 10:  # 최근 10개 기록만 유지
            calculation_history.pop(0)
            
        return {
            "result": result,
            "expression": expression,
            "success": True
        }
    except Exception as e:
        return {
            "error": str(e),
            "expression": expression,
            "success": False
        }

@mcp.tool()
async def solve_equation(a: float, b: float, c: float = 0) -> Dict[str, Union[List[float], str, bool]]:
    """
    2차 방정식 ax² + bx + c = 0 의 해를 구하는 도구입니다.
    1차 방정식의 경우 c를 생략하면 ax + b = 0 형태로 계산됩니다.
    
    Args:
        a: x²의 계수 (2차 방정식) 또는 x의 계수 (1차 방정식)
        b: x의 계수 (2차 방정식) 또는 상수항 (1차 방정식)
        c: 상수항 (2차 방정식) - 기본값 0
    """
    try:
        if c == 0 and a != 0:  # 1차 방정식 ax + b = 0
            x = -b / a
            return {
                "equation_type": "linear",
                "solution": [x],
                "success": True
            }
        else:  # 2차 방정식 ax² + bx + c = 0
            if a == 0:
                return {
                    "error": "2차 방정식의 경우 a는 0이 될 수 없습니다",
                    "success": False
                }
            
            discriminant = b**2 - 4*a*c
            if discriminant > 0:
                x1 = (-b + math.sqrt(discriminant)) / (2*a)
                x2 = (-b - math.sqrt(discriminant)) / (2*a)
                return {
                    "equation_type": "quadratic",
                    "solution": [x1, x2],
                    "discriminant": discriminant,
                    "success": True
                }
            elif discriminant == 0:
                x = -b / (2*a)
                return {
                    "equation_type": "quadratic",
                    "solution": [x],
                    "discriminant": discriminant,
                    "success": True
                }
            else:
                return {
                    "equation_type": "quadratic",
                    "solution": [],
                    "discriminant": discriminant,
                    "message": "실근이 존재하지 않습니다",
                    "success": True
                }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

@mcp.prompt()
def calculator_prompt(operation: str) -> str:
    """
    계산기 사용을 위한 프롬프트 템플릿입니다.
    
    Args:
        operation: 수행할 연산 종류 (basic/equation)
    """
    if operation == "basic":
        return """기본 계산기를 사용합니다.
사용 가능한 연산:
- 사칙연산: +, -, *, /
- 수학 함수: sqrt(), pow(), abs(), sin(), cos(), tan()
- 상수: pi, e

예시:
- 2 + 2
- sqrt(16)
- sin(pi/2)
"""
    else:
        return """방정식 계산기를 사용합니다.
1차 방정식 (ax + b = 0) 또는 2차 방정식 (ax² + bx + c = 0) 의 해를 구합니다.

입력할 값:
- a: x²의 계수 (2차) 또는 x의 계수 (1차)
- b: x의 계수 (2차) 또는 상수항 (1차)
- c: 상수항 (2차, 선택사항)

예시:
- 2x + 3 = 0 의 경우: a=2, b=3
- x² - 5x + 6 = 0 의 경우: a=1, b=-5, c=6
"""

if __name__ == "__main__":
    mcp.run()