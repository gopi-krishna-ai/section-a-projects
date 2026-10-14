"""
Curriculum Seed Data for Python & DSA Mastery Platform
Comprehensive, verified, runnable learning tracks.
"""

TOPICS_DATA = [
    # --- Python Track ---
    {
        "id": "py_intermediate",
        "track": "python",
        "level": "Level 1: Intermediate",
        "title": "Core Mechanics & Idiomatic Python",
        "description": "Comprehensions, iterables, generators, closures, args/kwargs, custom sorting, and memory references.",
        "order_index": 1,
        "icon": "Terminal",
        "prerequisites": []
    },
    {
        "id": "py_advanced",
        "track": "python",
        "level": "Level 2: Advanced",
        "title": "Python Data Model & Metaprogramming",
        "description": "Dunder methods, decorators with arguments, descriptors, MRO, concurrency, asyncio, and memory behavior.",
        "order_index": 2,
        "icon": "Cpu",
        "prerequisites": ["py_intermediate"]
    },
    {
        "id": "py_engineering",
        "track": "python",
        "level": "Level 3: Engineering",
        "title": "Production Engineering & Architecture",
        "description": "SOLID principles, dependency injection, streaming large datasets, robust validation, and profiling.",
        "order_index": 3,
        "icon": "Boxes",
        "prerequisites": ["py_advanced"]
    },

    # --- DSA Track ---
    {
        "id": "dsa_complexity",
        "track": "dsa",
        "level": "Stage 1",
        "title": "Asymptotic & Complexity Analysis",
        "description": "Big-O, Omega, Theta, loop analysis, recursion trees, and Python operation costs.",
        "order_index": 4,
        "icon": "Activity",
        "prerequisites": []
    },
    {
        "id": "dsa_arrays_strings",
        "track": "dsa",
        "level": "Stage 2",
        "title": "Arrays, Two Pointers & Sliding Window",
        "description": "Prefix sums, contiguous subarrays, two-pointer convergence, and window expansion/contraction.",
        "order_index": 5,
        "icon": "LayoutList",
        "prerequisites": ["dsa_complexity"]
    },
    {
        "id": "dsa_hashing",
        "track": "dsa",
        "level": "Stage 3",
        "title": "Hashing & Frequency Mapping",
        "description": "Hash tables, collision mechanics, fast complement lookups, and grouping anagrams.",
        "order_index": 6,
        "icon": "Hash",
        "prerequisites": ["dsa_arrays_strings"]
    },
    {
        "id": "dsa_searching_sorting",
        "track": "dsa",
        "level": "Stage 4",
        "title": "Binary Search & Sorting Invariants",
        "description": "Binary search on answers, lower/upper bounds, partitioning, and custom comparator mechanics.",
        "order_index": 7,
        "icon": "Search",
        "prerequisites": ["dsa_arrays_strings"]
    },
    {
        "id": "dsa_linked_lists",
        "track": "dsa",
        "level": "Stage 5",
        "title": "Linked Lists & Pointer Manipulation",
        "description": "Fast and slow pointer cycles, list reversal, middle discovery, and dummy node techniques.",
        "order_index": 8,
        "icon": "GitCommit",
        "prerequisites": ["dsa_arrays_strings"]
    },
    {
        "id": "dsa_stacks_queues",
        "track": "dsa",
        "level": "Stage 6",
        "title": "Stacks, Queues & Monotonic Structures",
        "description": "LIFO/FIFO invariants, balanced bracket matching, and monotonic next-greater element scans.",
        "order_index": 9,
        "icon": "Layers",
        "prerequisites": ["dsa_arrays_strings"]
    },
    {
        "id": "dsa_recursion_backtracking",
        "track": "dsa",
        "level": "Stage 7",
        "title": "Recursion Trees & Backtracking",
        "description": "State exploration, decision trees, subsets, permutations, pruning, and constraint satisfaction.",
        "order_index": 10,
        "icon": "GitFork",
        "prerequisites": ["dsa_complexity"]
    },
    {
        "id": "dsa_trees_bst",
        "track": "dsa",
        "level": "Stage 8",
        "title": "Trees, Traversals & BST Invariants",
        "description": "DFS (pre/in/post-order), BFS level-order, tree diameter, lowest common ancestor, and BST validations.",
        "order_index": 11,
        "icon": "Binary",
        "prerequisites": ["dsa_recursion_backtracking"]
    },
    {
        "id": "dsa_heaps",
        "track": "dsa",
        "level": "Stage 9",
        "title": "Heaps & Priority Queues",
        "description": "Min/max-heaps, Python heapq, Top-K elements, stream medians, and merging sorted inputs.",
        "order_index": 12,
        "icon": "BarChart",
        "prerequisites": ["dsa_trees_bst"]
    },
    {
        "id": "dsa_graphs",
        "track": "dsa",
        "level": "Stage 10",
        "title": "Graphs, BFS/DFS & Shortest Paths",
        "description": "Adjacency lists, cycle detection, topological sorting, Dijkstra, and Disjoint Set Union.",
        "order_index": 13,
        "icon": "Share2",
        "prerequisites": ["dsa_stacks_queues"]
    },
    {
        "id": "dsa_dp",
        "track": "dsa",
        "level": "Stage 11",
        "title": "Dynamic Programming & State Transitions",
        "description": "Overlapping subproblems, state transitions, memoization, tabulation, 1D/2D DP, and space optimization.",
        "order_index": 14,
        "icon": "Cpu",
        "prerequisites": ["dsa_recursion_backtracking"]
    }
]

