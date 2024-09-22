---
tags: [tag one]
difficulty: Medium
---

# Add Two Numbers
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list. You may assume the two numbers do not contain any leading zero, except the number 0 itself.

## Code

**Auxiliary**
```python
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
    
    return dummy_head.next
```

**Truth**
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
    
    return dummy_head.next
```

## Tests
**Test Title**
```python
{
    "parameter_name": "example",
    "another_parameter": 42 
}
```

```python
{
    "expected": [3,4]
}
```

**Test Two**
```python
{
    "parameter_name": "...",
    "another_parameter": 69 
}
```

```python
{
    "expected": [3,4]
}
```