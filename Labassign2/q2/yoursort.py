def bubble_sort(arr, *, reverse=False):
    """Bubble sort implementation with keyword argument for reverse sorting"""
    n = len(arr)
    compare = lambda x, y: x > y if reverse else x < y
    
    for i in range(n):
        for j in range(0, n-i-1):
            if not compare(arr[j], arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr, key=lambda x: x):
    """Insertion sort implementation with optional key function"""
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key(key_item):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

def selection_sort(arr, start=0, end=None):
    """Selection sort implementation with positional arguments for range"""
    if end is None:
        end = len(arr)
        
    for i in range(start, end-1):
        min_idx = i
        for j in range(i+1, end):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr