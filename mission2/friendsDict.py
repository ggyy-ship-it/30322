# friendsDict.py
# 任務 1：基本友誼小船管理 (Dict 操作)
#
# 這裡所有函式的第一個參數都是 'graph'
# 這是 main.py 傳遞過來的「友誼小船圖」

# 函式中  :型態 -> 型態:   ，單純的註解，讓使用者了解輸入和輸出的型態
def add_person(network, person):
    """
    處理新增一個人 (註冊)
    (學生任務) 新增一個「人」（節點），他一開始沒有朋友
    """
    ####### (學生需完成) ######
    network[person]={}
    print(f"已新增 {person}，他目前沒有朋友")
    ###########################

def show_my_friends(graph: dict, current_user: str):
    """
    (選項1) 顯示目前登入者的朋友
    (學生任務) 顯示某個人的所有朋友及好感度
    """
    ####### (學生需完成) ######
    
    friends = graph.get(current_user, {})

    if not friends:
        print(f"{current_user} 沒有任何朋友。")
        return

    for friend, closeness in friends.items():
        print(f"{current_user} -> {friend} (好感度: {closeness})")

    ###########################

def add_friendship(graph: dict, person1: str, person2: str, closeness: int):
    """
    (選項2) 處理新增/修改朋友關係 (以 current_user 為 p1)
    (學生任務) 新增或更新一對朋友關係及其好感度
    提示：記得要 "雙向" 新增
    """
    ####### (學生需完成) ######
    if person1 not in graph:
        graph[person1] = {}
    if person2 not in graph:
        graph[person2] = {}
    graph[person1][person2] = closeness
    graph[person2][person1] = closeness
    ###########################
    print(f"已更新 {person1} 和 {person2} 的關係，好感度 {closeness}")

def remove_friendship(graph: dict, person1: str, person2: str):
    """
    (選項3) 處理刪除朋友關係 (以 current_user 為 p1)
    (學生任務) 刪除一對朋友關係
    提示：
    1. 檢查 person2 是否是 person1 的朋友
    2. 檢查 person1 是否是 person2 的朋友
    3. 雙向都要刪除 (使用 del)
    """
    ####### (學生需完成) ######
    removed = False
    if person1 in graph and person2 in graph[person1]:
        del graph[person1][person2]
        removed = True
    if person2 in graph and person1 in graph[person2]:
        del graph[person2][person1]
        removed = True
    if not removed:
        print(f"{person1} 和 {person2} 並無朋友關係可刪除。")
    ###########################
    print(f"已刪除 {person1} 和 {person2} 的朋友關係")

# --- 加分題目 ---
def print_network(graph: dict):
    """
    (選項8) 顯示目前的社交網路圖
    (進階學生任務) 印出整個社交網路圖
    提示：
    1. 迴圈遍歷 graph 的每個人 (node)
    2. 對每個人，再迴圈遍歷他的朋友 (friend, closeness)
    3. 印出格式：Person1 -> Person2 (Closeness)
    """
    ####### (學生需完成) ######
    
    for person, friends in graph.items():
        if not friends:
            print(f"{person} -> (沒有朋友)")
            continue
        for friend, closeness in friends.items():
            print(f"{person} -> {friend} (好感度: {closeness})")
    ###########################
    print("--- 社交網路圖 ---")
def remove_person(graph: dict, person: str):
    """
    (選項9) 處理刪除帳號 (以 current_user 為 person)
    (進階學生任務) 刪除一個人，以及他所有的朋友關係
    提示：
    1. (重要) 必須先找出 person 的所有朋友 (例如 friends_list = list(graph[person].keys()))
    2. 迴圈遍歷這些朋友，刪除他們指向 person 的連結 (例如 del graph[friend][person])
    3. 最後才刪除 graph[person] (del graph[person])
    """
    ####### (學生需完成) ######
    if person not in graph:
        print(f"{person} 不存在於網路中。")
        return
    # 先複製朋友列表，避免在迴圈中修改 dict
    friends_list = list(graph[person].keys())
    for friend in friends_list:
        if friend in graph and person in graph[friend]:
            del graph[friend][person]
    # 最後刪除此人
    del graph[person]
    ###########################
    print(f"{person} 已消失。")
