def linear_search(arr, key):
    """Linear search implementation using lambda function"""
    search = lambda arr, key, i: i if i < len(arr) and arr[i] == key else -1
    for i in range(len(arr)):
        result = search(arr, key, i)
        if result != -1:
            return result
    return -1

def binary_search(arr, key, *, left=None, right=None):
    """Binary search implementation with default arguments"""
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
        
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
    return -1