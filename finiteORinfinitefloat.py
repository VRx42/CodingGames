input()
d=int(input())
for n in 2,5:
 while d%n==0:d/=n
print("in"*(d>1)+"finite")