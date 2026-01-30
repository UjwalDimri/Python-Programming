# Experiment 2: Conditional Statements

# Question 1
# Check whether the given number is divisible by 3 and 5 both.
a = 15 
if ((a%3==0) and (a%5==0)):
    print("Yes the given number is divisible by 3 and 5 both.")
# Question -2
# Check whether a given number is multiple of five or not.
a = 10
if (a%5==0):
    print("Its a Multiple Of Five")
else:
    print("It is not a Multiple Of FIve")
# Question -3 
# Find the greatest among the two numbers. 
# If numbers are equal than print “numbers are equal”
a = 10 
b = 9
if (a>b):
    print(f"{a} is greater than{b}")
elif (b>a):
    print(f"{b} is greater than {a}")
else:
    print("Both Are Equal")

# Question - 4 
# Find the greatest among three numbers assuming no two values are same.
a = 10
b = 19
c = 25
if ((a>b)and(a>c)):
    print(f"{a} is greatest ")
elif ((b>a)and(b>c)):
      print(f"{b} is greatest ")
elif ((c>a)and(c>b)):
    print(f"{c} is greatest")
else:
    print("Error")
# Question - 5
# Check whether the quadratic equation has real roots or imaginary roots.
b=int(input("input the coeff of x: "))
a=int(input("input the coeff of x^2: "))
c=int(input("input the coeff of c: "))
d=(b*b)-(4*(a*c))
if(d>0):
       print("the equation has real roots")
elif(d==0):
       print("the equation has two equal roots")
else:
       print("the equation has imaginary roots")
# #  Display the roots 


# Question-6
# Find whether a given year is a leap year or not.
year = int(input("Enter any Year to check its a leap year or not"))
if (year%400==0) or ((year%4==0)and(year%100!=0)):
    print(f"{year} - a Leap year")
else:
    print(f"{year} not a leap year")

# # Question 7
# # 7.Write a program which takes any date as input and display next date of the calendar
# # e.g.
# # I/P: day=20 month=9 year=2005 
# # O/P: day=21 month=9 year 2005
day = int(input("Enter any Day"))
month = int(input("Enter any Month"))
year = int(input("Enter any Year"))


if(month==2):
  if((year%400==0) or ((year%4==0)and(year%100!=0))):
     if (day>=1)and(day<29):
         day=day+1
         print(f"day={day} month={month} year={year}")
     elif (day==29):
         day = 1
         month=month+1
         print(f"day={day} month={month} year={year}")
     print(f"nextday:{day},nextmonth")
  else:
      if(day>=1)and(day<28):
          day=day+1
      elif(day==28):
          day = 1
elif(month==12):
    if (day>=1)and(day<31):
        day=day+1
        print(f"day={day} month={month} year={year}")
    elif (day==31):
        day = 1
        month = 1
        year = year+1
        print(f"day={day} month={month} year={year}")
    else:
        print("Enter a vaild input")
elif(month==1 or month==3 or month==5 or month==7 or month==8 or month==10):
     if (day>=1)and(day<31):
        day=day+1
        print(f"day={day} month={month} year={year}")
     elif (day==31):
        day = 1
        month = 1
        print(f"day={day} month={month} year={year}")
     else:
        print("Enter a vaild input")
         
elif(month==4 or month==6 or month==9 or month==11):
     if (day>=1)and(day<30):
        day=day+1
        print(f"day={day} month={month} year={year}")
     elif (day==30):
        day = 1
        month = 1
        print(f"day={day} month={month} year={year}")
     else:
        print("Enter a vaild input")
         
else:
    print("Enter a valid input")

# 8.Print the grade sheet of a student for the given range of cgpa. Scan marks of five subjects and calculate the percentage.
# CGPA=percentage/10
# CGPA range:
# 0 to 3.4 -> F
# 3.5 to 5.0->C+
# 5.1 to 6->B
# 6.1 to 7-> B+
# 7.1 to 8-> A
# 8.1 to 9->A+
# 9.1 to 10-> O (Outstanding)
# Sample Gradesheet
# Name: Rohit Sharma
# Roll Number: R17234512			SAPID: 50005673
# Sem: 1						Course: B.Tech. CSE AI&ML

# Subject name: Marks
# PDS: 		70
# Python: 	80
# Chemistry: 	90
# English: 	60
# Physics: 	50
# Percentage: 70%
# CGPA:7.0
# Grade:  
Name=input("Enter Your Name:")
roll_Number=int(input("Enter Your Roll NUmber"))
Sem=int(input("Enter Your Semester"))
sapid=int(input("Enter Your Sap ID:"))
course=input("Enter Your Course")
sub1 = int(input("Enter your Subject 1 marks"))
sub2 = int(input("Enter your Subject 2 marks"))
sub3 = int(input("Enter your Subject 3 marks"))
sub4= int(input("Enter your subject 4 marks"))
sub5 = int(input("Enter your Subject 5 Marks"))
percentage = ((sub1+sub2+sub3+sub4+sub5)//5)
cgpa = percentage//10
grade='F'
if((cgpa>=0) and (cgpa<=3.4)): # 0 to 3.4 -> F
    grade='F'
elif((cgpa>=3.5)and(cgpa<=5.0)):   # 3.5 to 5.0->C+
    grade='C+'
elif((cgpa>=5.1)and(cgpa<=6.0)):#5.1 to 6.0
    grade='B'
elif((cgpa>6.1)and(cgpa<=7)):# 6.1 to 7-> B+
    grade='B+'
elif((cgpa>7.1)and(cgpa<=8)):# 7.1 to 8-> A
    grade='A'
elif((cgpa>8.1))and(cgpa<=9):# 8.1 to 9->A+
    grade='A+'
elif((cgpa>9.1)and(cgpa<=10)):# 9.1 to 10-> O (Outstanding)
    grade='O'
else:
    print("Error")
print("grade Sheet")
print(f'''Name: {Name}
Roll Number: R17234512			SAPID: {sapid}
Sem: {Sem}						Course: {course}

Subject name: Marks
PDS: 		{sub1}
Python: 	{sub2}
Chemistry: 	{sub3}
English: 	{sub4}
Physics: 	{sub5}
Percentage: {percentage}
CGPA:{cgpa}
Grade:{grade} ''')

