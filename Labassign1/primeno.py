# Create a program that takes user input and checks whether the
# entered number is a prime number or not. Utilize a for loop and
# branching statements.

def primeno():
    num = int(input("Enter a number: "))
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                print(num, "is not a prime number")
                break
        else:
            print(num, "is a prime number")
    else:
        print(num, "is not a prime number")

if __name__ == "__main__":
    primeno()

        