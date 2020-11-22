from random import random,choice,shuffle

class Point:
    def __init__(self,index):
        self.name=index
        self.neighbours=[]
        self.type=0
        self.players=0
        # 0 1 2 3 4: 普通 村庄 矿山 起点 终点

    def addNeighbour(self,pt):
        self.neighbours.append(pt)

    def setType(self,t):
        self.type=t

class Solution:
    def __init__(self,step,prev,money,pt,key):
        self.step=step
        self.prev=prev
        self.next=[]
        self.money=money
        self.pt_index=pt
        self.key=key
        self.last_supply=key
        self.last_supply_pt=0
        self.last_cash=money

class Decision:
    def __init__(self,start,end,weather,getMineral=False):
        self.start,self.end,self.weather=start,end,weather
        self.water=self.food=self.money=0 # 消耗为正 赚得为负 水或食物单位为箱
        if start.name==end.name and start.type!=4:
            if getMineral:
                self.getMineral(weather)
            else:
                self.water=WATER_CONSUMPTION[weather]
                self.food=FOOD_CONSUMPTION[weather]
        if start.name!=end.name:
            self.water=2*WATER_CONSUMPTION[weather]
            self.food=2*FOOD_CONSUMPTION[weather]
            if MOVE_PLAN[start.name-1][end.name-1]>1:
                self.water=self.water*MOVE_PLAN[start.name-1][end.name-1]
                self.food=self.food*MOVE_PLAN[start.name-1][end.name-1]


    def getMineral(self,weather):
        self.water=3*WATER_CONSUMPTION[weather]
        self.food=3*FOOD_CONSUMPTION[weather]
        if POINTS[self.start.name-1].players>1:
            if MINING>0:
                self.money=-PROFIT/MINING
            else:
                self.money=-PROFIT
        else:
            self.money=-PROFIT

WEATHER=[]
DAY_NUM=0
MAX_BURDEN=0
INIT_MONRY=0
PROFIT=0
WATER_WEIGHT=0
WATER_PRICE=0
FOOD_WEIGHT=0
FOOD_PRICE=0
WATER_CONSUMPTION={}
FOOD_CONSUMPTION={}
POINTS=[]
POINT_NUM=0
DESTINATION=0
MOVE_PLAN=[]
MINING=0
WATER_ADD={}
FOOD_ADD={}
MONEY_REDUCE={}

def loadPoints(file_name):
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line=line.split(',')
            p=Point(int(line[0]))
            POINTS[int(line[0])-1]=p
            if line[2].replace('\n','')!='':
                p.setType(int(line[2]))
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line=line.split(',')
            if line[1]!='':
                for pt in line[1].split(' '):
                    POINTS[int(line[0])-1].addNeighbour(POINTS[int(pt)-1])

def loadEnvir(problem_no):
    global WEATHER
    global DAY_NUM
    global MAX_BURDEN
    global INIT_MONRY
    global PROFIT
    global WATER_WEIGHT
    global WATER_PRICE
    global FOOD_WEIGHT
    global FOOD_PRICE
    global WATER_CONSUMPTION
    global FOOD_CONSUMPTION
    global POINT_NUM
    global DESTINATION
    global MOVE_PLAN
    if problem_no==1 or problem_no==2:
        WEATHER='高温,高温,晴朗,沙暴,晴朗,高温,沙暴,晴朗,高温,高温,沙暴,高温,晴朗,高温,高温,高温,沙暴,沙暴,高温,高温,晴朗,晴朗,高温,晴朗,沙暴,高温,晴朗,晴朗,高温,高温'.split(',')
        DAY_NUM=30
        MAX_BURDEN=1200
        INIT_MONRY=10000
        PROFIT=1000
        WATER_WEIGHT=3
        WATER_PRICE=5
        FOOD_WEIGHT=2
        FOOD_PRICE=10
        WATER_CONSUMPTION={'晴朗':5,'高温':8,'沙暴':10}
        FOOD_CONSUMPTION={'晴朗':7,'高温':6,'沙暴':10}
        POINT_NUM=12 if problem_no==1 else 17
        DESTINATION=9 if problem_no==1 else 12
        assert(len(WEATHER)==DAY_NUM)
        for i in range(POINT_NUM):
            POINTS.append([])
            MOVE_PLAN.append([])
            for j in range(POINT_NUM):
                MOVE_PLAN[i].append(0)            
        loadPoints('problem/problem{}_graph_simple.csv'.format(problem_no))
    if problem_no==6:
        DAY_NUM=30
        MAX_BURDEN=1200
        INIT_MONRY=10000
        PROFIT=1000
        WATER_WEIGHT=3
        WATER_PRICE=5
        FOOD_WEIGHT=2
        FOOD_PRICE=10
        WATER_CONSUMPTION={'晴朗':3,'高温':9,'沙暴':10}
        FOOD_CONSUMPTION={'晴朗':4,'高温':9,'沙暴':10}
        POINT_NUM=25
        DESTINATION=24
        for i in range(POINT_NUM):
            POINTS.append([])
            MOVE_PLAN.append([])
            for j in range(POINT_NUM):
                MOVE_PLAN[i].append(0)  
        loadPoints('problem/problem6_graph.csv') 

