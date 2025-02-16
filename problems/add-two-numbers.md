---
tags: [tag one]
difficulty: Medium
creator: porterehunley
---

# Add Two Numbers
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.

## Code

**Input Validation**
```python
def input_validation(l1, l2):
    if len(l1) == 0:
        return "l1 must not be empty"
    if len(l2) == 0:
        return "l2 must not be empty"

    return True
```

**Auxiliary**
```python
from typing import List

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_to_linked_list(lst: List[int]) -> ListNode:
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

def linked_list_to_list(node: ListNode) -> List[int]:
    lst = []
    while node:
        lst.append(node.val)
        node = node.next
    return lst
```

**Problem**
```python
def addTwoNumbers(l1: List[int], l2: List[int]):
    l1 = list_to_linked_list(l1)
    l2 = list_to_linked_list(l2)

    dummy_head = ListNode(0)
    current = dummy_head
    carry = 0
    
    while l1 or l2:
        x = l1.val if l1 else 0
        y = l2.val if l2 else 0
        
        total = x + y + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        current = current.next
        
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    
    return linked_list_to_list(dummy_head.next)
```

**Truth**
```python
def addTwoNumbers(l1: List[int], l2: List[int]):
    l1 = list_to_linked_list(l1)
    l2 = list_to_linked_list(l2)

    dummy_head = ListNode(0)
    current = dummy_head
    carry = 0
    
    while l1 or l2 or carry:
        x = l1.val if l1 else 0
        y = l2.val if l2 else 0
        
        total = x + y + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        current = current.next
        
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    
    return linked_list_to_list(dummy_head.next)
```

## Examples
**Test One**
```python
{
    "l1": [2, 4, 3],
    "l2": [5, 6, 4]
}
```

```python
{
    "expected": [7, 0, 8]
}
```

**Test Two**
```python
{
    "l1": [0],
    "l2": [0]
}
```

```python
{
    "expected": [0]
}
```

## Tests
**Breaking Input**
```python
{
    "l1": [9,9,9,9,9,9,9],
    "l2": [9,9,9,9]
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
    "l1": [2,4,3],
    "l2": [5,6,4]
}
```

```json
{
    "is_breaking": false
}
```
