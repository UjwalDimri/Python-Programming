num1 = int(input("Enter First number"))
num2 = int(input("Enter Second Number"))
print(f"The Sum of {num1}&{num2}is{num1+num2}")

# Naming of variable ---
    #    - no special character alllowed except _
        #  - should not be a keyword
        # emp_sal , emp_age examples of variable
# Identify operator
    # obj1 is Obj2
        # Return True if obj1 and obj2 Share same memory location 
x = 10
y = 10
if x is y :
      print("Same Location")

else :
   print("Different Numbers")
print(r"c:\Desktop\new.txt")
    #   by using r it will print this as it is 

# Conditionals
marks = int(input("Enter your Marks"))

if (marks >= 40):
     print("Pass")
else:
     print("Fail")

# ---here indentation is very Important

# --multiple conditionals statement

num = int(input("Enter any Number"))
if num > 0:
     print("Positive")
elif num < 0:
     print("Negative")
else :
     print("Zero")
    
# LOOPS
# for and While
for i in range (1,6):
    print(i) # only till 5 it will print
for i in range(1,10,2):
     print(i)

# to Find something
str ="Python"
if 'P' in str :
    print("found")
else :
     print("P not found")

i = 1
while (i <=5) :
     print(i)
     i += 1 


# break - stops loop immediately 
# continue - Skips Current Iteration 
# pass - Does Nothing


for i in range (1,6):
     if i==3:
          continue
     print(i)

