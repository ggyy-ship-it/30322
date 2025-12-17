import random
import json
import os
from collections import deque
from datetime import datetime


from typing import Dict, List, Tuple, Optional


graph: Optional[Dict[str, List[Tuple[str, int]]]] = None
planets: Optional[List[str]] = None

# ----------------------------
# Random data generator
# ----------------------------

def generate_random_space_data(num_planets=50, num_routes=120, filename="space_map.json"):
    planets = [f"Planet_{i}" for i in range(num_planets)]

    routes = []
    existing = set()
    attempts = 0
    while len(routes) < num_routes and attempts < num_routes * 10:
        a = random.choice(planets)
        b = random.choice(planets)
        if a == b:
            attempts += 1
            continue
        key = (a, b)
        if key in existing:
            attempts += 1
            continue
        fuel_cost = random.randint(1, 50)
        routes.append({"from": a, "to": b, "fuel": fuel_cost})
        existing.add(key)

    data = {"planets": planets, "routes": routes, "meta": {"generated_at": str(datetime.now())}}
    with open(filename, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(planets)} planets and {len(routes)} routes -> {filename}")


# ----------------------------
# Load / Build Graph
# ----------------------------

def load_space_map(filename="space_map.json"):
    if not os.path.exists(filename):
        print("Data file not found. Please generate or provide space_map.json")
        return None, None
    with open(filename, "r",encoding="utf-8") as f:
        data = json.load(f)

    planets = data.get("planets", [])
    graph = {p: [] for p in planets}  

    for r in data.get("routes", []):
        frm = r["from"]
        to = r["to"]
        fuel = r["fuel"]
        if frm in graph:
            graph[frm].append((to, fuel))
        else:
            graph[frm] = [(to, fuel)]
    return planets, graph


# ----------------------------
# Search: Linear / Binary
# ----------------------------

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def binary_search(sorted_arr, target):
    left, right = 0, len(sorted_arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# ----------------------------
# Sort: Selection / Quicksort
# ----------------------------

def selection_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)


# ----------------------------
# BFS: shortest by hops
# ----------------------------

def bfs_path(graph, start, goal):
    if start not in graph or goal not in graph:
        return []
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path


# ----------------------------
# Dijkstra: shortest by weight (fuel)
# ----------------------------

def dijkstra(graph, start):
    if start not in graph:
        return {}
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    visited = set()

    while len(visited) < len(graph):
        candidates = [n for n in graph if n not in visited]
        if not candidates:
            break
        u = min(candidates, key=lambda x: dist[x])
        if dist[u] == float('inf'):
            break
        visited.add(u)
        for v, w in graph.get(u, []):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return dist, prev


def reconstruct_path(prev, start, goal):
    if goal not in prev and start != goal:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    if path[0] == start:
        return path
    return []


# ----------------------------
# Visualization using graphviz
# ----------------------------

def visualize_graphviz(graph, filename="space_map", engine='dot'):
    
    try:
        from graphviz import Digraph
    except ImportError:
        print("請先安裝 python graphviz 套件：pip install graphviz")
        return None

    dot = Digraph(comment='Space Map', engine=engine)
    dot.attr('node', shape='circle')

    for node in graph:
        dot.node(node, node)

    for u in graph:
        for v, w in graph[u]:
            dot.edge(u, v, label=str(w))

    output_path = dot.render(filename=filename, cleanup=True)
    print(f"GraphViz 圖檔已產生：{output_path}")
    return output_path



# ----------------------------
# Utility: print small summary
# ----------------------------

def summary(planets, graph):
    if planets is None or graph is None:
        print("No data loaded.")
        return
    total_edges = sum(len(v) for v in graph.values())
    print(f"Planets: {len(planets)} | Routes: {total_edges}")


# ----------------------------
# CLI Menu
# ----------------------------

