def factorial(x):
    # Base Case: if x is 0 or 1, return 1
    if x == 0 or x == 1:
        return 1
    # Recursive Case: x * factorial of (x - 1)
    else:
        return x * factorial(x - 1)

# 輸入資料，這裡用列表來儲存需要計算階層的數字
input_data = input()

# 計算並輸出每個數字的階層
output_data = int(input_data[0])

print(factorial(output_data))  