LESSONS_DATA = [
    {
        "topic_id": "py_intermediate",
        "title": "Deep Dive: Comprehensions, Iterables & Lazy Evaluation",
        "content": """# Intermediate Python Mastery: Comprehensions, Iterators & Generators

Understanding Python beyond basic syntax requires knowing how objects are allocated, iterated, and lazily evaluated.

## 1. List, Dict & Set Comprehensions
Comprehensions are not merely syntactic sugar—they run at C-speed in CPython bytecode by bypassing repeated `list.append` attribute lookups.

```python
# List comprehension with filtering
evens = [x * 2 for x in range(10) if x % 2 == 0]

# Dict comprehension: mapping items to frequency or transformed values
word_lens = {word: len(word) for word in ["apple", "banana", "cherry"]}
```

## 2. Iterators vs. Generators
- An **Iterable** is any object that implements `__iter__()`.
- An **Iterator** is an object with `__next__()` that preserves traversal state.
- A **Generator** function uses `yield` to stream data on demand without loading entire datasets into memory.

```python
def fibonacci_stream():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

## 3. Function Closures and *args / **kwargs
A closure occurs when an inner function retains references to variables in its enclosing lexical scope even after the outer function has completed execution.
""",
        "runnable_snippets": [
            {
                "title": "Memory Comparison: List vs Generator",
                "code": """import sys

# List allocates all elements in memory immediately
list_data = [x ** 2 for x in range(10000)]

# Generator holds only execution state
gen_data = (x ** 2 for x in range(10000))

print(f"List memory size: {sys.getsizeof(list_data)} bytes")
print(f"Generator memory size: {sys.getsizeof(gen_data)} bytes")
print(f"Next 3 values from generator: {[next(gen_data) for _ in range(3)]}")
""",
                "explanation": "Generators maintain O(1) memory footprint regardless of stream size."
            },
            {
                "title": "Higher-Order Custom Sorting with Keys",
                "code": """students = [
    {"name": "Alice", "score": 88, "age": 22},
    {"name": "Bob", "score": 95, "age": 20},
    {"name": "Charlie", "score": 88, "age": 19}
]

# Primary sort by score descending (-x['score']), secondary by age ascending
students.sort(key=lambda s: (-s['score'], s['age']))
print(students)
""",
                "explanation": "Tuple-based keys allow compound multi-key sorting in O(N log N) using Timsort."
            }
        ],
        "key_takeaways": [
            "Use generator expressions when streaming large or unbounded sequences.",
            "List comprehensions are faster than manual loops with append().",
            "Tuple keys in sorting allow multi-condition priority sorting in a single pass."
        ],
        "order_index": 1
    },
    {
        "topic_id": "dsa_arrays_strings",
        "title": "Two Pointers, Sliding Window & Prefix Sum Patterns",
        "content": """# Arrays & Strings: Algorithmic Invariants

Arrays are contiguous blocks of memory. When solving array problems, the primary bottleneck is avoiding repeated O(N^2) scans.

## The Three Fundamental Patterns

### 1. Two Pointers (Inward Convergence or Fast/Slow)
- **When to use:** Sorted arrays, pair searches, palindromes, in-place partitioning.
- **Invariant:** At every step, the element pairs outside `[left, right]` have already been proven invalid, eliminating half the search space in O(1).

### 2. Sliding Window (Dynamic or Fixed Size)
- **When to use:** Finding contiguous subarrays or substrings satisfying a condition (e.g. longest substring without repeating characters, minimum window sum).
- **Invariant:** Expand `right` to satisfy the condition; contract `left` while condition is violated (or to minimize length). Each element enters and exits the window at most once -> O(N) total time.

### 3. Prefix Sums
- **When to use:** Answering multiple range-sum queries in O(1), or subarray sums equaling `K`.
- **Formula:** `Sum(arr[i...j]) = prefix[j + 1] - prefix[i]`
""",
        "runnable_snippets": [
            {
                "title": "Two Pointers: Target Pair Sum in Sorted Array",
                "code": """def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        curr_sum = nums[left] + nums[right]
        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1  # Need a larger sum
        else:
            right -= 1 # Need a smaller sum
    return []

print(two_sum_sorted([2, 7, 11, 15], 18)) # Output: [1, 2]
""",
                "explanation": "Guarantees O(N) time and O(1) auxiliary space without hash maps."
            }
        ],
        "key_takeaways": [
            "Sliding window provides O(N) total time because right advances N times and left advances at most N times.",
            "Prefix sum maps subarray sums to difference of two prefixes: P[j] - P[i] = K => P[i] = P[j] - K."
        ],
        "order_index": 1
    }
]

