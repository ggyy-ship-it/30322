def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# 輸入
N = int(input())

# 範圍檢查
if 1 < N <= 20: 
    print( fibonacci(N))
    print( fibonacci(N - 1))

