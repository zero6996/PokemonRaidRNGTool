## PokemonRaidRNGTool

> 使用PySide2编写的图形化RaidRNG工具


### 使用步骤说明 :bookmark_tabs:
#### :one:安装Python3.7

Python[环境搭建](https://www.runoob.com/python/python-install.html)

#### :two:使用pip安装z3求解器包

```bash
pip install z3-solver -i https://pypi.douban.com/simple/
```

#### :three:进入文件夹，运行`RaidToolApp.py`

- 打开CMD，输入`python RaidToolApp.py`即可


> 如果想不显示命令行窗口，可使用`pythonw RaidToolApp.py`命令

#### :four:填写内容

输入PID、EC、Ivs等内容，点击计算即可。



### 后续优化

使用Pyinstaller将工具制作为exe文件。

#### 1. 遇到问题

打包后exe文件无法运行，提示：`Failed to execute script RaidToolApp`

查看日志发现错误：`z3types.Z3Exception:libz3.dll not found.`

问题暂未解决。2019.12.25

#### 2. 替代方法

使用批处理文件运行python代码，见`shortcut.bat`文件，右键编辑，修改内容如下：

1. 将第二行`D:`修改为你的RaidTool文件夹盘符。
2. 将第三行`cd D:\xxxx`修改为你的RaidTool文件夹位置。

保存退出，双击运行即可。



[该工具原文地址](https://www.bilibili.com/read/cv4157878)，计算部分代码均来自该文章，本人仅完成QT界面设计和相关代码编写。