a=["up","right","down","left"]
b=["^",">","v","<"]
s=input().split()
r=""
i=0
while i < len(s):
        e=s[i]
        r+=b[a.index(e)]
        j=1
        i+=1
        while i<len(s) and s[i]==e:j+=1;i+=1
        if j>1: r+=str(j)
print(r)