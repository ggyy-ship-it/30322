number = list(map(int,input().split()))
#交換數字位置
def swap(x,y) :
    original = number[x]
    number[x] = number[y]
    number[y] = original
#找最小數字
def find_min(start_index) :
    min = number[start_index]
    index = start_index

    for i in range ( start_index+1 ,len(number) ):
        if min > number[i] :
            min = number[i]
            index = i
    return index
#輸出
for i in range(len(number)):
    a = find_min(i)
    swap(i,a)
    print(' '.join(map(str,number)))