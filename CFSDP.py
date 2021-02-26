import numpy as np
import matplotlib.pyplot as plt
import collections
import pandas as pd


def dist(matrix):
    """
    计算欧式氏距离
    :param matrix:2维数组
    :return: distance[i,j]
    """
    distance = np.zeros(shape=(len(matrix), len(matrix)))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            if j < i:
                distance[i, j] = distance[j, i]
            elif i < j:
                distance[i, j] = np.sqrt(np.sum(np.power(matrix[i] - matrix[j], 2)))
    return distance


def dc(distance, persent):
    """
    按照百分比选出dc--截断距离
    :param distance: 2维距离数组
    :param persent: 截断距离在总距离排名中的百分比
    :return: dc: 截断距离
    """
    temp = []
    for i in range(len(distance[0])):
        for j in range(i + 1, len(distance[0])):
            temp.append(distance[i][j])
    temp.sort()
    dc = temp[int(len(temp) * persent / 100)]
    return dc



def loc_density(distance, dc):
    """
    局部密度(离散型):距离小于dc的点的个数(包括自身)
    :param distance: 点的距离
    :param dc: 截断距离
    :return: loc_density: 局部密度
    """
    loc_density = np.zeros(distance.shape[0])
    for i, j in enumerate(distance):
        loc_density[i] = len(j[j <= dc])
    return loc_density

def continous_density(distance, dc):
    loc_density = np.zeros(distance.shape[0])
    for i, j in enumerate(distance):
        loc_density[i] = np.sum(np.exp(-(j / dc) ** 2))
    return loc_density

def node_info(distance,loc_density):
    """
    1.找出密度大于自己的点集
    2.在该点集中找出离自己最近的点
    3.找出自己和该点的距离,并将该点记为最近的高密度点
    :param distance: 距离
    :param loc_density: 局部密度
    :return: high_den_dis: 高密度点最近距离 high_den_node: 高密度点
    """
    high_den_dis=np.zeros(distance.shape[0])
    high_den_node = np.zeros(distance.shape[0],dtype=np.int)

    for i,node in enumerate(loc_density):
        # 1.点集
        high_den_nodes = np.squeeze(np.argwhere(loc_density > loc_density[i]))
        if high_den_nodes.size == 0:
            #2.3.密度最大的点 距离为最远距离
            high_den_dis[i] = np.max(distance)
            high_den_node[i] = i
        else:
            #2.3.从点集的距离中选出最近的那个点和距离
            high_den_dis[i] = np.min(distance[i][high_den_nodes])
            min_distance_node = np.squeeze(np.argwhere(distance[i][high_den_nodes] == high_den_dis[i]))
            if min_distance_node.size >= 2:
                min_distance_node = np.random.choice(a=min_distance_node)
            if distance[i][high_den_nodes].size > 1:
                high_den_node[i] = high_den_nodes[min_distance_node]
            else:
                high_den_node[i] = high_den_nodes
    return high_den_dis,high_den_node

def show_optionmal(den, det, v):
    """
    画detal图和原始数据图
    :param den:
    :param det:
    :param v:
    :return:
    """
    plt.figure(num=1, figsize=(15, 9))
    ax1 = plt.subplot(121)
    for i in range(len(v)):
        plt.scatter(x=den[i], y=det[i], c='k', marker='o', s=15)
    plt.xlabel('density')
    plt.ylabel('detal')
    plt.title('Chose Leader')
    plt.sca(ax1)

    ax2 = plt.subplot(122)
    for j in range(len(v)):
        plt.scatter(x=v[j, 0], y=v[j, 1], marker='o', c='k', s=8)
    plt.xlabel('axis_x')
    plt.ylabel('axis_y')
    plt.title('Dataset')
    plt.sca(ax2)
    plt.show()

