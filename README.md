# AVL Tree Python Implementation

A Python implementation of an **AVL Tree**, a self-balancing binary search tree that maintains height balance to ensure O(log n) time complexity for insertions, deletions, and lookups.

## Thank You's
special thanks to Sean on collaborating with me on this project :) 

## Features

- **Insertions and Deletions** with automatic rebalancing using rotations and promotions/demotions.
- **Search and Finger Search** methods optimized for ordered access.
- **Join and Split** operations between AVL trees.
- Tracks **minimum and maximum** elements in O(1).
- Converts tree to sorted array via `avl_to_array()`.

## File Structure

- `AVLTree.py` — Core implementation, including:
  - `AVLNode`: The node structure of the AVL Tree.
  - `AVLTree`: AVL tree logic, balancing, and advanced operations.

## Key Functions & Complexity

| Method                  | Complexity | Description |
|-------------------------|------------|-------------|
| `insert(key, val)`      | O(log n)   | Inserts a node and balances the tree. |
| `delete(node)`          | O(log n)   | Removes a node and rebalances the tree. |
| `search(key)`           | O(log n)   | Standard binary search. |
| `finger_search(key)`    | O(log n)   | Optimized search starting from max. |
| `join(tree2, key, val)` | O(log n)   | Joins two AVL trees. |
| `split(node)`           | O(log n)   | Splits the AVL tree into two. |
| `avl_to_array()`        | O(n)       | Converts the tree to a sorted list. |

## Advanced Design Notes

- **Real and Virtual Nodes**: Uses virtual nodes to simplify balance checking and subtree manipulation.
- **Balance Factor Tracking**: Encoded in two-digit format for efficient decision-making during rebalancing.
- **Efficient Rebalancing**: Uses single and double rotations with precise case analysis for height adjustments.

## Example Use

```python
tree = AVLTree()
tree.insert(10, "a")
tree.insert(20, "b")
tree.insert(5, "c")

node, _ = tree.search(10)
tree.delete(node)

print(tree.avl_to_array())  # [(5, 'c'), (20, 'b')]

