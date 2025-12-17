# main.py
import csv
import time

def load_numbers(filename="numbers.csv"):
    """
    從 CSV 檔案讀取數字資料。
    :param filename: CSV 檔案的路徑
    :return: 一個包含所有數字的 list
    """
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 跳過標頭行 'number'
            for row in reader:
                numbers.append(int(row[0]))
        print(f"成功從 {filename} 讀取 {len(numbers)} 筆數字。")
        return numbers
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {filename}。請先執行 generate_numbers.py。")
        return []
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return []

# =================================================================
# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 學生需要實作的區域 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# =================================================================

def quick_sort(data):
    """
    實作快速排序法 (Quick Sort)。
    :param data: 待排序的數字列表
    :return: 排序後的數字列表
    """
    # 【任務】請在此處實作快速排序法的演算法。
    # 提示：這是一個遞迴函式，你需要選擇一個基準點 (pivot)。
    # 為了不修改到原始資料，建議複製一份再進行排序。
    sorted_data = data[:] # 複製列表
    # ... 你的程式碼 ...
    def _quick_sort(lst):
        if len(lst) <= 1:
            return lst
        pivot = lst[len(lst) // 2]
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
        return _quick_sort(left) + middle + _quick_sort(right)

    sorted_data = _quick_sort(sorted_data)
    print("（快速排序法）已排序完成。")
    return sorted_data

def selection_sort(data):
    """
    實作選擇排序法 (Selection Sort)。
    :param data: 待排序的數字列表
    :return: 排序後的數字列表
    """
    # 【任務】請在此處實作選擇排序法的演算法。
    # 提示：每一輪都找到未排序部分中的最小值，然後放到正確位置。
    # 為了不修改到原始資料，建議複製一份再進行排序。
    sorted_data = data[:] # 複製列表
    # ... 你的程式碼 ...
    sorted_data = data[:]
    n = len(sorted_data)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if sorted_data[j] < sorted_data[min_index]:
                min_index = j
        sorted_data[i], sorted_data[min_index] = sorted_data[min_index], sorted_data[i]
    print("（選擇排序法）已排序完成。")
    return sorted_data


def linear_search(data, value):
    """
    實作線性搜尋法 (Linear Search)。
    :param data: 數字列表
    :param value: 要搜尋的數字
    :return: 找到的數字索引(int)或 None
    """
    # 【任務】請在此處實作線性搜尋法的演算法。
    # 提示：從頭到尾一個一個比對。
    print(f"（此處應為線性搜尋法）正在搜尋數字 {value}...")
    # ... 你的程式碼 ...
    for i in range(len(data)):
        if data[i] == value:
            return i
    return None


    


def binary_search(data, value):
    """
    實作二元搜尋法 (Binary Search)。
    :param data: **已排序好**的數字列表
    :param value: 要搜尋的數字
    :return: 找到的數字索引(int)或 None
    """
    # 【任務】請在此處實作二元搜尋法的演算法。
    # 提示：使用這個函式前，資料必須先排序好。
    # 提示：需要 low, high, mid 三個指標。
    print(f"（此處應為二元搜尋法）正在搜尋數字 {value}...")
    # ... 你的程式碼 ...

    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == value:
            return mid
        elif data[mid] < value:
            low = mid + 1
        else:
            high = mid - 1
    return None

# =================================================================
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ 學生需要實作的區域 ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
# =================================================================

# =================================================================
# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 進階挑戰 ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# =================================================================

def find_top_n(data, n):
    """
    找出前 N 個最大的數字。
    :param data: 數字列表
    :param n: 要找出的數量
    """
    # 【進階挑戰任務】
    # 1. 使用你實作的任一排序法，進行降冪排序 (由大到小)。
    #    (你可能需要稍微修改你的排序函式，讓它可以支援降冪排序)
    # 2. 取出前 n 個數字並印出。
    print(f"（此處應為找出前 N 大數字）正在找出前 {n} 個最大的數字...")
    # ... 你的程式碼 ...
    sorted_desc = quick_sort(data)[::-1]  # 使用快速排序後反轉為降冪
    top_n = sorted_desc[:n]
    print(f"前 {n} 個最大數字為：{top_n}")
    return top_n
# =================================================================
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲ 進階挑戰 ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
# =================================================================

"""
程式主選單
"""
numbers = load_numbers() # 讀取檔案

sorted_numbers = None # 用來存放排序後的資料

while True:
    print("\n===== 選擇執行的動作 =====")
    print("1. 快速排序 (Quick Sort)")
    print("2. 選擇排序 (Selection Sort)")
    print("3. 線性搜尋 (Linear Search)") 
    print("4. 二元搜尋 (Binary Search)")
    print("--- 進階挑戰 ---")
    print("5. 找出前 N 個最大的數字")
    print("0. 離開程式")
    choice = input("請輸入您的選擇：")

    if choice in ['1', '2']:
        start_time = time.time()
        if choice == '1':
            sorted_numbers = quick_sort(numbers)
        elif choice == '2':
            sorted_numbers = selection_sort(numbers)
        end_time = time.time()
        
        print(f"排序完成，花費時間: {end_time - start_time:.6f} 秒")
        print("排序後前 20 個數字：", sorted_numbers[:20])
        print("排序後末 20 個數字：", sorted_numbers[-20:])

    elif choice in ['3', '4']:
        try:
            value_to_find = int(input("請輸入要搜尋的數字："))
        except ValueError:
            print("輸入無效，請輸入一個整數。")
            continue

        result_index = None
        if choice == '3':
            result_index = linear_search(numbers, value_to_find) 
        elif choice == '4':
            if sorted_numbers is None:
                print("錯誤：二元搜尋需要資料先排序。請先執行選項 1 或 2。")
                continue
            result_index = binary_search(sorted_numbers, value_to_find)

        if result_index is not None:
            print(f"找到了！數字 {value_to_find} 在列表中的索引為: {result_index}")
        else:
            print(f"找不到數字 {value_to_find}。")
    
    elif choice == '5':
        try:
            n = int(input("請輸入要找出前幾名："))
            if n <= 0 or n > len(numbers):
                print(f"錯誤：N 的值 ({n}) 必須介於 1 和總資料數 ({len(numbers)}) 之間。")
                continue
            find_top_n(numbers, n)
        except ValueError:
            print("輸入無效，請輸入一個整數。")

    elif choice == '0':
        print("感謝使用，程式結束。")
        break
    else:
        print("無效的選擇，請重新輸入。")
    input('請按Enter繼續...')