def normalize(high_den_dis,loc_density):
    """
    对高密度最小距离和密度进行归一化处理,减小数量级影响
    :param high_den_dis:
    :param loc_density:
    :return: nor_dis,nor_den
    """
    nor_dis = (high_den_dis - np.min(high_den_dis)) / (np.max(high_den_dis) - np.min(high_den_dis))
    nor_den = (loc_density - np.min(loc_density)) / (np.max(loc_density) - np.min(loc_density))
    return nor_dis,nor_den

def draw_dec(high_den_dis,loc_density):
    """
    画出决策图
    Y:每点的密度*最小距离
    :param high_den_dis:
    :param loc_density:
    :return:
    """
    nor_dis,nor_den = normalize(high_den_dis,loc_density)
    gamma = nor_dis * nor_den
    plt.figure(2,(15,10))
    plt.scatter(x=range(len(high_den_dis)), y=-np.sort(-gamma), c='k', marker='o', s=-np.sort(-gamma) * 100)
    plt.xlabel('num')
    plt.ylabel('gamma')
    plt.title('Decision Graph')
    plt.show()
    return gamma

def ultClassify(high_den_node,cluster_center):
    """
    确定最终分类
    :param high_den_node: 最近高密度点
    :param cluster_center: 被选中的聚类中心
    :return: cluster[i]: i点聚类中心
    """
    for i in range(len(high_den_node)):
            #一直找最近的高密度点,直到该点为被选中的聚类中心
            while high_den_node[i] not in cluster_center:
                temp = high_den_node[i]
                high_den_node[i] = high_den_node[temp]
    cluster = high_den_node[:]
    return cluster

def show_cluster(cluster,matrix,cluser_center):
    colors = [
        '#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#228B22',
        '#0000FF', '#FF1493', '#EE82EE', '#000000', '#FFA500',
        '#00FF00', '#006400', '#00FFFF', '#0000FF', '#FFFACD',
    ]
    # 画最终聚类效果图
    leader_color = {}
    main_leaders = dict(collections.Counter(cluster)).keys()
    for index, i in enumerate(main_leaders):
        leader_color[i] = index
    plt.figure(num=3, figsize=(15, 10))
    for node, class_ in enumerate(cluster):
        #  标出每一类的聚类中心点
        if node in cluser_center:
            plt.scatter(x=matrix[node, 0], y=matrix[node, 1], marker='+', s=100, c='K', alpha=0.8)
        else:
            plt.scatter(x=matrix[node, 0], y=matrix[node, 1], c=colors[leader_color[class_]], s=5, marker='o',
                        alpha=0.66)
    plt.title('The Result Of Cluster')
    plt.show()

def CFSDP(matrix):
    """
    基于密度峰值的聚类分析
    :param matrix:
    :return:
    """
    percent = 3
    distance = dist(matrix) #计算欧氏距离
    dcut = dc(distance, percent) #选择截断距离
    density = continous_density(distance, dcut)   #计算密度
    high_den_dis, high_den_node = node_info(distance,density)   #找出最近高密度点,与其的密度
    show_optionmal(density,high_den_dis,matrix)
    gamma = draw_dec(high_den_dis,density)
    center_num = int(input("请输入中心数量:"))
    cluster_center = np.argsort(-gamma)[:center_num]   #选出聚类的中心
    print("中心:",cluster_center)
    cluster = ultClassify(high_den_node,cluster_center) #最终聚类
    show_cluster(cluster,matrix,cluster_center)

def CFSDP_for_ipynb(url):
    """
    给notebook调用的
    :return:
    """
    print(url)
    ECUnew = pd.read_csv(url)
    matrix = ECUnew.to_numpy()
    CFSDP(matrix)



if __name__ == '__main__':
    ECUnew = pd.read_csv('./data/ECUnew.csv')
    matrix = ECUnew.to_numpy()
    CFSDP(matrix)
    # Compound = r'./data/Compound.txt'
    # raw_data = np.loadtxt(Compound, delimiter='	', usecols=[0, 1])
    # CFSDP(raw_data)

