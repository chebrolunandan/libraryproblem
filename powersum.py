num=int(input())
s=0 , p=0
while num>0:
    d=num%10
    s=s+(d**p)
    p=d
    num=num//10
print(s)