PROBLEMS_DATA = [
    # Problem 1: Two Sum (Hashing)
    {
        "slug": "two-sum",
        "title": "Two Sum",
        "topic_id": "dsa_hashing",
        "track": "dsa",
        "difficulty": "Easy",
        "description": """Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.""",
        "constraints": [
            "2 <= len(nums) <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ],
        "examples": [
            {
                "input": {"nums": [2, 7, 11, 15], "target": 9},
                "output": [0, 1],
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": {"nums": [3, 2, 4], "target": 6},
                "output": [1, 2],
                "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
            }
        ],
        "starter_code": """def two_sum(nums: list[int], target: int) -> list[int]:
    # Write your solution here
    pass
""",
        "reference_solution": """def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
        "brute_force_solution": """def two_sum(nums: list[int], target: int) -> list[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
""",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "hints": [
            {"level": 1, "title": "Understand the Goal", "content": "You need to find two distinct indices whose values sum to target. What is given? What is required?"},
            {"level": 2, "title": "Avoid Nested Loops", "content": "A brute force checks every pair in O(N^2). For each number x, what exact number must exist elsewhere in the array?"},
            {"level": 3, "title": "Constant-Time Lookup", "content": "Notice that for each x, the complement is (target - x). What data structure checks existence in O(1)?"},
            {"level": 4, "title": "Single Pass Design", "content": "Maintain a dictionary mapping value -> index. Check if complement is in dict before inserting the current value."},
            {"level": 5, "title": "Edge Case Handling", "content": "Ensure you don't use the same element twice (e.g. nums=[3,3], target=6). Storing index as value prevents self-matching."},
            {"level": 6, "title": "Full Solution", "content": "Iterate once with enumerate. Check `target - num in seen`. If found, return [seen[target - num], i]; else record seen[num] = i."}
        ],
        "test_cases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected_output": [0, 1], "is_hidden": False},
            {"input": {"nums": [3, 2, 4], "target": 6}, "expected_output": [1, 2], "is_hidden": False},
            {"input": {"nums": [3, 3], "target": 6}, "expected_output": [0, 1], "is_hidden": False},
            {"input": {"nums": [-1, -2, -3, -4, -5], "target": -8}, "expected_output": [2, 4], "is_hidden": True},
            {"input": {"nums": [1000000, 500, 2000000, 500], "target": 1000}, "expected_output": [1, 3], "is_hidden": True}
        ],
        "tags": ["array", "hash_table"],
        "dry_run_steps": [
            {"step": 1, "action": "Initialize seen = {}", "state": {"seen": {}}},
            {"step": 2, "action": "i=0, num=2. complement = 9 - 2 = 7. 7 in seen? False. seen[2] = 0.", "state": {"seen": {2: 0}}},
            {"step": 3, "action": "i=1, num=7. complement = 9 - 7 = 2. 2 in seen? True! Found at index 0.", "state": {"result": [0, 1]}}
        ]
    },

    # Problem 2: Maximum Subarray (Kadane's Algorithm)
    {
        "slug": "maximum-subarray",
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "topic_id": "dsa_arrays_strings",
        "track": "dsa",
        "difficulty": "Medium",
        "description": """Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

A subarray is a contiguous non-empty sequence of elements within an array.""",
        "constraints": [
            "1 <= len(nums) <= 10^5",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "examples": [
            {
                "input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]},
                "output": 6,
                "explanation": "The subarray [4, -1, 2, 1] has the largest sum 6."
            },
            {
                "input": {"nums": [1]},
                "output": 1,
                "explanation": "The subarray [1] has the largest sum 1."
            },
            {
                "input": {"nums": [5, 4, -1, 7, 8]},
                "output": 23,
                "explanation": "The subarray [5, 4, -1, 7, 8] has the largest sum 23."
            }
        ],
        "starter_code": """def max_subarray(nums: list[int]) -> int:
    # Implement Kadane's algorithm
    pass
""",
        "reference_solution": """def max_subarray(nums: list[int]) -> int:
    max_so_far = nums[0]
    current_max = nums[0]
    for num in nums[1:]:
        current_max = max(num, current_max + num)
        max_so_far = max(max_so_far, current_max)
    return max_so_far
""",
        "brute_force_solution": """def max_subarray(nums: list[int]) -> int:
    max_sum = float('-inf')
    n = len(nums)
    for i in range(n):
        curr = 0
        for j in range(i, n):
            curr += nums[j]
            if curr > max_sum:
                max_sum = curr
    return max_sum
""",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "hints": [
            {"level": 1, "title": "Contiguous Subarray Invariant", "content": "Notice that the subarray must be contiguous. If adding previous elements makes the sum worse than starting fresh, what should you do?"},
            {"level": 2, "title": "Subproblem Decision", "content": "At each index i, we have two choices: extend the existing subarray (`current_max + num`), or start a brand new subarray at `num`."},
            {"level": 3, "title": "Kadane's Relation", "content": "current_max = max(num, current_max + num). If current_max drops below num, discard the past prefix."},
            {"level": 4, "title": "Global Tracking", "content": "Maintain max_so_far initialized to nums[0] to handle arrays of all negative numbers."},
            {"level": 5, "title": "Avoid 0-init Pitfall", "content": "Do NOT initialize max_so_far to 0! If nums = [-5, -2, -8], the correct answer is -2, not 0."},
            {"level": 6, "title": "Complete Code", "content": "Initialize max_so_far = current_max = nums[0]. Loop from index 1. Update current_max and max_so_far. Return max_so_far."}
        ],
        "test_cases": [
            {"input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "expected_output": 6, "is_hidden": False},
            {"input": {"nums": [1]}, "expected_output": 1, "is_hidden": False},
            {"input": {"nums": [5, 4, -1, 7, 8]}, "expected_output": 23, "is_hidden": False},
            {"input": {"nums": [-5, -1, -8, -3]}, "expected_output": -1, "is_hidden": True},
            {"input": {"nums": [-2, -1]}, "expected_output": -1, "is_hidden": True}
        ],
        "tags": ["array", "dynamic_programming"],
        "dry_run_steps": [
            {"step": 1, "action": "nums = [-2, 1, -3, 4]. Init current_max = -2, max_so_far = -2", "state": {"curr": -2, "max": -2}},
            {"step": 2, "action": "num = 1: max(1, -2 + 1) = 1. max_so_far = max(-2, 1) = 1.", "state": {"curr": 1, "max": 1}},
            {"step": 3, "action": "num = -3: max(-3, 1 + -3) = -2. max_so_far = max(1, -2) = 1.", "state": {"curr": -2, "max": 1}},
            {"step": 4, "action": "num = 4: max(4, -2 + 4) = 4. max_so_far = max(1, 4) = 4.", "state": {"curr": 4, "max": 4}}
        ]
    },

    # Problem 3: Longest Substring Without Repeating Characters (Sliding Window)
    {
        "slug": "longest-substring-without-repeating-characters",
        "title": "Longest Substring Without Repeating Characters",
        "topic_id": "dsa_arrays_strings",
        "track": "dsa",
        "difficulty": "Medium",
        "description": """Given a string `s`, find the length of the longest substring without repeating characters.""",
        "constraints": [
            "0 <= len(s) <= 5 * 10^4",
            "s consists of English letters, digits, symbols, and spaces."
        ],
        "examples": [
            {
                "input": {"s": "abcabcbb"},
                "output": 3,
                "explanation": "The answer is 'abc', with length 3."
            },
            {
                "input": {"s": "bbbbb"},
                "output": 1,
                "explanation": "The answer is 'b', with length 1."
            },
            {
                "input": {"s": "pwwkew"},
                "output": 3,
                "explanation": "The answer is 'wke', with length 3."
            }
        ],
        "starter_code": """def length_of_longest_substring(s: str) -> int:
    # Implement sliding window
    pass
""",
        "reference_solution": """def length_of_longest_substring(s: str) -> int:
    char_map = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
""",
        "brute_force_solution": """def length_of_longest_substring(s: str) -> int:
    max_len = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            max_len = max(max_len, j - i + 1)
    return max_len
""",
        "time_complexity": "O(N)",
        "space_complexity": "O(min(N, M))",
        "hints": [
            {"level": 1, "title": "Substring Invariant", "content": "A substring is contiguous. Can you expand a window [left, right] until you hit a duplicate character?"},
            {"level": 2, "title": "Window Contraction", "content": "When a duplicate character appears at index right, where should left jump to?"},
            {"level": 3, "title": "Store Last Seen Index", "content": "Instead of removing characters one by one with a set, store each character's last seen index in a dictionary."},
            {"level": 4, "title": "Left Pointer Guard", "content": "Only update left if the duplicate was seen INSIDE the current window (`char_map[char] >= left`)."},
            {"level": 5, "title": "Window Length Formula", "content": "Length of window [left, right] is `(right - left + 1)`. Update max_len at every right advance."},
            {"level": 6, "title": "Complete Implementation", "content": "Loop with enumerate(s). If char in char_map and char_map[char] >= left: left = char_map[char] + 1. char_map[char] = right. max_len = max(max_len, right - left + 1)."}
        ],
        "test_cases": [
            {"input": {"s": "abcabcbb"}, "expected_output": 3, "is_hidden": False},
            {"input": {"s": "bbbbb"}, "expected_output": 1, "is_hidden": False},
            {"input": {"s": "pwwkew"}, "expected_output": 3, "is_hidden": False},
            {"input": {"s": ""}, "expected_output": 0, "is_hidden": True},
            {"input": {"s": " "}, "expected_output": 1, "is_hidden": True},
            {"input": {"s": "abba"}, "expected_output": 2, "is_hidden": True}
        ],
        "tags": ["sliding_window", "hash_table", "string"],
        "dry_run_steps": [
            {"step": 1, "action": "s='abba'. right=0 ('a'), left=0, seen={'a': 0}, max=1", "state": {"left": 0, "right": 0, "max": 1}},
            {"step": 2, "action": "right=1 ('b'), left=0, seen={'a': 0, 'b': 1}, max=2", "state": {"left": 0, "right": 1, "max": 2}},
            {"step": 3, "action": "right=2 ('b'), seen duplicate 'b' at 1 >= left(0). left moves to 1+1=2. seen['b']=2, max=2", "state": {"left": 2, "right": 2, "max": 2}},
            {"step": 4, "action": "right=3 ('a'), 'a' in seen at index 0. But 0 < left(2)! Do NOT pull left backward! seen['a']=3, max=2", "state": {"left": 2, "right": 3, "max": 2}}
        ]
    },

    # Problem 4: Coin Change (Dynamic Programming)
    {
        "slug": "coin-change",
        "title": "Coin Change (Fewest Coins)",
        "topic_id": "dsa_dp",
        "track": "dsa",
        "difficulty": "Medium",
        "description": """You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an infinite number of each kind of coin.""",
        "constraints": [
            "1 <= len(coins) <= 12",
            "1 <= coins[i] <= 2^31 - 1",
            "0 <= amount <= 10^4"
        ],
        "examples": [
            {
                "input": {"coins": [1, 2, 5], "amount": 11},
                "output": 3,
                "explanation": "11 = 5 + 5 + 1 (3 coins)"
            },
            {
                "input": {"coins": [2], "amount": 3},
                "output": -1,
                "explanation": "Cannot make amount 3 with only coin denomination 2."
            },
            {
                "input": {"coins": [1], "amount": 0},
                "output": 0,
                "explanation": "Amount 0 requires 0 coins."
            }
        ],
        "starter_code": """def coin_change(coins: list[int], amount: int) -> int:
    # Write dynamic programming solution
    pass
""",
        "reference_solution": """def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
""",
        "brute_force_solution": """def coin_change(coins: list[int], amount: int) -> int:
    # Exponential brute force recursion
    def helper(rem):
        if rem == 0: return 0
        if rem < 0: return float('inf')
        ans = float('inf')
        for c in coins:
            ans = min(ans, 1 + helper(rem - c))
        return ans
    res = helper(amount)
    return res if res != float('inf') else -1
""",
        "time_complexity": "O(amount * len(coins))",
        "space_complexity": "O(amount)",
        "hints": [
            {"level": 1, "title": "Subproblem Formulation", "content": "Let dp[x] be the minimum coins needed to make amount x. What is base case dp[0]?"},
            {"level": 2, "title": "Transition Equation", "content": "To make amount x using a coin c, we need 1 + dp[x - c] coins. Therefore: dp[x] = min(dp[x], dp[x - c] + 1)."},
            {"level": 3, "title": "Initialization", "content": "Initialize an array of size (amount + 1) filled with float('inf'), except dp[0] = 0."},
            {"level": 4, "title": "Loop Order", "content": "For each coin, iterate x from coin up to amount. This cleanly avoids checking negative indices."},
            {"level": 5, "title": "Unreachable Amounts", "content": "If dp[amount] is still float('inf') after filling the table, return -1."},
            {"level": 6, "title": "Implementation", "content": "dp = [float('inf')] * (amount + 1); dp[0] = 0. For c in coins: for x in range(c, amount + 1): dp[x] = min(dp[x], dp[x-c] + 1). Return dp[amount] if != inf else -1."}
        ],
        "test_cases": [
            {"input": {"coins": [1, 2, 5], "amount": 11}, "expected_output": 3, "is_hidden": False},
            {"input": {"coins": [2], "amount": 3}, "expected_output": -1, "is_hidden": False},
            {"input": {"coins": [1], "amount": 0}, "expected_output": 0, "is_hidden": False},
            {"input": {"coins": [186, 419, 83, 408], "amount": 6249}, "expected_output": 20, "is_hidden": True},
            {"input": {"coins": [2, 5, 10, 1], "amount": 27}, "expected_output": 4, "is_hidden": True}
        ],
        "tags": ["dynamic_programming"],
        "dry_run_steps": [
            {"step": 1, "action": "amount=4, coins=[1, 2]. dp = [0, inf, inf, inf, inf]", "state": {"dp": [0, "inf", "inf", "inf", "inf"]}},
            {"step": 2, "action": "Process coin=1: dp[1]=1, dp[2]=2, dp[3]=3, dp[4]=4", "state": {"dp": [0, 1, 2, 3, 4]}},
            {"step": 3, "action": "Process coin=2: dp[2]=min(2, dp[0]+1)=1; dp[3]=min(3, dp[1]+1)=2; dp[4]=min(4, dp[2]+1)=2", "state": {"dp": [0, 1, 1, 2, 2]}}
        ]
    }
]

DEBUG_EXERCISES_DATA = [
    {
        "title": "Off-by-One in Binary Search",
        "topic": "Searching & Binary Search",
        "difficulty": "Easy",
        "bug_category": "Off-by-one error",
        "description": "This binary search function fails on certain targets or causes infinite loops when elements are not present.",
        "buggy_code": """def binary_search(arr, target):
    left = 0
    right = len(arr) # BUG: Should be len(arr) - 1 or while left < right
    while left <= right: # BUG: Out of bounds index when right == len(arr)
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
        "test_cases": [
            {"input": {"arr": [1, 3, 5, 7, 9], "target": 9}, "expected_output": 4},
            {"input": {"arr": [1, 3, 5, 7, 9], "target": 10}, "expected_output": -1},
            {"input": {"arr": [2], "target": 2}, "expected_output": 0}
        ],
        "hint": "Check the initial value of right and the loop condition: if right = len(arr), arr[mid] can index out of bounds.",
        "fixed_code": """def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
        "explanation": "In 0-indexed Python arrays, the last valid index is len(arr) - 1. Initializing right to len(arr) with '<=' causes an IndexError when target > all elements."
    },
    {
        "title": "Mutable Default Argument Bug",
        "topic": "Python Functions & Scopes",
        "difficulty": "Medium",
        "bug_category": "Unexpected mutation",
        "description": "This function is supposed to append an item to a list and return it. But subsequent calls keep retaining items from previous invocations!",
        "buggy_code": """def append_item(val, items=[]): # BUG: Mutable default argument persists across calls
    items.append(val)
    return items
""",
        "test_cases": [
            {"input": {"val": 1}, "expected_output": [1]},
            {"input": {"val": 2}, "expected_output": [2]}
        ],
        "hint": "Default parameter expressions in Python are evaluated once at function definition time, NOT at every call time.",
        "fixed_code": """def append_item(val, items=None):
    if items is None:
        items = []
    items.append(val)
    return items
""",
        "explanation": "In Python, default arguments are evaluated only once when the function is defined. A mutable default like [] is shared across all function calls. Use None as sentinel."
    }
]

LOGIC_PUZZLES_DATA = [
    {
        "title": "Loop Invariant & Output Prediction",
        "category": "output_prediction",
        "statement": "What does the following snippet print?",
        "code_snippet": """x = 1
for i in range(1, 5):
    x = (x * 2) - i
print(x)
""",
        "options": ["-10", "1", "3", "-3"],
        "correct_answer": "-10",
        "explanation": "State trace: Initially x=1. i=1: x=(1*2)-1=1. i=2: x=(1*2)-2=0. i=3: x=(0*2)-3=-3. i=4: x=(-3*2)-4=-10. The output is -10.",
        "reasoning_pattern": "State transition tracing"
    },
    {
        "title": "Finding the Counterexample",
        "category": "counterexample_discovery",
        "statement": "A student claims: 'If the sum of two integers A and B is even, then A and B must both be even.' Which pair disproves this claim?",
        "code_snippet": None,
        "options": ["A = 4, B = 6", "A = 3, B = 5", "A = 2, B = 3", "A = 0, B = 8"],
        "correct_answer": "A = 3, B = 5",
        "explanation": "For A = 3 and B = 5, both are odd, yet 3 + 5 = 8 (even). This counterexample definitively disproves the universal claim.",
        "reasoning_pattern": "Counterexample discovery"
    }
]
