number = list(map(int,input().split()))
x,y = map(int,input().split())
original = number[x]
number[x] = number[y]
number[y] = original
for i in number :
    
    print(i , end=' ')