a = input("Enter student name: ")
b = input("Enter student Roll number: ")
b = int(b)

print("Student name is: ", a)
print("Student Roll number is: ", b)

# Example 2: Taking multiple inputs and calculating average marks
print("\n--- Example 2: Student Marks ---")
name = input("Enter student name: ")
english = float(input("Enter English marks: "))
math = float(input("Enter Math marks: "))
science = float(input("Enter Science marks: "))

average = (english + math + science) / 3

print("Student name: ", name)
print("English: ", english)
print("Math: ", math)
print("Science: ", science)
print("Average marks: ", average)