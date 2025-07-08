import re
import math

precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

def tokenizing(expression):
    pattern = r'(\b(?:sin|cos|tan|asin|acos|atan|sinh|cosh|tanh|log10|log|ln|\*\*)\b\([^()]*\)|\([^()]*\)!\b|\b(?:pi|e)\b|\d+\.?\d*|\+|\-|\*|\/|\^|\(|\))'
    tokens = re.findall(pattern, expression)
    return [token.strip() for token in tokens if token.strip()]

def comparator(operator, holdingStack, postfixed):
    while (holdingStack and holdingStack[-1] != "(" and precedence[operator] <= precedence.get(holdingStack[-1], 0)):
        postfixed.append(holdingStack.pop())
    holdingStack.append(operator)

def calculate_function(func, value):
    if func == 'sin':
        return math.sin(value)
    elif func == 'cos':
        return math.cos(value)
    elif func == 'tan':
        return math.tan(value)
    elif func == 'asin':
        return math.asin(value)
    elif func == 'acos':
        return math.acos(value)
    elif func == 'atan':
        return math.atan(value)
    elif func == 'sinh':
        return math.sinh(value)
    elif func == 'cosh':
        return math.cosh(value)
    elif func == 'tanh':
        return math.tanh(value)
    elif func == 'log10':
        return math.log10(value)
    elif func == 'log':
        return math.log(value)
    elif func == 'ln':
        return math.log(value)
    elif func == 'pi':
        return math.pi
    elif func == 'e':
        return math.e
    else:
        raise ValueError(f"Unknown function: {func}")

def calculator(expression):
    postfixed = []
    holdingStack = []
    solvingStack = []

    tokens = tokenizing(expression)

    if tokens and tokens[0] == "-":
        postfixed.append("-" + tokens[1])
        del tokens[:2]

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token[0].isdigit() or token in ['pi', 'e']:
            postfixed.append(token)
        elif token in precedence:
            comparator(token, holdingStack, postfixed)
        elif token == "(":
            holdingStack.append(token)
        elif token == ")":
            while holdingStack and holdingStack[-1] != "(":
                postfixed.append(holdingStack.pop())
            if holdingStack:
                holdingStack.pop()
        else:
            func = re.match(r'(\b(?:sin|cos|tan|asin|acos|atan|sinh|cosh|tanh|log10|log|ln|\*\*)\b)', token)
            if func:
                func_name = func.group(1)
                inner_expression = re.search(r'\((.*?)\)', token).group(1)
                inner_result = calculator(inner_expression)
                result = calculate_function(func_name, inner_result)
                postfixed.append(str(result)) 
        i += 1

    while holdingStack:
        postfixed.append(holdingStack.pop())

    for token in postfixed:
        if token not in precedence:
            if token.replace('.', '', 1).isdigit():
                solvingStack.append(float(token)) 
            elif token in ['pi', 'e']:
                solvingStack.append(calculate_function(token, None)) 
            else:
                solvingStack.append(token)
                
        else:
            if len(solvingStack) < 2:
                raise ValueError(f"Not enough operands for operator: {token}")
            operand2 = float(solvingStack.pop())
            operand1 = float(solvingStack.pop()) 
            
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2
            elif token == '^':
                result = operand1 ** operand2 
                
            solvingStack.append(result)

    if not solvingStack:
        raise ValueError("No result found.")
    return solvingStack.pop()


expression = "cos(2^(sin(60) + 1)) + 6"
result = calculator(expression)
print(f"Result: {result}")  