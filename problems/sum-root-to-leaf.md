---
tags: [binary tree, recursive]
difficulty: Medium
---

# Sum Root to Leaf Numbers
You are given the root of a binary tree containing digits from 0 to 9 only. Each root-to-leaf path in the tree represents a number. Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.

## Variants

**Debugging**
```python
def sumNumbers(root: Optional[TreeNode]) -> int:
    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    
    def r(root):
        if not root:
            return []

        left_nums = r(root.left)
        right_nums = r(root.right)

        if not left_nums and not right_nums:
            return [[str(root.val)]]

        for num in left_nums:
            num.append(str(root.val))

        for num in right_nums:
            num.append(str(root.val))

        return left_nums + right_nums

    nums = r(root)
    return sum([int(''.join(num)) for num in nums])
```

## Tests
```python
{
    "root": []
}
```