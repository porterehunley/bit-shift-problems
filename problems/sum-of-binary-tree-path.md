---
tags: [binary tree, recursive]
difficulty: Medium
---

# Sum of binary Tree Path
Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references. A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.

## Variants

**Debugging**
```python
def pathSum(root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
    def recursive(root, target):
        if root == None:
            return []

        if target == root.val:
            return [[root.val]]

        left_paths = recursive(root.left, target-root.val)
        right_paths = recursive(root.right, target-root.val)

        if len(left_paths):
            left_paths = [[root.val] + path for path in left_paths]
    
        if len(right_paths):
            right_paths = [[root.val] + path for path in right_paths]

        return left_paths + right_paths

    return recursive(root, targetSum)
```

## Tests

**Full**
```python
{
    "root": [5,4,8,11,null,13,4,7,2,null,null,5,1],
    "targetSum": 22
}
```

```python
{
    "expected": [[5,4,11,2],[5,8,4,5]]
}
```

**Small**
```python
{
  "root": [1,2,3],
  "targetSum": 5
}
```

```python
{
  "expected": []
}
```

**One Length**
```python
{
  "root": [1,2],
  "targetSum": 0
}
```

```python
{
  "expected": []
}
```

**Another One**
```python
{
  "root": [1,2],
  "targetSum": 1
}
```

```python
{
  "expected": []
}
```
