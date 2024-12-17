# Q2) Write a program that calculates the area of a rectangle using user-
# input length and width, and then compare it with the area of a
# square with side length half of the rectangle's width.

print("enter length of rectangle")
length = input()
print("enter breadth of rectangle")
breadth = input()
area = int(length) * int(breadth)
print("Area of rectangle is: ", area)
print("enter side of square")  
side = input()
area = int(side) * int(side)
print("Area of square is: ", area)


