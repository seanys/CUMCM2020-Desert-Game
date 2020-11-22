from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter,FuncFormatter
import seaborn as sns
import numpy as np
from random import random
from scipy import interpolate

def getKey(water, food):
    return str(water).zfill(4)+str(food).zfill(4)

def getZ(money, water, food):
    z = np.zeros(water.shape)
    for i in range(len(water)):
        for j in range(len(water[i])):
            if getKey(water[i][j], food[i][j]) not in money.keys():
                z[i][j] = 0
                continue
            z[i][j] = money[getKey(water[i][j], food[i][j])]
            # print(water[i][j],food[i][j],z[i][j])
    return z

def illustrate(problem_no):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    init_water = []
    init_food = []
    money = {}

    with open('problem/problem{}_global.csv'.format(problem_no), 'r') as f:
        for line in f.readlines():
            value = line.replace(' ', '').replace('\n', '').split(',')
            key = getKey(int(value[0]), int(value[1]))
            money[key] = int(float(value[2]))
            if int(value[0]) not in init_water:
                init_water.append(int(value[0]))
            if int(value[1]) not in init_food:
                init_food.append(int(value[1]))

    X, Y = np.meshgrid(init_water, init_food)
    Z = getZ(money, X, Y)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def fair_game():
    stretegy=[0,0]
    benefit1=[[9070,9425,9325],[9535,8850,9325],[9535,9425,8515]]
    benefit2=[[9070,9535,9535],[9425,8850,9425],[9325,9325,8515]]

    win=0
    lose=0
    total1=0
    total2=0
    X=[]
    Y=[]
    for i in range(1,5001):
        for player in range(0,2):
            rd=random()
            if rd<0.609:
                stretegy[player]=0
            elif rd<0.91:
                stretegy[player]=1
            else:
                stretegy[player]=2

        money1=benefit1[stretegy[0]][stretegy[1]]
        money2=benefit2[stretegy[0]][stretegy[1]]

        if money1>=money2:
            win=win+1
        if money1<=money2:
            lose=lose+1

        total1=total1+money1
        total2=total2+money2
        X.append(i)
        Y.append(total1/(total1+total2))

    sns.set(style="darkgrid")
    print(win,lose,total1,total2)
    sns.lineplot(X,Y)
    plt.show()    

def game_sim():
    winners=[0,0,0]
    death=[]
    with open('game.csv','r') as f:
        for line in f.readlines():
            line=line.replace('\n','').split(',')
            risk=[float(line[0]),float(line[1]),float(line[2])]
            money=[float(line[3]),float(line[4]),float(line[5])]                   
            money_rank=np.argsort(money)
            risk_rank=np.argsort(np.argsort(risk))
            winner=money_rank[2]
            winners[risk_rank[winner]]=winners[risk_rank[winner]]+1
            for i in range(0,3):
                if money[i]<1:
                    death.append(risk[i])
            print(winner,risk[winner],risk_rank[winner])
    print(winners)
    for i in range(len(death)):
        death[i]=death[i]*100
    death=death*10
    sns.set(style="darkgrid")
    sns.distplot(death)
    def to_percent(temp, position):
        return '%1.2f'%(0.01*temp)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
    plt.show()

illustrate(1) # 第一关，第二关全局最优策略绘图
fair_game() # 博弈胜率绘图
game_sim() # 第六关仿真数据分析
