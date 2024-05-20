import numpy as np
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import math, pylab, matplotlib, numpy
import csv

PI = 3.141592653


def lentoAngle(armLen, dist):
    return math.asin(dist / 2 / armLen)


def calanglerange(strarm, armLen, min, max):
    print(strarm + ' R movment range is %f° Distance is %fmm' % (
        (lentoAngle(armLen, max) * 180.0 / PI) - (lentoAngle(armLen, min) * 180.0 / PI), max - min))
    return (lentoAngle(armLen, max) * 180.0 / PI) - (lentoAngle(armLen, min) * 180.0 / PI)


def vtow(armLen, theta, V):
    return math.asin(V / armLen / 2) / PI * 180.0


if __name__ == '__main__':

    calanglerange('sankyo', 145, -170, 250)

    calanglerange('HWIN', 135, -260, 260)

    calanglerange('RND', 160, -268, 305)

    print(vtow(174, 90, 300))

    print(305 / 2 / math.cos(30.0 / 180.0 * PI))

    with open('F:/00_software/02_Python/IL1000Data/2023_0302_173722_760/MergDat_230307_203202.csv') as f:

        ##########################################################################
        f_csv = csv.reader(f)
        headers = next(f_csv)
        ##########################################################################
        distData = []
        for i, rows in enumerate(f_csv):
            distData = np.append(distData, [float(rows[1])])


    # 根据均值、标准差,求指定范围的正态分布概率值
    def normfun(x, mu, sigma):
        pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
        return pdf


    result = np.random.randint(-65, 80, size=100) # 最小值,最大值,数量
    result = np.random.normal(15, 44, 100)  # 均值为0.5,方差为1
    print(type(result))


    result = distData - distData.mean()
    print(distData.mean())
    print(max(result))
    x = np.arange(min(result), max(result), 0.01)
    # 设定 y 轴，载入刚才的正态分布函数
    print(result.mean(), result.std())
    y = normfun(x, result.mean(), result.std())
    plt.plot(x, y)  # 这里画出理论的正态分布概率曲线

    # 这里画出实际的参数概率与取值关系
    plt.hist(result, bins=2000, rwidth=1, density=True)  # bins个柱状图,宽度是rwidth(0~1),=1没有缝隙
    plt.title('distribution')
    plt.xlabel('distance')
    plt.ylabel('probability')
    # 输出
    plt.show()  # 最后图片的概率和不为1是因为正态分布是从负无穷到正无穷,这里指截取了数据最小值到最大值的分布
