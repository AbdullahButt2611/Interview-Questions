# 25 Horses Problem
`Goldman Sachs`

## Problem

You are given **25 horses**.

Rules:

* Only **5 horses can run in one race**
* You **cannot measure time**
* You only know the **rank in each race**

Find the **top 3 fastest horses** using the **minimum number of races**.

## Solution

### Step 1: First 5 Races

Divide the horses into **5 groups of 5**.

Race them:

* Race 1 → A1 A2 A3 A4 A5
* Race 2 → B1 B2 B3 B4 B5
* Race 3 → C1 C2 C3 C4 C5
* Race 4 → D1 D2 D3 D4 D5
* Race 5 → E1 E2 E3 E4 E5

Now each group has an order:

```id="h5tc5i"
A1 > A2 > A3 > A4 > A5
B1 > B2 > B3 > B4 > B5
C1 > C2 > C3 > C4 > C5
D1 > D2 > D3 > D4 > D5
E1 > E2 > E3 > E4 > E5
```

Total races: **5**

### Step 2: Race the Winners

Race the winners of each group.

Race 6:

```id="q5ytuo"
A1 vs B1 vs C1 vs D1 vs E1
```

Example result:

```id="e409it"
A1 > B1 > C1 > D1 > E1
```

Possible horses that can still be in the top 3:

```id="a3loq6"
A1
A2
A3
B1
B2
C1
```

Total races: **6**

### Step 3: Final Race

Race the remaining horses (except A1 because it is already fastest).

Race 7:

```id="bugso3"
A2 vs A3 vs B1 vs B2 vs C1
```

The **top two horses from this race** will be the **2nd and 3rd fastest horses**.

## Result

* **1st place:** A1
* **2nd place:** Winner of Race 7
* **3rd place:** Second place of Race 7

Minimum races needed: **7**

For a **pictorial description and better understanding**, visit [Geeks for Geeks: Find the Fastest 3 Horses](https://www.geeksforgeeks.org/aptitude/puzzle-9-find-the-fastest-3-horses/).
