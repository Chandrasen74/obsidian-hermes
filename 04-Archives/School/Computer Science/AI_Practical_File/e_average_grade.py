m1=float(input("Enter marks in subject 1: "))
m2=float(input("Enter marks in subject 2: "))
m3=float(input("Enter marks in subject 3: "))
avg=(m1+m2+m3)/3
if avg>=90:
    grade='A1'
elif avg>=80:
    grade='A2'
elif avg>=70:
    grade='B1'
elif avg>=60:
    grade='B2'
else:
    grade='C'
print("Average =",avg)
print("Grade =",grade)
