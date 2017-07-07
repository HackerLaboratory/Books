这里对Python科学计算生态系统和库进行简单介绍

## Numpy

Numpy(Numerical Python的简称)是Python科学计算的基础包。它提供以下功能：

* 快速高效的多维数组对象ndarray
* 用于对数组执行元素级运算以及直接对数组执行数学运算的函数
* 用于读写硬盘上基于数组的数据集的工具
* 线性代数运算、傅立叶变换，以及随机数生成
* 用于将C、C++、Fortran代码集成到Python的工具

除了为Python提供快速的数组处理能力，Numpy在数据分析方面还有另外一个主要作用，即作为在算法之间传递数据的容器。对于数值型数据，Numpy数组在存储和处理数据时要比内置的Python数据结构要高效的多

此外，有低级语言（比如C、Fortran）编写的库可以直接操作Numpy数组中的数据，无需进行任何数据复制工作

## pandas

pandas提供了使我们能够快速便捷地处理结构化数据的大量数据结构和函数。你很快就会发现，它是使Python成为强大而高效的数据分析环境的重要原因之一。《Python for Data Analysis》用到最多的pandas对象就是DataFrame，它是一个面向列的二维表结构，且含有行标和列标：

```
>>> frame
    total_bill     tip      sex      smoker     day    timesize
1   16.99          1.01     Female   No         Sun    Dinner  2
2   10.34          1.66     Male     No         Sun    Dinner  3
3   11.23          1.23     Male     Yes        Sun    Dinner  2

```

pandas兼具Numpy高性能的数组计算功能以及电子表格和关系型数据库灵活的数据处理功能。它提供了复杂精细的索引功能，以便更为便捷地完成重塑、切片和切块、聚合以及选取数据子集等操作。pandas将是一个很重要的数据分析工具

对于金融行业的用户，pandas提供了大量适用于金融数据的高性能时间序列功能和工具

对于使用R语言进行统计计算的用户，肯定不会对DataFrame这个名字感到陌生，因为它源自于R的data.frame对象。但是这两个对象并不相同。R的data.frame对象所提供的功能只是Dataframe对象所提供功能的一个子集。可以经常拿Python和R进行对比，毕竟R是最流行的开源数据分析环境

pandas这个名字源自于panel data（面板数据，这是计量经济学中关于多维结构化数据集的一个术语）以及Python data analysis（Python数据分析）

## matplotlib

matplotlib是最流行的用于绘制数据图表的Python库。它最初由John D. Hunter创建，目前由一个庞大的开发人员团队维护。它非常适合创建出版物上用的图表

它跟IPython结合的很好，因而提供了一种非常好用的交互式数据绘图环境。绘制的图表也是交互式的，你可以利用绘图窗口中的工具栏放大图表中的某个区域或对整个图表进行调整

## IPython

IPython是Python科学计算标准工具集的组成部分，它将其他所有的东西联系到了一起。它为交互式和探索式计算提供了一个强健而高效的环境。它是一个增强式的Python Shell，目的是提高编写、测试、调试Python代码的速度。它主要用于交互式数据处理和利用matplotlib对数据进行可视化处理

除了标准的基于终端的IPython Shell外，该项目还提供了：

* 一个类似于Mathematica的HTML笔记本（通过Web浏览器连接IPython）
* 一个基于Qt框架的GUI控制台，其中包含有绘图、多行编辑以及语法高亮显示等功能
* 用于交互式并行和分布式计算的基础框架

## SciPy

Scipy是一组专门解决科学计算中各种标准问题域的包的集合，主要包括下面的包：

* scipy.integrate：数值积分例程和微分方程求解器
* scipy.linalg：扩展了由numpy.linalg提供的线性代数例程河矩阵分解功能
* scipy.optimize：函数优化器（最小化器）以及根查找算法
* scipy.sginal：信号处理工具
* scipy.sparse：稀疏矩阵和稀疏线性系统求解器
* scipy.special：SPECFUN（这是一个实现了许多常用数学函数，比如伽马函数的Fortran库）的包装器
* scipy.stats：标准连续喝离散概率分布（如密度函数、采样器、连续分布函数等）、各种统计校验方法，以及更好的描述统计法
* scipy.weave：利用內联C++代码加速数组计算的工具

NumPy和Scipy的有机结合完全可以替代MATLAB的计算功能

