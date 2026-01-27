 

num1 = int(input("enter 1 num:"))
num2 =int(input("enter num2 : "))
print("\n1. +", "\n2. -", "\n3. /", "\n4. *", "\n5. %")
operation = input("enter operation:")

"""
if operation == "1":
    print("addition is :",num1 + num2)
elif operation == "2":
    print("subtraction :",num1 - num2)
elif operation == "3":
    print("division is :",num1 / num2)
elif operation == "4":
    print("multiplication is :", num1 * num2)
else:
    print("invalid operator")

"""
match operation:
    case "1":
        print("addition is :", num1 + num2)

    case "2":
        print("subtraction :", num1 - num2)

    case "3":
        print("division is :", num1 / num2)

    case "4":
        print("multiplication is :", num1 *num2)

    case "5":
        print("modulus is : ", num1 % num2)

        