---
tags: [recursion, backtracking] 
difficulty: Medium
creator: porterehunley
---

# Generate Parentheses
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses. n is between 1 and 7.

## Code

**Input Validation**
```python
def input_validation(n):
    if n < 1 or n > 7:
        return "n must be between 1 and 7"
    return True
```

**Auxiliary**
```python
from typing import Set
```

**Problem**
```python
def generateParenthesis(n: int) -> Set[str]:
    # n is between 1 and 7
    if n == 1:
        return {"()"}

    curr_parens = generateParenthesis(n-1)
    new_parens = []
    for p in curr_parens:
        new_parens.append('()' + p)
        if new_parens[-1] != p + '()':
            new_parens.append(p + '()')
        new_parens.append('(' + p + ')')

    return set(new_parens)
```

**Truth**
```python
def generateParenthesis(n):
    if n == 1:
        return {'()'}

    past = generateParenthesis(n-1)
    new_parens = set()
    for p in past:
        for i in range(len(p)):
            for j in range(i, len(p)):
                new_parens.add(
                    p[0:i] +
                    '(' +
                    p[i:j] +
                    ')' +
                    p[j:]
                )

    return set(new_parens)
```

## Examples
**Example One**
```python
{
    "n": 1
}
```

```python
{
    "expected": ["()"]
}
```

**Example Two**
```python
{
    "n": 3
}
```

```python
{
    "expected": ["((()))","(()())","(())()","()(())","()()()"]
}
```

## Tests
**Non-Breaking Input**
```python
{
    "n": 3
}
```

```json
{
    "is_breaking": false 
}
```

**Breaking Input**
```python
{
    "n": 4
}
```

```json
{
    "is_breaking": true 
}
```