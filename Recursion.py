def cd(i,k):
    print(i)
    
    if i ==k :
        return
    cd(i-1,k)

s,end=map(int,input().split())
cd(s,end)