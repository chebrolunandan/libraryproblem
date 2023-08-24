gender=input()
age=int(input())
amount=float(input())

if (gender=="M" and age<=18):
    amount=amount-(amount*0.05)
elif (gender=="M" and ((age>=18) and (age>=30))):
    amount=amount-(amount*0.1)
if (gender=="F" and age<=18):
    amount=amount-(amount*0.07)
elif (gender=="F" and ((age>=18) and (age>=30))):
    amount=amount-(amount*0.12)
else:
    amount = amount - (amount * 0.15)
print(amount)