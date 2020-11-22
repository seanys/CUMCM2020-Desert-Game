from collections import defaultdict
from heapq import *
import pandas as pd
import json

def dijkstraRaw(edges, from_node, to_node):
	g = defaultdict(list)
	for l,r,c in edges:
		g[l].append((c,r))
	q, seen = [(0,from_node,())], set()
	while q:
		(cost,v1,path) = heappop(q)
		if v1 not in seen:
			seen.add(v1)
			path = (v1, path)
			if v1 == to_node:
				return cost, path
			for c, v2 in g.get(v1, ()):
				if v2 not in seen:
					heappush(q, (cost+c, v2, path))
	return float("inf"),[]
 
def dijkstra(edges, from_node, to_node):
	len_shortest_path = -1
	ret_path=[]
	length,path_queue = dijkstraRaw(edges, from_node, to_node)
	if len(path_queue)>0:
		len_shortest_path = length		## 1. Get the length firstly;
		## 2. Decompose the path_queue, to get the passing nodes in the shortest path.
		left = path_queue[0]
		ret_path.append(left)		## 2.1 Record the destination node firstly;
		right = path_queue[1]
		while len(right)>0:
			left = right[0]
			ret_path.append(left)	## 2.2 Record other nodes, till the source-node.
			right = right[1]
		ret_path.reverse()	## 3. Reverse the list finally, to make it be normal sequence.
	return len_shortest_path,ret_path

# 获得两个最短路径的可能交点
def getAllInters(routes1,routes2):
    all_inters = []
    for route1 in routes1:
        for route2 in routes2:
            for i in range(1,len(route1)):
                if route1[i] in route2:
                    all_inters.append(route1[i])


if __name__ == "__main__":
    problem_id = 3
    problem = pd.read_csv("problem/problem" + str(problem_id) + "_graph.csv")

    edges = []
    for i in range(problem.shape[0]):
        point = problem["point"][i]
        neighbor = json.loads(problem["neighbor"][i])
        for j in neighbor:
            edges.append((i+1,j,1))
            # print((i+1,j,1))

    length, shortest_path = dijkstra(edges, 1, 8)
