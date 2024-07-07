---
tags: [dp]
difficulty: Easy
---

# Jump Game


## Variants

**Missing Logic**
```python
def canJump(self, nums):
  m = 0
  for i, n in enumerate(nums):
    if i > m:
      return False
    m = max(m, i+n)
  return True
```

