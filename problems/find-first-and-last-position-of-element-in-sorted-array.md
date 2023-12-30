---
tags: [binary search]
---

# Find First and Last Position of Element in Sorted-array
Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value. If target is not found in the array, return [-1, -1].

## Variants

**Debugging**
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

**Missing Logic**
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

## Tests

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