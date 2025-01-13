import yoursearch
import yoursort
import random

def main():
    # Get list size from user
    size = int(input("Enter the size of the list: "))
    
    # Create random list
    arr = random.sample(range(1, 100), size)
    print("\nOriginal list:", arr)
    
    # Sorting demonstrations
    print("\nSorting Demonstrations:")
    # Bubble sort in reverse order
    bubble_sorted = yoursort.bubble_sort(arr.copy(), reverse=True)
    print("Bubble Sort (reverse):", bubble_sorted)
    
    # Insertion sort with custom key function (sort by remainder when divided by 5)
    insertion_sorted = yoursort.insertion_sort(arr.copy(), key=lambda x: x % 5)
    print("Insertion Sort (by mod 5):", insertion_sorted)
    
    # Selection sort with range
    selection_sorted = yoursort.selection_sort(arr.copy(), start=1, end=4)
    print("Selection Sort (partial range):", selection_sorted)
    
    # Searching demonstrations
    print("\nSearching Demonstrations:")
    # Get key from user
    key = int(input("Enter a number to search for: "))
    
    # Linear search
    linear_result = yoursearch.linear_search(arr, key)
    print(f"Linear Search: {key} found at index {linear_result}")
    
    # Sort array for binary search
    sorted_arr = sorted(arr)
    print("Sorted array for binary search:", sorted_arr)
    
    # Binary search
    binary_result = yoursearch.binary_search(sorted_arr, key)
    print(f"Binary Search: {key} found at index {binary_result}")

if __name__ == "__main__":
    main()