# bfs.py
# 任務 2：廣度優先搜尋 (BFS) 的應用
from collections import deque

# --- BFS演算法任務 ---
def is_connected(graph: dict, person1: str, person2: str) -> bool:
    """
    (選項4)  是否在朋友圈內
    (學生任務) 使用 BFS 檢查 person1 是否可以連到 person2。
    """
    # 建立搜尋佇列
    search_queue = deque() 
    # 建立陣列，紀錄已搜尋過的對象   
    searched = set() 
    # 將起始點 person1 加入佇列和 visited 集合
    search_queue.append(person1)
    searched.add(person1)
    # 當佇列還有人排隊時，會繼續迴圈
    ####### (學生需完成) #######
    while search_queue:
        current = search_queue.popleft()
        if current == person2:
            return True
        # 取得鄰居（graph 使用 dict->{neighbor: closeness}）
        for neighbor in graph.get(current, {}).keys():
            if neighbor not in searched:
                searched.add(neighbor)
                search_queue.append(neighbor)
    ###########################
    # 如果佇列都空了還沒找到，表示無法到達
    return False


# --- 加分題目 ---
def suggest_friends(graph: dict, person: str, hops: int = 2) -> list[str]:
    """
    (選項6) 處理推薦朋友 (BFS) (以 current_user 為 p1)
    (學生任務) 推薦新朋友
    找出所有與 person 剛好相隔 'hops' 層關係的人 (例如 "朋友的朋友")
    
    提示：
    1. 這很像 BFS，你需要儲存 (節點, 距離)
    2. 建立一個 results = [] 串列
    3. 當你找到一個節點的 distance == hops 時，把它加入 results
    4. 最後回傳 results
    """
    # (學生進階)
    results = []            
    if person not in graph:
        return results
    visited = set([person])
    queue = deque()
    queue.append((person, 0))
    while queue:
        node, dist = queue.popleft()
        if dist == hops:
            # 不包含自己與已是直接朋友
            if node != person and node not in graph.get(person, {}):
                results.append(node)
            # don't expand nodes at exactly hops
            continue
        # expand next layer
        for neighbor in graph.get(node, {}).keys():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return results