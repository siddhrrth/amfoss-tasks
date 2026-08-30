# Task 04 — The Pirate King's Challenge

For this task, I had to solve a set of competitive programming problems from Codeforces. I worked on each problem by finding the main pattern or observation and then implementing the solution in Python. All the solutions included below were accepted on Codeforces.

---

## 1. The 67th OEIS Problem

**Contest:** Codeforces Round 1090 (Div. 4)
**Problem:** D — The 67th OEIS Problem
**Status:** Accepted

### My Approach

For this problem, I noticed that the required values follow a simple pattern.

For every `i` from `1` to `n`, I calculate:

```text
(2 × i + 1) × (2 × i + 3)
```

I store each value in a list and print all the values after generating them.

### Code

```python
t = int(input())

for i in range(t):
    n = int(input())

    ans = []

    for i in range(1, n + 1):
        ans.append((2 * i + 1) * (2 * i + 3))

    print(*ans)
```

### Complexity

* **Time Complexity:** `O(n)` per test case
* **Space Complexity:** `O(n)` because I store the generated values in a list

---

## 2. Digit String

**Contest:** Educational Codeforces Round 190 (Rated for Div. 2)
**Problem:** B — Digit String
**Status:** Accepted
**Submission:** [Codeforces Submission](https://codeforces.com/contest/2230/submission/388849352)

### My Approach

I use two counters to find the best possible split in the string.

* `count2` keeps track of the number of `2`s that I have passed.
* `count13` keeps track of the number of `1`s and `3`s that are still remaining.

First, I count all the `1`s and `3`s in the string. Then I go through the string from left to right.

Whenever I find a `2`, I increase `count2`. Whenever I find a `1` or `3`, I decrease `count13` because I have passed that character.

At every position, I check `count2 + count13` and keep the maximum value in `best`.

Finally, I subtract the maximum number of characters I can keep from the original length:

```text
len(s) - best
```

This gives the minimum number of characters that need to be removed.

### Code

```python
import sys

t = int(sys.stdin.readline())

for i in range(t):
    s = sys.stdin.readline().strip()

    count2 = 0
    count13 = 0

    for x in s:
        if x == '1' or x == '3':
            count13 += 1

    best = count13

    for x in s:
        if x == '2':
            count2 += 1

        if x == '1' or x == '3':
            count13 -= 1

        best = max(best, count2 + count13)

    print(len(s) - best)
```

### Complexity

* **Time Complexity:** `O(|s|)` per test case
* **Space Complexity:** `O(1)` extra space

---

## 3. Another Puzzle from Papyrus

**Contest:** Codeforces Round 1106 (Div. 2)
**Problem:** A — Another Puzzle from Papyrus
**Status:** Accepted
**Submission:** [Codeforces Submission](https://codeforces.com/contest/2238/submission/388938584)

### My Approach

I check two possible ways of matching the two arrays.

First, I check the arrays in their original order. For every position, `a[i]` must be at least `b[i]`. If this is possible, I calculate the total cost by adding the difference between the two values.

After that, I sort both arrays and try the same process again. In this case, the starting cost is `c`.

If the sorted arrays can be matched successfully, I compare this cost with the first one and keep the smaller answer.

If neither method works, I print `-1`.

### Code

```python
t = int(input())

for i in range(t):
    n, c = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    possible = True
    cost = 0

    for i in range(n):
        if a[i] < b[i]:
            possible = False
            break
        cost += a[i] - b[i]

    ans = cost if possible else float('inf')

    a.sort()
    b.sort()

    possible = True
    cost = c

    for i in range(n):
        if a[i] < b[i]:
            possible = False
            break
        cost += a[i] - b[i]

    if possible:
        ans = min(ans, cost)

    if ans == float('inf'):
        print(-1)
    else:
        print(ans)
```

### Complexity

* **Time Complexity:** `O(n log n)` per test case because I sort both arrays.
* **Space Complexity:** `O(n)` for storing the arrays.

---

## 4. Duck Surplus

**Contest:** Order Capital Round 2 (Codeforces Round 1104, Div. 1 + Div. 2)
**Problem:** C — Duck Surplus
**Status:** Accepted
**Submission:** [Codeforces Submission](https://codeforces.com/contest/2237/submission/388934028)

### My Approach

I maintain a variable called `ans` while processing the values.

For every new value `a_i`, I compare it with the current value of `ans`.

* If `ans` is greater than `a_i`, I add `a_i` to `ans`.
* Otherwise, I replace `ans` with `a_i`.

I repeat this for all the values in the test case and print the final value of `ans`.

### Code

```python
import sys

def main():
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)
    t = int(next(iterator))

    for i in range(t):
        n = int(next(iterator))
        ans = 0

        for j in range(n):
            a_i = int(next(iterator))

            if ans > a_i:
                ans += a_i
            else:
                ans = a_i

        print(ans)

main()
```

### Complexity

* **Time Complexity:** `O(n)` per test case
* **Space Complexity:** `O(n)` because I store the input using `split()`

---

## 5. Good Times Good Times

**Contest:** Codeforces Round 1107 (Div. 3)
**Problem:** B — Good Times Good Times
**Status:** Accepted
**Submission:** [Codeforces Submission](https://codeforces.com/contest/2241/submission/388934934)

### My Approach

The main observation I used is that I don't need the actual value of the given number. I only need to know how many digits it has.

If the number has `n` digits, I can directly calculate the answer using:

```text
10^n + 1
```

So I read the number as a string and use `len()` to find its number of digits.

For example, if the input has 3 digits:

```text
10^3 + 1 = 1001
```

### Code

```python
t = int(input())

for i in range(t):
    n = input()

    print(10 ** len(n) + 1)
```

### Complexity

* **Time Complexity:** `O(n)` for reading the input
* **Space Complexity:** `O(n)` for storing the input string

---

## Conclusion

While solving these problems, I practiced finding patterns and observations instead of using unnecessarily complicated approaches. These problems also helped me improve my understanding of loops, arrays, strings, sorting, and basic mathematical operations in Python.

All five solutions included in this write-up were accepted on Codeforces.
