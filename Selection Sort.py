number = list( map( int,input().split() ) )
min = number[0]
index = 0


for i in range ( 1 ,len(number) ):
    if min > number[i] :
        min = number[i]
        index = i
    
print( min , index )