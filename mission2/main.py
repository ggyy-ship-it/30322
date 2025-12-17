# main.py
# 這是我們的主程式，負責協調所有模組

import math

# 匯入 (Import) 我們的工具模組
import friends             # 讀取檔案
import friendsDict as fd   # 任務1: 新增/刪除
import bfs                 # 任務2: BFS 應用
import dijkstra as dj      # 任務3: Dijkstra 應用

# --- 選單顯示函式 ---

def print_login_menu():
    """印出「登入/註冊」選單"""
    print("\n" + "="*30)
    print("      歡迎來到友誼小船friend'ship系統")
    print("="*30)
    print("  1. 登入 (Login)")
    print("  2. 註冊 (Register)")
    print("\n  11. 離開程式 (Exit)")
    print("="*30)
    return input("請輸入您的選擇：")

def print_user_menu(username):
    """印出登入後的使用者主選單"""
    print(f"\n--- {username} 的主選單 ---")
    print("  1. 顯示你的朋友")
    print("  2. 新增 / 修改 朋友關係")
    print("  3. 刪除 朋友關係")
    print("  4. 查詢 某人是否在朋友圈內 (BFS)")
    print("  5. 查詢 某人關係最近的路徑 (Dijkstra)")
    # 6,7,8,9為加分題目
    print("  6. 推薦 朋友 (BFS)")
    print("  7. 顯示 完整社交網路")
    print("  8. 顯示 使用者到所有人的社交距離")
    print("  9. 刪除帳號")
    print("\n  10. 登出 (Logout)")
    print("  11. 離開程式 (Exit)")
    print("="*30)
    return input("請輸入您的選擇：")

# --- 輔助函式 (來自您原本的程式碼，非常有用) ---
# 函式中  :型態 -> 型態:   ，單純的註解，讓使用者了解輸入和輸出的型態
def get_validated_person_name(prompt: str, network: dict, must_exist: bool = True) -> str:
    """
    一個共用的函式，用來向使用者詢問人名並進行驗證。    
    :param prompt: 要顯示的提示文字 (例如 "請輸入起始人名: ")
    :param network: 我們的 graph 字典
    :param must_exist: True 表示人名「必須存在」於 network 中 (用於登入、查詢)。
    #                  False 表示人名「必須不存在」於 network 中 (用於註冊)
    :return: 一個已經通過驗證的人名 (str)
    """
    while True:
        # 取得輸入，並用 .strip() 去除前後空白
        person_name = input(prompt).strip()
        # 防止使用者直接按 Enter
        if not person_name:
            print("輸入不得為空，請重新輸入。")
            continue            
        # 檢查人名是否存在
        exists = person_name in network        
        if must_exist:
            # 要求「必須存在」
            if exists:
                return person_name # 驗證通過，回傳人名
            else:
                print(f"錯誤：'{person_name}' 不在社交網路中 (查無此人)，請重新輸入。")
                # 迴圈繼續                
        else:
            # 要求「必須不存在」 (用於註冊)
            if not exists:
                return person_name # 驗證通過，回傳人名
            else:
                print(f"錯誤：'{person_name}' 已經在網路中了，請輸入一個「新」的人名。")
                # 迴圈繼續

# --- 任務 1: 註冊 / 朋友關係 ---
def handle_add_person(network):
    """處理新增一個人 (註冊)"""
    # 使用 validator 驗證 must_exist=False，確保是新人
    person = get_validated_person_name("請輸入要註冊的新人名: ", network, must_exist=False)
    # 呼叫 friendsDict.py 中的 add_person
    fd.add_person(network, person)
    print(f"註冊成功！歡迎, {person}！現在您可以登入了。")

def handle_show_my_friends(network, current_user):
    """(選項1) 顯示目前登入者的朋友"""
    print(f"\n--- {current_user} 的好友列表 ---")
    # 呼叫 friendsDict.py 中的 show_my_friends
    fd.show_my_friends(network, current_user)

