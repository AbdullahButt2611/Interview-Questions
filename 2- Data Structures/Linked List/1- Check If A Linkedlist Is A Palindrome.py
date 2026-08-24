class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

# Method to Reverse a Linked List 
# (Also an important question)        
def reverse_list(head):
    prev = None
    current = head

    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node

    return prev

def is_palindrome(head):
    if not head or not head.next:
        return True  # Empty list or single element is considered a palindrome

    # Find the middle of the linked list using slow and fast pointers
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse the second half of the linked list
    reversed_second_half = reverse_list(slow)

    # Compare the reversed second half with the first half
    while reversed_second_half:
        if head.value != reversed_second_half.value:
            return False
        head = head.next
        reversed_second_half = reversed_second_half.next

    return True

def print_list(head):
    while head:
        print(head.value, end=" ")
        head = head.next
    print()

# Example with an odd-length palindrome
odd_palindrome = ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(1)))))
print_list(odd_palindrome)
print("Is palindrome:", is_palindrome(odd_palindrome))

# Example with an even-length palindrome
even_palindrome = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))
print_list(even_palindrome)
print("Is palindrome:", is_palindrome(even_palindrome))

# Example with a non-palindrome
non_palindrome = ListNode(1, ListNode(2, ListNode(3)))
print_list(non_palindrome)
print("Is palindrome:", is_palindrome(non_palindrome))



# ========================================
# Output:
# ========================================
# 1 2 3 2 1 
# Is palindrome: True
# 1 2 2 1 
# Is palindrome: True
# 1 2 3
# Is palindrome: False
