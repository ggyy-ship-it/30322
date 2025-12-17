number = list(map(int,input().split()))
target = int(input())
count = 0
found = False

for i in number:
    print(i)
    count += 1
    if i == target:
        found = True
        break

if found:
    print(f"The Computer searched {count} times.")
else :
    print("Not found")