def handle_add_friend_user(network, current_user):
    """(選項2) 處理新增/修改朋友關係 (以 current_user 為 p1)"""
    p1 = current_user
    print(f"您目前的身分是: {p1}")
    p2 = get_validated_person_name("請輸入要新增/修改的好友名稱: ", network, must_exist=True)
    
    if p1 == p2:
        print("錯誤：您不能新增自己為好友。")
        return

    while True:
        try:
            closeness = int(input(f"請輸入 {p1} 和 {p2} 的好感距離 (1-100)，數字越小表示越親近："))
            if not 0 < closeness <= 100:
                print("輸入無效：好感距離必須在 1 到 100 之間。")
            else:
                # 呼叫 friendsDict.py 中的 add_friendship
                fd.add_friendship(network, p1, p2, closeness)
                break
        except ValueError:
            print("輸入錯誤：好感距離必須是數字。")

def handle_remove_friend_user(network, current_user):
    """(選項3) 處理刪除朋友關係 (以 current_user 為 p1)"""
    p1 = current_user
    print(f"您目前的身分是: {p1}")
    p2 = get_validated_person_name("請輸入要刪除的好友名稱: ", network, must_exist=True)
    if p1 == p2:
        print("錯誤：您不能刪除自己。")
        return    
    # 呼叫 friendsDict.py 中的 remove_friendship
    fd.remove_friendship(network, p1, p2)

# --- 任務 2: 呼叫 bfs 模組 ---

def handle_is_connected(network, current_user):
    """(選項4) 處理查詢關係層級 (BFS) (以 current_user 為 p1)"""
    p1 = current_user
    print(f"您目前的身分是: {p1}")
    p2 = get_validated_person_name("請輸入要查詢的對象名稱: ", network, must_exist=True)
    
    # 呼叫 bfs.py 中的 is_connected
    friendZone = bfs.is_connected(network, p1, p2)    
    if friendZone:
        print(f"{p2} 在您的朋友圈內！")
    else:
        print(f"{p2} 不在您的朋友圈內。")

# --- 任務 3: 呼叫 dijkstra 模組 ---

def handle_find_path_user(network, current_user):
    """(選項5) 處理查詢最熱絡路徑 (Dijkstra) (以 current_user 為 p1)"""
    p1 = current_user
    print(f"您目前的身分是: {p1}")
    p2 = get_validated_person_name("請輸入要查詢的對象名稱: ", network, must_exist=True)

    # 呼叫 dijkstra.py 中的 find_closest_path
    path, distance = dj.find_closest_path(network, p1, p2)
    
    if distance == float('inf'):
        print(f"找不到路徑：從 {p1} 到 {p2} 沒有路徑。")
    else:
        print(f"從 {p1} 到 {p2} 的最熱絡路徑：")
        print(f"  路徑: {' -> '.join(path)}")
        print(f"  總社交距離: {distance}")

# --- 加分題目 ---
# bfs.py 裡的加分題目
def handle_suggest_friends_user(network, current_user):
    """(選項6) 處理推薦朋友 (BFS) (以 current_user 為 p1)"""
    person = current_user
    print(f"您目前的身分是: {person}")    
    try:
        hops = int(input("請輸入要推薦幾層外的關係(大於1) (例如 2 表示朋友的朋友): "))
        if hops <= 1:
            print("層數必須大於 1")
            return
        # 呼叫 bfs.py 中的 suggest_friends
        suggestions = bfs.suggest_friends(network, person, hops=hops)
        
        if not suggestions:
            print(f"找不到 {hops} 層關係外的潛在朋友。")
        else:
            print(f"推薦給 {person} 的 {hops} 層新朋友：{suggestions}")
    except ValueError:
        print("輸入錯誤：層數必須是數字。")
# dijkstra.py 裡的加分題目        
def handle_show_all_distances(network, current_user):
    """(選項7) 顯示使用者到所有其他人的社交距離"""
    print(f"\n--- {current_user} 的社交距離總覽 ---")
    
    # 1. 呼叫 dijkstra.py 中的 find_all_social_distances
    # 假設該函式會回傳一個字典，例如:{'Alice': 0, 'Bob': 20, 'Charlie': 50, 'David': inf}
    distances = dj.find_all_social_distances(network, current_user)    
    # 2. 印出結果
    if distances is None:
        print("無法計算社交距離，請確認您的網路資料。")
        return
    else:
        for person, distance in distances.items():
            if distance == math.inf:
                print(f"到 {person}：無法連結")
            else:
                print(f"到 {person}：社交距離 {distance}")

