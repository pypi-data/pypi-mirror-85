# Hierarchical QuadTree

This library has only one goal: insert circles of varying sizes in the plane, such that collisions can be checked very fast.
Cython package is required.

## Basic usage

```python
from hqt import HierarchicalQuadTree, Circle, Rectangle

# create a boundary: x=0, y=0, width=100, height=100
boundary = Rectangle(0, 0, 100, 100)
# define capacity, ie. max number of nodes in a quadtree
capacity = 4
# create a HierarchicalQuadTree
hqt = HierarchicalQuadTree(boundary, capacity)

# insert a Circle of radius 5 at position (45, 50)
hqt.insert(Circle(x=40, y=50, radius=5))

# return circles colliding with a given circle:
hqt.find_collisions(Circle(x=50, y=50, radius=6))
# >>> [<circle x=45.0 y=50.0 radius=5.0>]
hqt.find_collisions(Circle(x=50, y=50, radius=4))
# >>> []

# faster results: return True if given Circle collides with any item:
hqt.does_collide(Circle(x=50, y=50, radius=6))
# >>> True
hqt.does_collide(Circle(x=50, y=50, radius=4))
# >>> False
```
## How does it work?

When the first circle is inserted into the HQT, a new quadtree is created. It can only recognize circles of a similar size (radius). Circles of a similar size will be inserted into the same quadtree. This allows for more focused and more efficient querying, as the rectangle selection has a size proportional to the size of the largest circle in the quadtree. When a larger circle is inserted, one that does not fit in the previous quadtree, a new quadtree is created. This new quadtree will only record large circles of a similar size, and will then have a wider selection when querying. Hence, when querying for collisions, each quadtree returns the circles it may collide with by searching its space with an adapted rectangle selection, thus allowing for fast and efficient search.

## Authors

Maixent Chenebaux