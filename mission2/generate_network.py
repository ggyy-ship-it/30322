# generate_network.py
# 
# 目的：一個用來隨機產生社交網路資料檔的工具
# 執行方式：python generate_network.py
#
# (修改版：根據需求，每組配對 (A,B) 都會產生 A->B 和 B->A 兩筆資料)

import random

# --- 1. 設定區 ---
# 你可以在這裡調整參數

FILENAME = "network_data.txt" # 要輸出的檔案名稱
NUM_PEOPLE = 10       # 總共要有幾個人 (例如：10 位)
NUM_EDGES = 20        # 總共要產生幾 *組* 朋友關係 (例如：20 組，會產生 40 筆資料)

MIN_CLOSENESS = 1     # 最小好感度
MAX_CLOSENESS = 100   # 最大好感度

# 為了方便擴充，我們用 "p1", "p2"... 來當作人名
people_list = [f"f{i}" for i in range(1, NUM_PEOPLE + 1)]

# --- 2. 主要邏輯 ---
def generate_file():
    print(f"--- 隨機社交網路產生器 (雙向版) ---")
    
    # 我們需要一個 set 來確保朋友關係「不重複」
    # (A, B) 和 (B, A) 視為同一組
    existing_edges = set()
    
    # 檢查：避免要求的關係數 > 最大可能關係數
    max_possible_edges = (NUM_PEOPLE * (NUM_PEOPLE - 1)) // 2
    if NUM_EDGES > max_possible_edges:
        print(f"警告：要求的關係組數 ({NUM_EDGES}) 大於最大可能 ({max_possible_edges}).")
        print(f"將只產生 {max_possible_edges} 組關係。")
        target_edge_count = max_possible_edges
    else:
        target_edge_count = NUM_EDGES

    try:
        with open(FILENAME, 'w', encoding='utf-8') as f:
            # 1. 寫入標題行
            f.write("Person1,Person2,Closeness\n")
            
            # 2. 開始隨機產生
            while len(existing_edges) < target_edge_count:
                # 隨機挑兩個不同的人
                p1 = random.choice(people_list)
                p2 = random.choice(people_list)
                
                if p1 == p2:
                    continue # 不可以跟自己當朋友，重抽
                
                # 為了避免 (A,B) 和 (B,A) 同時出現，我們統一排序
                pair = tuple(sorted((p1, p2)))
                
                # 如果這組關係還不存在
                if pair not in existing_edges:
                    # 加入 set 中
                    existing_edges.add(pair)
                    
                    # --- 修改點：產生雙向關係 ---
                    
                    # 1. 產生 A -> B (pair[0] -> pair[1])
                    closeness_ab = random.randint(MIN_CLOSENESS, MAX_CLOSENESS)
                    f.write(f"{pair[0]},{pair[1]},{closeness_ab}\n")
                    
                    # 2. 產生 B -> A (pair[1] -> pair[0])
                    closeness_ba = random.randint(MIN_CLOSENESS, MAX_CLOSENESS)
                    f.write(f"{pair[1]},{pair[0]},{closeness_ba}\n")
        
        print(f"\n成功！")
        print(f"已產生 {NUM_PEOPLE} 個人， {len(existing_edges)} 組雙向關係 (共 {len(existing_edges) * 2} 筆資料)。")
        print(f"檔案已儲存至：{FILENAME}")

    except Exception as e:
        print(f"產生檔案時發生錯誤: {e}")

# --- 3. 程式執行點 ---
if __name__ == "__main__":
    generate_file()