# friendsDict.py 裡的加分題目
def handle_print_network(network):
    """(選項8) 顯示目前的社交網路圖"""
    print("\n--- 目前的社交網路圖 ---")
    if not network:
        print("網路是空的。")
        return
    else:
        # 呼叫 friendsDict.py 中的 print_network
        fd.print_network(network)

def handle_remove_person(network, current_user):
    """(選項9) 處理刪除帳號 (以 current_user 為 person)"""
    person = current_user
    print(f"您目前的身分是: {person}")
    confirm = input(f"確定要刪除您的帳號 '{person}' 嗎？此動作無法復原！(y/n): ").strip().lower()
    if confirm == 'y':
        # 呼叫 friendsDict.py 中的 remove_person
        fd.remove_person(network, person)
        print(f"您的帳號 '{person}' 已被刪除。再見！")
    else:
        print("已取消刪除帳號。")
# --- 登入與主迴圈 ---

def handle_login(network):
    """處理登入流程，並進入使用者選單"""
    try:
        # 使用 validator 檢查 'must_exist=True'
        current_user = get_validated_person_name("請輸入您的名字: ", network, must_exist=True)
    except (EOFError, KeyboardInterrupt):
        print("\n取消登入。")
        return None # 回到登入/註冊選單
        
    print(f"\n歡迎回來, {current_user}!")

    # 進入登入後的使用者迴圈
    while True:
        choice = print_user_menu(current_user)
        
        if choice == '1':
            handle_show_my_friends(network, current_user)
        elif choice == '2':
            handle_add_friend_user(network, current_user)
        elif choice == '3':
            handle_remove_friend_user(network, current_user)
        elif choice == '4':
            handle_is_connected(network, current_user)
        elif choice == '5':
            handle_find_path_user(network, current_user)
        elif choice == '6':
            handle_suggest_friends_user(network, current_user)
        elif choice == '7':
            handle_show_all_distances(network, current_user)
        elif choice == '8':
            handle_print_network(network)
        elif choice == '9':
            # 再次確認是否刪除帳號
            print("注意：刪除帳號將會登出並移除所有朋友關係。")
            if input("請確認是否刪除帳號 (y/n): ").strip().lower() == 'y':
                handle_remove_person(network, current_user)
                print(f"您已登出，回到登入/註冊選單。")
                break # 跳出使用者迴圈，回到登入/註冊選單
        elif choice == '10': # 登出
            print(f"再見, {current_user}。您已登出。")
            break # 跳出使用者迴圈，回到登入/註冊選單
        elif choice == '11': # 離開程式
            return 'EXIT' # 傳送 'EXIT' 信號給 main 迴圈
        else:
            print("無效的選擇，請重新輸入。")
        input('按下 Enter 鍵繼續...') # 暫停，讓使用者看結果
    return None # 預設 (登出時)


# --- 程式主要執行流程 ---
def main():
    print("--- 系統啟動 ---")
    
    # 1. 載入社交網路
    # 呼叫 friends.py 中的 load_network 函式
    my_network = friends.load_network("mission2/network_data.txt")
    
    if not my_network:
        print("載入失敗，程式結束。")
        return
    
    print("載入成功！")
    # (啟動時不再預先顯示網路)
    
    # 2. 進入「應用程式」主迴圈 (登入/註冊)
    while True:
        try:
            choice = print_login_menu()
            
            if choice == '1':
                # 登入，並進入使用者選單
                login_status = handle_login(my_network)
                if login_status == 'EXIT':
                    break # 如果從使用者選單選擇 '11'，則結束程式
            
            elif choice == '2':
                # 註冊
                handle_add_person(my_network)
            
            elif choice == '11':
                break # 在登入選單選擇 '11'，結束程式
            
            else:
                print("無效的選擇，請重新輸入。")
        
        except (EOFError, KeyboardInterrupt):
            # 讓使用者可以用 Ctrl+C 或 Ctrl+D 離開程式
            print("\n偵測到使用者中斷...")
            break

    print("感謝使用，系統關閉。")


# --- 程式執行點 ---
if __name__ == "__main__":
    main()