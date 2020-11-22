'''
算法说明：getAllRoutes基于对最路径算法Dijkstra算法修改，实现获得两点之间最短路径的功能；
getKeyPoint则是文中提到的寻找可能会做出决策关键位置，是路径交点中，离两个点最近的位置。
该算法可以实现模型的简化，也可以寻找潜在产生决策的位置。

案例说明：第三关中，寻找起点1号到矿山9号和终点13号的可能关键结点，首先计算出起点到达矿山和
终点的全部最短路径，计算其公共位置，从公共位置中选择出到矿山和终点的距离之和最短的位置，该位
置4号即为可能产生决策的位置。
'''
import pandas as pd
import json
import copy

# 获得路径的全部交点，选择离目标位置最近的点
def getKeyPoint(routes1, routes2, pt1, pt2):
    all_inters = getAllInters(routes1,routes2)
    min_distance = 99999999
    key_pt = []
    for inter in all_inters:
        routes1 = getAllRoutes(inter,pt1)
        routes2 = getAllRoutes(inter,pt2)
        distance = len(routes1[0]) + len(routes2[0])
        if distance < min_distance:
            key_pt = inter
            min_distance = distance
    return key_pt
    
# 获得两个最短路径的可能交点
def getAllInters(routes1,routes2):
    all_inters = []
    for route1 in routes1:
        for route2 in routes2:
            for i in range(1,len(route1)):
                if route1[i] in route2:
                    all_inters.append(route1[i])
    return all_inters

# 根据有向链求解全部的途径
def getAllRoutes(from_id, to_id):
    # print(from_id, to_id)
    front_neighbors = getAllFrontNeighbor(from_id, to_id)
    # print(front_neighbors)
    routes = []
    reversed_routes = [[to_id]]
    temp_reversed_routes = []
    i = 0
    while True:
        get_end = False
        temp_reversed_routes = []
        for route in reversed_routes:
            for front_pt in front_neighbors[route[-1]-1]:
                temp_reversed_routes.append(route+[front_pt]) # 仅仅append处理是不增加的！！！
                if front_pt == from_id:
                    get_end = True
        reversed_routes = copy.deepcopy(temp_reversed_routes)
        if get_end == True:
            break
        i = i +1 
    for item in reversed_routes:
        item.reverse()
        routes.append(item)
    # print(routes)
    return routes

# 获得全部的单向网络
def getAllFrontNeighbor(from_id,to_id):
    cur_pts = [from_id] # 当前本轮外面的点
    searched_pts = [from_id] # 已经检索过的位置
    around_graph = [] # 按照距离存储的图
    cur_distance = 1 # 当前距离
    front_neighbors = [[] for i in range(problem.shape[0])] # 前面的邻接边，可能有多条

    while True:
        # 首先计算出全部的周边点
        all_neighbor_pts = []
        for cur_pt in cur_pts:
            for pt_id in neighbors[cur_pt-1]:
                if pt_id not in searched_pts:
                    if pt_id not in all_neighbor_pts:
                        all_neighbor_pts.append(pt_id)
                    front_neighbors[pt_id-1].append(cur_pt)
        # 计算完该轮区域
        around_graph.append(all_neighbor_pts)
        cur_pts = all_neighbor_pts
        searched_pts = searched_pts + all_neighbor_pts

        if to_id in searched_pts:
            break

    return front_neighbors

if __name__ == "__main__":
    problem_id = 3
    problem = pd.read_csv("problem/problem" + str(problem_id) + "_graph.csv")
    neighbors = []

    for i in range(problem.shape[0]):
        neighbors.append(json.loads(problem["neighbor"][i]))

    from_id, to_id1 = 1, 13 # 起始位置与目标位置
    routes1 = getAllRoutes(from_id,to_id1) # 获得全部的路径
    print("1-13的全部路径：")
    print(routes1)
    
    from_id, to_id2 = 1, 9 # 起始位置与目标位置
    routes2 = getAllRoutes(from_id,to_id2) # 获得全部的路径
    print("1-9的全部路径：")
    print(routes2)

    key_pt = getKeyPoint(routes1,routes2,to_id1,to_id2)
    print("起点前往终点和矿山的潜在决策位置：")
    print(key_pt)
