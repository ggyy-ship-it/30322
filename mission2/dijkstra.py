# dijkstra.py
# 任務 3：Dijkstra 演算法的應用

def find_lowest_cost_node(costs, processed):
    """
    在尚未處理的節點中，尋找成本最低的節點。
    """
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

# --- dijkstra演算法任務 ---
def find_closest_path(graph: dict, person1: str, person2: str):
    """
    (選項5) 處理查詢最熱絡路徑 (Dijkstra) (以 current_user 為 p1)
    (學生任務) 找出從 person1 到 person2「最熱絡」的路徑 (最小社交距離)
    使用 Dijkstra 演算法來找出最短路徑
    """        
    # 圖形雜湊表 
    # graph
    # 成本雜湊表
    # 1. 初始化所有節點的成本 (Costs)為infinity
    infinity = float('inf')
    costs = {}    
    # 取得所有節點
    all_nodes = set(graph.keys())
    # costs[]初始化所有節點為 infinity
    for node in all_nodes:
        costs[node] = infinity
    costs[person1] = 0 # 起點
    # 2. 初始化父節點 (Parents) 雜湊表
    parents = {}    
    # 3. 初始化已處理 (Processed) 列表
    processed = []
    # 4. 演算法主迴圈
    # 從尚未處理的節點中(processed)，找出成本最低的節點node
    node = find_lowest_cost_node(costs, processed)
    ####### (學生需完成) ######
    for neighbor, weight in graph.get(person1, {}).items():
        costs[neighbor] = weight
        parents[neighbor] = person1
    while node is not None:
        cost = costs[node]
        neighbors = graph.get(node, {})
        for n, w in neighbors.items():
            new_cost = cost + w
            if new_cost < costs.get(n, infinity):
                costs[n] = new_cost
                parents[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs, processed)
    ###########################
    # 6. 藉由 parents 反推路徑 (沿用您的邏輯)
    path = [person2]
    ####### (學生需完成) #######
    if costs.get(person2, infinity) == infinity:
        return [], infinity

    path = []
    cur = person2
    while cur != person1:
        path.append(cur)
        cur = parents.get(cur)
        if cur is None:
            # 無法回溯到起點
            return [], costs[person2]
    path.append(person1)
    path.reverse()
    ###########################
    return path, costs[person2]


# --- 加分題目 ---

def find_all_social_distances(graph: dict, person: str) -> dict:
    """
    (選項7) 顯示使用者到所有其他人的社交距離
    (進階學生任務) 找出 person 到「所有其他人」的最短社交距離
    (Dijkstra 演算法的標準產出)    
    """
    # (學生進階)
    infinity = float('inf')
    costs = {node: infinity for node in graph.keys()}
    costs[person] = 0
    parents = {}
    processed = []

    for neighbor, weight in graph.get(person, {}).items():
        costs[neighbor] = weight
        parents[neighbor] = person

    node = find_lowest_cost_node(costs, processed)
    while node is not None:
        cost = costs[node]
        for n, w in graph.get(node, {}).items():
            new_cost = cost + w
            if new_cost < costs.get(n, infinity):
                costs[n] = new_cost
                parents[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs, processed)

    return costs
