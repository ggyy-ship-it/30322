graph = {}
graph['start'] = {}
graph['start']['A'] = 2
graph['start']['B'] = 5
graph['A'] = {}
graph['A']['B'] = 8
graph['A']['E'] = 7
graph['B'] = {}
graph['B']['E'] = 2
graph['B']['D'] = 4
graph['C'] = {}
graph['C']['B'] = 3
graph['D'] = {}
graph['D']['fin'] = 3
graph['D']['E'] = 6
graph['E'] = {}
graph['E']['fin'] = 1
graph['fin'] = {}
# 成本雜湊表
infinity = float('inf')
costs = {}
costs['A'] = infinity
costs['B'] = infinity
costs['C'] = infinity
costs['D'] = infinity
costs['E'] = infinity
costs['fin'] = infinity
# 建立起始點的路徑成本
s= input()                #輸入起點
for i in graph[s]:
    costs[i]=graph[s][i]

# 建立父節點雜湊表
parents = {}
for i in graph[s]:
    parents[i]=s
processed = []

def find_lowest_cost_node(costs):    
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


node = find_lowest_cost_node(costs)
while node is not None:
    cost = costs[node]
    neighbors = graph[node]
    for n in neighbors.keys():
        new_cost = cost + neighbors[n]  
        if  new_cost<costs[n]:  
            costs[n] = new_cost            
            parents[n] = node    
    processed.append(node)
    node = find_lowest_cost_node(costs)
#print('Cost from the start to each node:')
print('length:',costs['fin'])


# 藉由parents反推路徑
prt = parents.get('fin')   # 先從fin的parent找
path=['fin']               # path紀錄反推路徑，之後再順print回來
while prt :           # 當parent不為空時會繼續找
    path.append(prt)  # 找到則新增至path裡
    prt = parents.get(prt) # 繼續取得前一個prt

while path : # 用堆疊結構後進先出的方式pop出來
    print(path.pop(),end=' ')