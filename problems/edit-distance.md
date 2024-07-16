---
tags: [dp]
difficulty: Medium
---

# Edit Distance
Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2. You can Insert a character, Delete a character, or Replace a character

## Variants

**Missing Logic**
```python
def minDistance(word1: str, word2: str):
	m, n = len(word1), len(word2)
	dp = [list(range(n+1))]
  dp += [[r+1]+[0]*n for r in range(m)]

	for i in range(m):
		for j in range(n):
      if word1[i] == word2[j]:
        dp[i+1][j+1] = dp[i][j]
      else:
        # TODO: just one line :)

	return dp[m][n]
```

## Tests

**Inner**
```python
{
  "word1": "horse",
  "word2": "ros"
}
```

```python
{
  "expected": 3
}
```

**Total**
```python
{
  "word1": "intention",
  "word2": "execution"
}
```

```python
{
  "expected": 5
}
```
