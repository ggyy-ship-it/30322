#創造數列
number = list(map(int,input().split()))
#創造目標
target = int(input())
#重設次數
count = 0
found = False
#設定low&high
low = 0
high = len(number) - 1
#迴圈跑二元搜尋法
while low <= high:
    mid = (low+high)//2
    print(number[mid])
    count += 1
    if number[mid] == target:
        found = True
        break
    elif number [mid] > target:
        high = mid - 1 
    elif number [mid] < target:
        low = mid + 1
#輸出結果
if found :
    print(f"The Computer searched {count} times.")
else :
    print('Not Found')