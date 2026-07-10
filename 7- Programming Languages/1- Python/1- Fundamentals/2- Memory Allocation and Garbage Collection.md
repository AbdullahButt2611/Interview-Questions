# How Is Memory Allocation and Garbage Collection Handled in Python?

`Unacademy` • `Amazon` • `Google`

## Question
How does Python handle memory allocation and garbage collection?

<br><br>

## Answer

### The Big Picture
Python manages memory automatically, so you never manually allocate or free memory the way you would with `malloc` and `free` in C. Two systems work together under the hood:

- An **allocator** that hands out memory when objects are created.
- A **garbage collector** that reclaims memory when objects are no longer needed.

<br><br>

### Everything Lives in a Private Heap
- All Python objects and data structures live in a private heap managed by the interpreter.
- Your code never touches this heap directly. The Python memory manager controls it for you.
- The CPython C layer decides when to request more memory from the operating system or give it back.

<br><br>

### How Allocation Works (in CPython)
CPython allocates in layers to avoid constantly bothering the operating system, which is slow.

- **Raw layer**: memory is requested from the OS in large chunks.
- **pymalloc**: a specialized allocator that manages small objects (roughly 512 bytes or less, which is most of what a program creates). It organizes memory into a hierarchy:
  - **Arenas**: large blocks of 256 KB each.
  - **Pools**: 4 KB sections carved out of arenas.
  - **Blocks**: fixed size slots carved out of pools.
- **Large allocations**: anything bigger than pymalloc's limit bypasses it and goes straight to the system allocator.
- **Free lists**: many common types (small integers, lists, and so on) keep caches of pre-allocated slots, so creating and destroying objects repeatedly stays cheap.

<br><br>

### Garbage Collection: Two Mechanisms
Python frees memory using two cooperating strategies.

<br><br>

#### 1. Reference Counting (Primary Mechanism)
- Every object keeps a count of how many references point to it.
- The count goes up when a new reference is assigned and down when one goes away (reassignment, going out of scope, or `del`).
- The moment the count hits zero, the object is destroyed and its memory is reclaimed immediately.

```python
import sys
a = []
b = a
print(sys.getrefcount(a))  # counts a, b, and the temporary argument reference
```

The blind spot: reference counting cannot free **reference cycles**. If A refers to B and B refers back to A, their counts never reach zero even when nothing else uses them.

```python
a = {}
b = {}
a["b"] = b
b["a"] = a   # a cycle that refcounting alone would leak
```

<br><br>

#### 2. Generational Cyclic Garbage Collector (Backup)
To handle those cycles, CPython adds a second collector that periodically scans for groups of objects that reference each other but are unreachable from the rest of the program. It uses a generational design based on the idea that most objects die young.

- New objects start in **generation 0**.
- Objects that survive a collection are promoted to generation 1, then generation 2.
- Younger generations are scanned far more often than older ones, since that is where most garbage is, which keeps collection cheap.

This collector runs automatically when allocation and deallocation counts cross certain thresholds. You can control it through the built in `gc` module (inspect stats, force a pass with `gc.collect()`, tune thresholds, or disable it).

<br><br>

### Important Caveats
- **Reference counting is a CPython implementation detail**, not part of the Python language itself. Jython and IronPython rely on the JVM and .NET garbage collectors, and PyPy uses its own strategies without reference counting. Code that assumes objects are freed the instant a refcount drops is relying on CPython behavior.
- **Freed memory is not always returned to the OS right away.** Memory often stays in pymalloc's arenas ready for reuse, so a Python process can appear to hold memory even after the objects are gone.