def getDecision(point,day):
    decision_list=[]
    if WEATHER[day]!='沙暴':
        for pt in point.neighbours:
            decision_list.append(Decision(point,pt,WEATHER[day]))
    decision_list.append(Decision(point,point,WEATHER[day]))
    if point.type==2:
        decision_list.append(Decision(point,point,WEATHER[day],getMineral=True))
    return decision_list

def getKey(water,food):
    return str(water).zfill(4)+str(food).zfill(4)

def revertKey(key):
    return int(key[0:4]),int(key[4:8])

def dp_main(init_water,init_food,start_day=0,init_pt=0,init_money=None,all_path=False):
    global WATER_ADD
    global FOOD_ADD
    global MONEY_REDUCE
    solution=[]
    for i in range(DAY_NUM+1):
        solution.append([])
        for j in range(POINT_NUM):
            solution[i].append({})            
    cur_key=getKey(init_water,init_food)
    if init_money==None:
        init_m=INIT_MONRY-init_water*WATER_PRICE-init_food*FOOD_PRICE
    else:
        init_m=init_money
    solution[start_day][init_pt][cur_key]=Solution(start_day,None,init_m,init_pt,cur_key)
    for step in range(start_day,DAY_NUM):
        real_date=step # 顺序法
        pt_list=list(range(POINT_NUM))
        shuffle(pt_list)
        for pt in pt_list:
            records=solution[step][pt]
            if len(records)==0:
                continue                   
            decisions=getDecision(POINTS[pt],real_date)
            shuffle(decisions)
            for d in decisions:
                _water,_food,_money=d.water,d.food,d.money #变化量
                for key in list(records.keys()):
                    cur_solution=records[key]
                    # if key=='00140228' and step==9 and pt==16:
                    #     print(9)
                    water,food=revertKey(key)
                    new_water=water-_water
                    new_food=food-_food
                    new_money=cur_solution.money-_money
                    last_cash=cur_solution.last_cash
                    last_supply=cur_solution.last_supply
                    last_supply_pt=cur_solution.last_supply_pt
                    if d.end.type==4 or d.end.type==1:
                        last_water,last_food=revertKey(last_supply)
                        last_cash=new_money
                        water_buy,food_buy=0,0
                        if new_water<0:
                            water_buy=-new_water
                        if new_food<0:
                            food_buy=-new_food
                        if water_buy>0 or food_buy>0:
                            if last_supply==cur_key:
                                continue
                            canBuy=False
                            if POINTS[last_supply_pt].players<2:
                                cost_k=2
                            if POINTS[last_supply_pt].players>1:
                                cost_k=4
                            cost=water_buy*WATER_PRICE*cost_k+food_buy*FOOD_PRICE*cost_k
                            if (last_water+water_buy)*WATER_WEIGHT+(last_food+food_buy)*FOOD_WEIGHT<=MAX_BURDEN and cost<=last_cash:
                                canBuy=True
                            if canBuy:
                                new_money=new_money-cost
                                new_water=new_water+water_buy
                                new_food=new_food+food_buy
                                WATER_ADD[last_supply]=water_buy
                                FOOD_ADD[last_supply]=food_buy
                                MONEY_REDUCE[last_supply]=cost
                                last_cash=new_money
                                last_supply=getKey(new_water,new_food)
                                last_supply_pt=d.end.name-1
                            else:
                                continue
                        else:
                            last_supply=getKey(new_water,new_food)
                            last_supply_pt=d.end.name-1
                    new_key=getKey(new_water,new_food)   
                    new_solution=Solution(step+1,cur_solution,new_money,d.end.name-1,new_key)
                    new_solution.last_cash=last_cash
                    new_solution.last_supply=last_supply
                    new_solution.last_supply_pt=last_supply_pt
                    cur_solution.next.append(new_solution)
                    if new_key in solution[step+1][d.end.name-1]:
                        if solution[step+1][d.end.name-1][new_key].money>new_solution.money:
                            continue
                    solution[step+1][d.end.name-1][new_key]=new_solution
    final=solution[DAY_NUM][DESTINATION]
    final_pts=[]
    final_pt=None
    max_finals=[]
    max_final=0
    for key in final:
        water,food=revertKey(key)
        if water<0 or food<0:
            continue
        max_finals.append(water*WATER_PRICE*0.5+food*FOOD_PRICE*0.5+final[key].money)
        final_pts.append(final[key])
    for index,value in enumerate(max_finals):
        if value>=max_final:
            max_final=value
            final_pt=final_pts[index]
    with open('output.csv','a') as f:
        f.write(str([init_water,init_food,max_final]).replace('[','').replace(']','')+'\n')
    if not all_path:
        return final_pt,max_final
    else:
        return final_pt,max_final,final_pts,max_finals

