no_of_days=int(input())

if (no_of_days<=0 and no_of_days>1460):
    print("invalid")
    exit()
    fee=0
elif (no_of_days<=30):
    fee=0
elif (no_of_days<=60):
    fee=0+(no_of_days-30)*0.5
elif (no_of_days<=120):
    fee=0+15+(no_of_days-60)*1
elif (no_of_days<=250):
    fee=0+15+60+(no_of_days-250)*2
else:
    fee = 0+15+60+240+(no_of_days-240)*3
print(fee)