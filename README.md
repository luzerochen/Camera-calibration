# 作业相机标定实验结果
### 文件结构
- harris.py：该文件为自己用harris算法写的角点检测
- getcorner.py： 调用openCV对棋盘格的角点检测
- parameters.py：调用getcorner文件对棋盘检测后的数据集，计算出单应性矩阵，相机的内参
- changeperspective.py: 自己写的改变图片的视角，变成鸟瞰图
- 文件data：保存getcorner.py文件检测出来的角点坐标以及世界坐标
- 文件chessboard：10张手机拍摄的棋盘图片

### 实验结果
#### harris角点检测
自己写的角点检测对于电脑生成出来无噪点的棋盘格运行较好，对于手机拍摄的照片，结果不好。
手机拍摄的照片，不同的照片需要调整不同的阈值。

- 电脑生成的棋盘格
[![](https://i.loli.net/2019/10/11/Wfgc6aZin3LETHX.png)](https://i.loli.net/2019/10/11/Wfgc6aZin3LETHX.png)
- 手机拍摄的照片，阈值低的棋盘格
[![](https://i.loli.net/2019/10/11/e51aqYgPuQEVUsB.png)](https://i.loli.net/2019/10/11/e51aqYgPuQEVUsB.png)
- 手机拍摄的照片，阈值高的棋盘格
[![](https://i.loli.net/2019/10/11/wRIUViJ71bQkYpt.png)](https://i.loli.net/2019/10/11/wRIUViJ71bQkYpt.png)

#### 相机内参计算结果
- 调用openCV的结果
[![](https://i.loli.net/2019/10/12/9oIVfcFxnO8G2BQ.png)](https://i.loli.net/2019/10/12/9oIVfcFxnO8G2BQ.png)
- 自己计算内参的结果
[![](https://i.loli.net/2019/10/12/L4DrSlYUHBAGbya.png)](https://i.loli.net/2019/10/12/L4DrSlYUHBAGbya.png)

#### 改变视角结果
- 不改变视角的原来照片
![69S`IF}L0D_{XIRW~KIBL@7.png](https://i.loli.net/2019/10/12/SqMxkH5TOF7gn8r.png)
- 改变视角后的照片
[![](https://i.loli.net/2019/10/12/9FpVKOfRSx2ZqwN.png)](https://i.loli.net/2019/10/12/9FpVKOfRSx2ZqwN.png)