def dp_all(problem_no):
    # 多重搜索+动态规划 求解第一关和第二关
    loadEnvir(problem_no)
    global_max=0
    final_pt=None
    max_ij=[0,0]
    for p in range(0,int(MAX_BURDEN/WATER_WEIGHT)):
        for q in range(0,int(MAX_BURDEN/FOOD_WEIGHT)):
            if p*WATER_WEIGHT+q*FOOD_WEIGHT>MAX_BURDEN:
                continue
            final,max_final=dp_main(p,q)
            if max_final>global_max:
                global_max=max_final
                final_pt=final
                max_ij=[p,q]
    while final_pt!=None:
        print(final_pt.step,final_pt.pt_index,final_pt.money,final_pt.key)
        final_pt=final_pt.prev
    print(max_ij,global_max)

def dp_game(risk):
    # 多重静态博弈 求解第六关
    water=[200,200,200]
    food=[300,300,300]
    player_pt=[0,0,0]
    money=[6000,6000,6000]
    path=[[],[],[]]
    death=[False,False,False]
    global MINING
    global WATER_ADD
    global FOOD_ADD
    global MONEY_REDUCE
    global WEATHER
    for step in range(0,30):
        next_state=[None,None,None]
        MINING=0
        WATER_ADD,FOOD_ADD,MONEY_REDUCE={},{},{}
        for p in range(0,3):
            if death[p]:
                continue
            final_pt,max_final=dp_main(water[p],food[p],step,player_pt[p],money[p])
            while final_pt!=None:
                # print(final_pt.step,final_pt.pt_index,final_pt.money,final_pt.key)
                if final_pt.step==step+1:
                    next_state[p]=final_pt
                    break
                final_pt=final_pt.prev
            if next_state[p]==None:
                death[p]=True
                money[p]=0
                continue
            if next_state[p].money>money[p]:
                MINING=MINING+1
        for i in range(POINT_NUM):
            POINTS[i].players=0
            for j in range(POINT_NUM):
                MOVE_PLAN[i][j]=0
        for p in range(0,3):
            if death[p]:
                continue
            next_pt_index=next_state[p].pt_index
            POINTS[next_pt_index].players=POINTS[next_pt_index].players+1
            MOVE_PLAN[player_pt[p]][next_pt_index]=MOVE_PLAN[player_pt[p]][next_pt_index]+1
        for p in range(0,3):
            if death[p]:
                continue
            final_pt,max_final,final_pts,max_finals=dp_main(water[p],food[p],step,player_pt[p],money[p],all_path=True)
            best_plan,good_plan=None,None
            while final_pt!=None:
                if final_pt.step==step+1:
                    best_plan=final_pt
                    break
                final_pt=final_pt.prev
            if best_plan==None:
                death[p]=True
                money[p]=0
                continue
            conflict=False
            for other in range(0,3):
                if p==other:
                    continue
                if death[other]:
                    continue
                if best_plan.pt_index==next_state[other].pt_index:
                    conflict=True
            if  conflict:
                if random()<risk[p]:
                    _water1,_food1=revertKey(best_plan.key)
                    _water2,_food2=revertKey(best_plan.prev.key)
                    water[p]=water[p]+_water1-_water2
                    food[p]=food[p]+_food1-_food2
                    if best_plan.pt_index in WATER_ADD:
                        water[p]=water[p]+WATER_ADD[best_plan.pt_index]
                    if best_plan.pt_index in FOOD_ADD:
                        food[p]=food[p]+FOOD_ADD[best_plan.pt_index]                    
                    money[p]=money[p]+best_plan.money-best_plan.prev.money
                    if best_plan.pt_index in MONEY_REDUCE:
                        money[p]=money[p]-MONEY_REDUCE[best_plan.pt_index]
                    player_pt[p]=best_plan.pt_index
                    path[p].append(best_plan.pt_index+1)
                else:
                    good_max=0
                    for index,plan in enumerate(final_pts):
                        while plan!=None:
                            if plan.step==step+1:
                                if plan.pt_index!=best_plan.pt_index:
                                    if max_finals[index]>good_max:
                                        good_max=max_finals[index]
                                        good_plan=plan
                                break
                            plan=plan.prev
                    if good_plan==None:
                        good_plan=best_plan
                    _water1,_food1=revertKey(good_plan.key)
                    _water2,_food2=revertKey(good_plan.prev.key)
                    water[p]=water[p]+_water1-_water2
                    food[p]=food[p]+_food1-_food2
                    if good_plan.pt_index in WATER_ADD:
                        water[p]=water[p]+WATER_ADD[good_plan.pt_index]
                    if good_plan.pt_index in FOOD_ADD:
                        food[p]=food[p]+FOOD_ADD[good_plan.pt_index]
                    money[p]=money[p]+good_plan.money-good_plan.prev.money
                    if good_plan.pt_index in MONEY_REDUCE:
                        money[p]=money[p]-MONEY_REDUCE[good_plan.pt_index]
                    player_pt[p]=good_plan.pt_index
                    path[p].append(good_plan.pt_index+1)
            else:
                _water1,_food1=revertKey(best_plan.key)
                _water2,_food2=revertKey(best_plan.prev.key)
                water[p]=water[p]+_water1-_water2
                food[p]=food[p]+_food1-_food2
                if best_plan.pt_index in WATER_ADD:
                    water[p]=water[p]+WATER_ADD[best_plan.pt_index]
                if best_plan.pt_index in FOOD_ADD:
                    food[p]=food[p]+FOOD_ADD[best_plan.pt_index]
                money[p]=money[p]+best_plan.money-best_plan.prev.money
                if best_plan.pt_index in MONEY_REDUCE:
                    money[p]=money[p]-MONEY_REDUCE[best_plan.pt_index]
                player_pt[p]=best_plan.pt_index
                path[p].append(best_plan.pt_index+1)
        print(path,money)
    with open('game.csv','a') as f:
        f.write(str([risk[0],risk[1],risk[2],money[0],money[1],money[2]]).replace('[','').replace(']','')+'\n')
    with open('path.csv','a') as f:
        f.write(str(path)+'\n')
    with open('weather.csv','a') as f:
        f.write(str(WEATHER).replace('[','').replace(']','')+'\n')

def dp_game_all():
    loadEnvir(6)
    global WEATHER
    global DAY_NUM
    for i in range(1000):
        WEATHER=[]
        for i in range(DAY_NUM):
            rd=random()
            if rd<0.1:
                WEATHER.append('沙暴')
            elif rd<0.55:
                WEATHER.append('晴朗')
            else:
                WEATHER.append('高温')
        risk=[random(),random(),random()]
        print(risk)
        dp_game(risk)


if __name__ == "__main__":
    dp_all(2) # 第一关、第二关求解
    dp_game_all() # 第六关求解
            