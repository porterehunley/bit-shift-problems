---
tags: [binary search]
difficulty: Medium
---

# Find First and Last Position of Element in Sorted Array
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references. A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.

## Code

**Auxiliary**
```python
from typing import List
```

**Problem**
```python
def searchRange(nums: List[int], target: int) -> List[int]:
    start, end = 0, len(nums)-1
    while start < end:
        mid = start +(end-start)//2
        if nums[mid] <= target:
            start = mid + 1
        else:
            end = mid

    idx0 = start - 1
    start, end = 0, len(nums)-1
    while start < end:
        mid = start + (end-start+1)//2
        if nums[mid] < target:
            start = mid
        else:
            end = mid-1

    idx1 = end + 1
    if idx1 >=len(nums) or nums[idx1] != target:
        return [-1,-1]

    return [idx1, idx0]
```

**Truth**
```python
def searchRange_truth(nums: List[int], target: int) -> List[int]:
    start = 0
    end = len(nums) - 1
    while (start < end):
        mid = start + (end-start) // 2
        if nums[mid] < target:
            start = mid + 1

        if nums[mid] >= target:
            end = mid

    if not nums or nums[start] != target:
        return [-1, -1]

    first = start

    start = 0
    end = len(nums) - 1
    while (start < end):
        mid = start + (end-start) // 2
        if nums[mid] <= target:
            start = mid + 1

        if nums[mid] > target:
            end = mid

    last = start - 1 if nums[start] != target else start

    return [first, last]
```

## Examples

**Double**
```python
{
    "nums": [5,7,7,8,8,10],
    "target": 8
}
```

```python
{
    "expected": [3,4]
}
```

**Not Present**
```python
{
    "nums": [5,7,7,8,8,10],
    "target": 6
}
```

```python
{
    "expected": [-1,-1]
}
```

**Empty**
```python
{
    "nums": [],
    "target": 6
}
```

```python
{
    "expected": [-1,-1]
}
```

**All**
```python
{
    "nums": [6,6,6,6,6],
    "target": 6
}
```

```python
{
    "expected": [0,4]
}
```

## Tests
**Breaking Input**
```python
{
    "nums": [1],
    "target": 1
}
```

```json
{
    "is_breaking": true 
}
```

**Non-Breaking Input**
```python
{
    "nums": [1,2,3,4,5,6,7,8,9,10],
    "target": 21
}
```

```json
{
    "is_breaking": false 
}
```