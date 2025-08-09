import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


# Splay Tree Implementation
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def splay(self, root, key):
        if not root or root.key == key:
            return root

        # Key lies in left subtree
        if key < root.key:
            if not root.left:
                return root
            if key < root.left.key:
                root.left.left = self.splay(root.left.left, key)
                root = self.right_rotate(root)
            elif key > root.left.key:
                root.left.right = self.splay(root.left.right, key)
                if root.left.right:
                    root.left = self.left_rotate(root.left)
            return self.right_rotate(root) if root.left else root

        else:
            if not root.right:
                return root
            if key > root.right.key:
                root.right.right = self.splay(root.right.right, key)
                root = self.left_rotate(root)
            elif key < root.right.key:
                root.right.left = self.splay(root.right.left, key)
                if root.right.left:
                    root.right = self.right_rotate(root.right)
            return self.left_rotate(root) if root.right else root

    def search(self, key):
        self.root = self.splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if not self.root:
            self.root = SplayNode(key, value)
            return
        self.root = self.splay(self.root, key)
        if self.root.key == key:
            return  # already exists
        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node


# Fibonacci Implementations
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value
    if n <= 1:
        tree.insert(n, n)
        return n
    value = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, value)
    return value


# Benchmark
def benchmark():
    ns = list(range(0, 951, 50))
    lru_times = []
    splay_times = []

    for n in ns:
        # LRU Cache timing
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=5) / 5
        lru_times.append(lru_time)

        # Splay Tree timing
        splay_tree = SplayTree()
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=5) / 5
        splay_times.append(splay_time)

    # Print table
    print(f"{'n':<10}{'LRU Cache Time (s)':<22}{'Splay Tree Time (s)':<22}")
    print("-" * 54)
    for n, lru_t, splay_t in zip(ns, lru_times, splay_times):
        print(f"{n:<10}{lru_t:<22.8f}{splay_t:<22.8f}")

    # Plot graph
    plt.figure(figsize=(10, 6))
    plt.plot(ns, lru_times, marker='o', label="LRU Cache")
    plt.plot(ns, splay_times, marker='s', label="Splay Tree")
    plt.xlabel("n (Fibonacci index)")
    plt.ylabel("Average execution time (s)")
    plt.title("Fibonacci Computation Time: LRU Cache vs Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    benchmark()