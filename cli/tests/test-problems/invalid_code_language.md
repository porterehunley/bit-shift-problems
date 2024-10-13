---
header_key: header_value
---

# Sample Problem
This is a description of the sample problem.

## Code

**Problem**
```java
def add(a: int, b: int) -> int:
  return a + b
```

**Truth**
```python
def add(a: int, b: int) -> int:
  return a + b
```

## Examples

**Test1**
```python
{
    "a": 1,
    "b": 2
}
```

```python
{
    "result": 3
}
```

## Tests
**Breaking Input**
```python
{
    "a": 1,
    "b": 2
}
```

```python
{
  "is_breaking": True
}
```

**Non-Breaking Input**
```python
{
  "a": 0,
  "b": 0
}
```

```python
{
  "is_breaking": False
}
```

 