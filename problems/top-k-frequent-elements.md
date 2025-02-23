---
tags: [heap] 
difficulty: Medium
creator: porterehunley
---

# Top K Frequent Elements
Given an integer array nums and an integer k, return the k most frequent elements within the array.

## Code

**Input Validation**
```python
def input_validation(nums, k):
    if len(nums) == 0 or len(nums) > 1000:
        return "nums must not be empty and must be between 1 and 1000 elements"
    if k <= 0 or k > len(nums):
        return "k must be greater than 0 and less than or equal to the length of nums"

    return True
```

**Auxiliary**
```python
from typing import List, Set
```

**Problem**
```python
def topKFrequent(nums: List[int], k: int) -> Set[int]:
    from heapq import heappop, heappush

    heap = []
    count = {}
    
    for num in nums:
        if num not in count:
            count[num] = 0
        count[num] += 1

    for (i,num) in enumerate(count):
        if (i < k):
            heappush(heap, num)
            continue

        if (count[num] > count[heap[0]]):
            heappop(heap)
            heappush(heap, num)
        
    return set(heap)
```

**Truth**
```python
def topKFrequent(nums: List[int], k: int) -> Set[int]:
    from heapq import heappop, heappush
    
    counts = {}
    for num in nums:
        if num not in counts:
            counts[num] = 0
        counts[num] += 1

    heap = []
    if k == len(nums):
        return nums
    
    target_len = k
    for num, count in counts.items():
        if len(heap) < target_len or count > heap[0][0]:
            heappush(heap, (count, num))
            if len(heap) > target_len:
                heappop(heap)

    return {x[1] for x in heap}
```

## Examples
**Example Title**
```python
{
    "nums": [1,1,1,2,2,3],
    "k": 2
}
```

```python
{
    "expected": [1,2]
}
```

**Example Two**
```python
{
    "nums": [1],
    "k": 1
}
```

```python
{
    "expected": [1]
}
```

## Tests
**Non-Breaking Input**
```python
{
    "nums": [1,1,1,2,2,3],
    "k": 2
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
    "nums": [4,1,-1,2,-1,2,3],
    "k": 2
}
```

```json
{
    "is_breaking": true
}
```