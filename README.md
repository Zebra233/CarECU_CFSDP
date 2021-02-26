# CarECU_CFSDP
利用基于峰值密度的聚类算法对车辆ECU数据进行聚类分析

## 算法
利用密度与最近高密度点的距离来帮助判断是否为聚类的中心,
在确定聚类中心后,各个点一直找其最近高密度点,直到为聚类中心.
这样就可以确定各个点属于哪个聚类

## 主要过程
1. 计算距离,密度和最近的高密度点
2. 通过决策图找出有几个聚类中心,再确定聚类中心
3. 确定聚类中心后,找到各个点所属聚类

## 部分结果图
![](https://raw.githubusercontent.com/Zebra233/pic_bed/master/20210226171811.png)
![](https://raw.githubusercontent.com/Zebra233/pic_bed/master/20210226171919.png)
