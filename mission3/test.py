#!/usr/bin/env python3
"""
space_navigation_with_cli_and_graphviz.py

功能：
- 生成隨機太空資料 (star map)
- 讀取/儲存 JSON
- 提供互動式 CLI 選單
- 搜尋/排序/演算法：Linear/Binary Search, Selection/Quicksort, BFS, Dijkstra
- 使用 Graphviz 產生可視化（節點 + 帶權重的邊）

注意：程式不使用 class，全部以 dict & list 做資料設計。

執行： python space_navigation_with_cli_and_graphviz.py

依賴：
- graphviz (Python) -> pip install graphviz
- Graphviz system binary (為了 render 圖檔，請先安裝系統版 graphviz)
"""

import random
import json
import os
import sys
from collections import deque
from datetime import datetime
import tempfile

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
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✔ Generated {len(planets)} planets and {len(routes)} routes -> {filename}")


# ----------------------------
# Load / Build Graph
# ----------------------------

def load_space_map(filename="space_map.json"):
    if not os.path.exists(filename):
        print("Data file not found. Please generate or provide space_map.json")
        return None, None
    with open(filename, "r") as f:
        data = json.load(f)

    planets = data.get("planets", [])
    graph = {p: [] for p in planets}  # adjacency list: {node: [(neighbor, fuel), ...]}

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
        # choose unvisited node with smallest dist
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

def visualize_graphviz(graph, filename="space_map", view=False, engine='dot'):
    try:
        from graphviz import Digraph
    except Exception as e:
        print("請先安裝 python graphviz 套件：pip install graphviz")
        return None

    dot = Digraph(comment='Space Map', engine=engine)
    dot.attr('node', shape='circle')

    # add nodes
    for node in graph:
        dot.node(node, node)

    # add edges with fuel label
    for u in graph:
        for v, w in graph[u]:
            dot.edge(u, v, label=str(w))

    output_path = dot.render(filename=filename, cleanup=True)
    print(f"Generated graph visualization -> {output_path}")
    if view:
        try:
            os.system(f'"{output_path}"')
        except Exception:
            pass
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
    planets, graph = None, None
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
0) 離開
"""

    while True:
        print(menu)
        choice = input("輸入選項: ").strip()

        if choice == '1':
            n = input("要生成幾個星球？預設50: ").strip() or '50'
            m = input("要生成幾條航道？預設120: ").strip() or '120'
            try:
                generate_random_space_data(int(n), int(m), filename)
            except Exception as e:
                print("生成失敗:", e)

        elif choice == '2':
            planets, graph = load_space_map(filename)
            if planets is not None:
                print("載入完成。")

        elif choice == '3':
            summary(planets, graph)

        elif choice == '4':
            if planets is None:
                print("請先載入資料 (選項2)。")
                continue
            N = int(input("顯示前多少個星球？預設10: ").strip() or '10')
            print(planets[:N])

        elif choice == '5':
            if planets is None:
                print("請先載入資料 (選項2)。")
                continue
            print("a) Selection Sort\nb) Quicksort")
            t = input("選擇排序方法: ").strip().lower()
            if t == 'a':
                out = selection_sort(planets)
                print("Sorted (selection):", out[:20])
            else:
                out = quicksort(planets)
                print("Sorted (quicksort):", out[:20])

        elif choice == '6':
            if planets is None:
                print("請先載入資料 (選項2)。")
                continue
            target = input("輸入要搜尋的星球名稱（例如 Planet_10）: ").strip()
            print("Linear Search:")
            idx = linear_search(planets, target)
            if idx >= 0:
                print(f"Found at index {idx} (unsorted)")
            else:
                print("Not found (unsorted)")

            print("Binary Search (需先排序)")
            sorted_planets = quicksort(planets)
            idx2 = binary_search(sorted_planets, target)
            if idx2 >= 0:
                print(f"Found in sorted list at index {idx2}")
            else:
                print("Not found in sorted list")

        elif choice == '7':
            if graph is None:
                print("請先載入資料 (選項2)。")
                continue
            s = input("起點: ").strip()
            g = input("終點: ").strip()
            path = bfs_path(graph, s, g)
            if path:
                print(f"BFS 最少跳躍路徑 ({len(path)-1} hops):", " -> ".join(path))
            else:
                print("找不到路徑或節點不存在")

        elif choice == '8':
            if graph is None:
                print("請先載入資料 (選項2)。")
                continue
            s = input("起點: ").strip()
            g = input("終點: ").strip()
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
            out = input("輸出檔名(不含副檔名)預設: space_map_viz: ").strip() or 'space_map_viz'
            print("正在產生可視化，若系統未安裝 graphviz binary，可能失敗。")
            res = visualize_graphviz(graph, filename=out)
            if res:
                print("視覺化完成：", res)

        elif choice == '0':
            print("Bye")
            break
        else:
            print("無效選項，請重新輸入。")


if __name__ == '__main__':
    cli_menu()
