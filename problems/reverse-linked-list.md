---
tags: [Linked List] 
difficulty: Easy
creator: porterehunley 
---

# Reverse Linked List
Return a reversed, singly linked list from the head node.

## Code

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
def reverseList(lst: List[int]) -> List[int]:
    head = list_to_linked_list(lst)

    curr = head
    prev = None
    if not curr:
        return head

    while curr.next:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp

    return linked_list_to_list(prev)
```

**Truth**
```python
def reverseList(lst: List[int]) -> List[int]:
    head = list_to_linked_list(lst)

    curr = head
    prev = None
    while curr:
        temp = curr.next
        curr.next = prev
        prev = curr
        curr = temp

    return linked_list_to_list(prev)
```

## Examples

**Example One**
```python
{
    "lst": [1, 2, 3, 4, 5]
}
```

```python
{
    "expected": [5, 4, 3, 2, 1]
}
```

**Example Two**
```python
{
    "lst": [1, 2, 3]
}
```

```python
{
    "expected": [3, 2, 1]
}
```

**Example Three**
```python
{
    "lst": []
}
```

```python
{
    "expected": []
}
```

## Tests
**Breaking Input**
```python
{
    "lst": [1,2,3,4,5]
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
    "lst": []
}
```

```json
{
    "is_breaking": false
}
```
