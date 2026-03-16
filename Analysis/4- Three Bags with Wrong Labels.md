# Correctly Label 3 Wrongly Labeled Bags

## Problem

You have **3 bags**:

* One contains **only red balls** (R)
* One contains **only black balls** (B)
* One contains a **mix of red and black balls** (M)

All three bags are **labeled incorrectly**. You are allowed to **pick only one ball from one bag**.

Your task is to **correctly label all three bags in one try**.

## Solution

1. **Pick a ball from the bag labeled "Mix" (M).**

   Since the label is wrong, this bag must contain either **all red** or **all black balls**.

2. **Determine the bag contents based on the ball color picked:**

   * If the ball is **red**:

     * The bag labeled "Mix" actually contains **only red balls**.
     * The bag labeled "Red" must then be the **mixed bag**.
     * The remaining bag labeled "Black" is correct for **black balls**.

   * If the ball is **black**:

     * The bag labeled "Mix" actually contains **only black balls**.
     * The bag labeled "Black" must then be the **mixed bag**.
     * The remaining bag labeled "Red" is correct for **red balls**.

**Result:** After picking just **one ball**, all bags can be correctly labeled.