def cli_menu():
    
    global planets, graph
    filename = "space_map.json"
    menu = """
    
Space Navigation CLI
--------------------
1) 生成隨機資料 (預設: 50 planets, 120 routes)
2) 載入資料 (space_map.json)
3) 顯示資料摘要
4) 列出前 N 個星球
5) 排序行星 (Selection / Quicksort)
6) 搜尋行星 (Linear / Binary)
7) BFS (最少跳躍) 路徑
8) Dijkstra (最低燃料) 到特定星球
9) 視覺化 (GraphViz)
0) 離開程式
"""

    while True:
        print(menu)
        choice = input("輸入選項: ").strip()

        if choice == '1':
            n = input("要生成幾個星球？預設50: ").strip() or '50'
            m = input("要生成幾條航道？預設120: ").strip() or '120'
            
            filename_input = input("輸入生成檔案名稱（不含副檔名，預設: space_map）: ").strip() or "space_map"
            filename = f"{filename_input}.json"

            try:
                n = int(n)
                m = int(m)

                if n <= 0 or m <= 0:
                    raise ValueError("數量必須為正整數")

                generate_random_space_data(n, m, filename)

            except ValueError as e:
                print("輸入錯誤：", e)

        elif choice == '2':
            files = [f for f in os.listdir('.') if f.endswith('.json')]
    
            if not files:
                print("目前資料夾沒有任何 JSON 檔案，請先生成資料")
                continue

            print("可載入的資料檔案：")
            for idx, f in enumerate(files):
                print(f"{idx+1}) {f}")
            
            while True:
                sel = input(f"請選擇要載入的檔案 (1-{len(files)}): ").strip()
                if not sel.isdigit():
                    print("請輸入數字")
                    continue
                sel = int(sel)
                if sel < 1 or sel > len(files):
                    print("數字超出範圍")
                    continue
                filename = files[sel-1]
                break
            planets, graph = load_space_map(filename)
            if planets is not None:
                print("載入完成。")

        elif choice == '3':
            summary(planets, graph)

        elif choice == '4':
            if not isinstance(planets, list):
                print("請先載入資料 (選項2)。")
                continue

            while True:
                n_str = input("顯示前多少個星球？（正整數，預設10）: ").strip() or "10"
                if not n_str.isdigit():
                    print("請輸入正整數")
                    continue

                N = int(n_str)
                if N <= 0:
                    print("數字必須大於 0")
                    continue

                break

            print(planets[:N])


        elif choice == '5':
            if not isinstance(planets, list):
                print("請先載入資料 (選項2)。")
                continue

            
            while True:
                print("a) Selection Sort")
                print("b) Quicksort")
                t = input("選擇排序方法 (a/b): ").strip().lower()

                if t == 'a':
                    sorted_result = selection_sort(planets)
                    method_name = "Selection Sort"
                    break
                
                elif t == 'b':
                    sorted_result = quicksort(planets)
                    method_name = "Quicksort"
                    break
                
                else:
                    print("輸入錯誤，請輸入 a 或 b")

            
            while True:
                n = input("要顯示幾項資料？（正整數）: ").strip()

                if not n.isdigit():
                    print("請輸入正整數")
                    continue

                n = int(n)
                if n <= 0:
                    print("數字必須大於 0")
                    continue

                break

            
            print(f"\n[{method_name}] 前 {n} 筆資料：")
            print(sorted_result[:n])


        elif choice == '6':
            if not isinstance(planets, list):
                print("請先載入資料 (選項2)。")
                continue
            
            target = input("輸入要搜尋的星球名稱（例如 Planet_10）: ").strip()
            if not target:
                print("星球名稱不可為空")
                continue
            
            print("Linear Search:")
            idx = linear_search(planets, target)
            
            if idx >= 0:
                print(f"Found at index {idx} ")
            else:
                print("Not found ")

            print("Binary Search ")
            sorted_planets = quicksort(planets)
            idx2 = binary_search(sorted_planets, target)
            
            if idx2 >= 0:
                print(f"Found in sorted list at index {idx2}")
            else:
                print("Not found in sorted list")

        elif choice == '7':
            if not isinstance(graph, dict):
                print("請先載入資料 (選項2)。")
                continue
            
            while True:
                s = input("起點: ").strip()
                g = input("終點: ").strip()
                if s not in graph or g not in graph:
                    print("節點不存在，請重新輸入")
                    continue
                break
            
            path = bfs_path(graph, s, g)
            if path:
                print(f"BFS 最少跳躍路徑 ({len(path)-1} hops):", " -> ".join(path))
            else:
                print("找不到路徑")

        elif choice == '8':
            if not isinstance(graph, dict):
                print("請先載入資料 (選項2)。")
                continue
            
            while True:
                s = input("起點: ").strip()
                g = input("終點: ").strip()
                
                if s not in graph or g not in graph:
                    print("節點不存在或無法抵達，請重新輸入")
                    continue
                break
            
            dist, prev = dijkstra(graph, s)
            
            if g not in dist or dist[g] == float('inf'):
                print("無法抵達")
            else:
                path = reconstruct_path(prev, s, g)
                print(f"最低燃料總量: {dist[g]}")
                print("路徑:", " -> ".join(path))

        elif choice == '9':
            if graph is None:
                print("請先載入資料 (選項2)。")
                continue

            out = input("輸出檔名(不含副檔名) 預設: space_map_viz: ").strip() or 'space_map_viz'
            print("正在產生 GraphViz 圖檔...")

            res = visualize_graphviz(graph, filename=out)
            if res:
                print("完成，可使用檔案總管開啟圖檔")

        elif choice == '0':
            print("Goodbye,World.")
            break


if __name__ == '__main__':
    cli_menu()
