---
tags: [backtracking, recursive]
difficulty: Medium
---

# Generate Parentheses
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

## Variants

**Missing Logic**
```python
def generateParenthesis(n: int) -> List[str]:
  def backtracking(m):
    # TODO: Base case

    past = backtracking(m-1)
    new_parens = set()
    for paren in past:
      for i in range(len(paren)):
        for j in range(i, len(paren)):
          # TODO: add logic
          new_parens.add()

    return list(new_parens)

  return backtracking(n)

```

## Tests

**Full**
```python
{
  "n": 3
}
```

```python
{
  "expected": ["(())()","(()())","()()()","((()))","()(())"]
}
```

**Smaller**
```python
{
  "n": 2
}
```

```python
{
  "expected": ["(())","()()"]
}
```