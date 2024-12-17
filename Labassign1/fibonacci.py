# Q5) Write a Python program to generate the Fibonacci series up to a
# specified number of terms. Use a while loop and branching to
# implement the logic.

def fibonacci():
    n = int(input("Enter the number of terms: "))
    n1, n2 = 0, 1
    count = 0
    if n <= 0:
        print("Please enter a positive integer")
    elif n == 1:
        print("Fibonacci sequence up to", n, ":")
        print(n1)
    else:
        print("Fibonacci sequence:")
        while count < n:
            print(n1, end=' ')
            nth = n1 + n2
            n1 = n2
            n2 = nth
            count += 1
    print()  # For a new line after the sequence

if __name__ == "__main__":
    fibonacci()