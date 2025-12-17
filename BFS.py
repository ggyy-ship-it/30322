from collections import deque

graph = {}

graph['A'] = ['B', 'C', 'D']

graph['B'] = ['E', 'F', 'G']

graph['C'] = ['H' , 'I']

graph['D'] = ['J', 'K' , 'L']
 

def BFS(name , T):

    search_queue = deque()        # 建立搜尋的佇列

    search_queue += graph[name]   # 將目標的朋友加入佇列

    searched = []                 # 建立陣列，紀錄已搜尋過的對象

    while search_queue:           # 當佇列還有人排隊時，會繼續迴圈

        person = search_queue.popleft()  # 取得佇列第一位person

        if person not in searched:       # 判斷person是否有在searched陣列裡面
            print(person)
            if person == T:        # 判斷person是否為目標
                
                return True

            else:

                search_queue += graph.get(person, []) # 將目標的朋友加入佇列

                searched.append(person)       # 將person加入至已搜尋過的陣列        

    return False

 

BFS( 'A' , input())