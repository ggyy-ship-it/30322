from collections import deque
graph = {}
graph['you'] = ['alice', 'bob', 'claire']
graph['bob'] = ['anuj', 'peggy']
graph['alice'] = ['peggy']
graph['claire'] = ['thom', 'jonny']
graph['anuj'] = ['rhino','shark']
graph['peggy'] = ['lion']
graph['thom'] = ['braz','leo']
graph['jonny'] = ['hippo','ray']
graph['braz']=['milk']
graph['lion']=[]
graph['shark']=[]
graph['rhino']=[]
graph['leo']=[]
graph['ray']=[]
graph['hippo']=[]
graph['milk']=[]

def BFS(name,T):

    search_queue = deque()        # 建立搜尋的佇列

    search_queue += graph[name]   # 將目標的朋友加入佇列

    searched = []                 # 建立陣列，紀錄已搜尋過的對象

    while search_queue:           # 當佇列還有人排隊時，會繼續迴圈

        person = search_queue.popleft()  # 取得佇列第一位person

        if person not in searched:       # 判斷person是否有在searched陣列裡面
            
            if person[-1] == T:        # 判斷person是否為目標
                
                print(f"Found {person}")

                return True

            else:
                print(person)
                search_queue += graph[person] # 將目標的朋友加入佇列

                searched.append(person)       # 將person加入至已搜尋過的陣列        

    return False

 

BFS('you',input())