---
tags: [recursion, backtracking] 
difficulty: Medium
creator: porterehunley
---

# Generate Parentheses
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses. n is between 1 and 7.

## Code

**Problem**
```python
def generateParenthesis(n: int) -> List[str]:
    # n is between 1 and 7
    if n == 1:
        return ["()"]

    curr_parens = generateParenthesis(n-1)
    new_parens = []
    for parens in curr_parens:
        new_parens.append('()' + parens)
        if new_parens[-1] != parens + '()':
            new_parens.append(parens+'()')
        new_parens.append('(' + parens + ')')

    return new_parens
```

**Truth**
```python
def solution_function():
    pass # Implement your working solution here
```

## Examples
**Example Title**
```python
{
    "parameter_name": "example",
    "another_parameter": 42 
}
```

**Example Two**
```python
{
    "parameter_name": "...",
    "another_parameter": 69 
}
```