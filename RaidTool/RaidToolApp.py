from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableWidgetItem, QTableWidget
from G8RNG import XOROSHIRO,Raid
from Pokemon import CalcDataString

class RaidToolApp:
    def __init__(self):
        # 从文件中加载UI定义
        qfile_stats = QFile("ui/raidtool.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象,里面的控件对象也成为窗口对象的属性了
        self.window = QUiLoader().load(qfile_stats)
        # 为 '开始计算'按钮绑定计算函数
        self.window.calc_btn.clicked.connect(self.calc)

    # 计算函数
    def calc(self):
        """
            获取文本框输入的内容,设置一些初始值
        """
        # 将字符串转换为十六进制
        table = self.window.showlayer
        # 设置单元格内容不可编辑
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        # 设置根据内容自动调整单元格大小，不满意，会导致内容缩小
        # table.resizeColumnsToContents()
        # table.resizeRowsToContents()

        # 设置表格行数
        table.setRowCount(1)
        try:
            PID = eval(self.window.pid_edit.text())
            EC = eval(self.window.ec_edit.text())

            IVs = []
            # 将字符串转换为list数组
            [IVs.append(int(iv)) for iv in self.window.ivs_edit.text().split(',')]
            MaxResults = int(self.window.maxresult_edit.text())
            usefilters = True if self.window.usefilter_box.currentText() == '是' else False
        except BaseException as e:
            # 合并单元格操作
            table.setSpan(0, 0, 1, 3)
            table.setItem(0, 0, QTableWidgetItem("输入内容不能为空！请核对后在输入"))

        # 获取一些设置值
        flawlessivNumber = 4 if self.window.flawlessiv_Box.currentText() == '4' else 5
        HANumber = 1 if self.window.ha_box.currentText() == '梦特' else 0
        useRandomGender = 1 if self.window.gender_box.currentText() == '是' else 0

        # 定义一些预期的IVs
        V6 = [31, 31, 31, 31, 31, 31]
        S0 = [31, 31, 31, 31, 31, 00]
        A0 = [31, 00, 31, 31, 31, 31]

        # 查找种子
        results = Raid.getseeds(EC, PID,IVs)

        # 如果没有查询到种子，打印
        if len(results) == 0:
            # 合并单元格
            table.setSpan(0, 0, 1, 3)
            table.setItem(0, 0, QTableWidgetItem("没有查询到种子！请核对PID、EC、IVS"))
            print("No raid seed")
        else:
            for result in results:
                if result[1] > 0:
                    print(f"seed = 0x{result[0]:016X}\nPerfect IVs:{result[1]}")
                    r = Raid(result[0], flawlessiv=result[1], HA=0, RandomGender=1)
                    r.print()
                else:
                    print(f"seed = 0x{result[0]:016X}\n(Shiny locked!) Perfect IVs:{-result[1]}")
                    r = Raid(result[0], flawlessiv=-result[1], HA=1, RandomGender=1)
                    r.print()

        # 计算帧数
        if len(results) > 0:
            print(f"\n\nResults:")
            seed = results[0][0]
            # 存放计算结果的数组
            self.RNGData = []
            i = 0
            while i < MaxResults:
                r = Raid(seed, flawlessiv = flawlessivNumber, HA = HANumber, RandomGender = useRandomGender)
                seed = XOROSHIRO(seed).next()
                if usefilters:
                    if r.ShinyType != 'None':
                        # print(i)
                        data = r.print()
                        data[0]['Frame'] = str(i)
                        self.RNGData.append(data)
                else:
                    data = r.print()
                    data[0]['Frame'] = str(i)
                    self.RNGData.append(data)
                i += 1
            # 打印计算结果
            print(self.RNGData)
            self.insertData()

    def insertData(self):
        table = self.window.showlayer
        dataLength = len(self.RNGData)
        # 清除单元格内容
        table.clearContents()
        # 清除单元格合并操作
        table.clearSpans()
        # 设置单元格数量
        table.setRowCount(dataLength)
        print(dataLength)
        # 获取计算数据的字符串列表
        calcDataStr = CalcDataString.CalcData
        # 遍历data，将数据插入到表格中
        for row,data in enumerate(self.RNGData):
            # QTableWidgetItem表示一个单元格，且只接受字符串类型数据
            for i in range(0,len(calcDataStr)):
                table.setItem(row, i, QTableWidgetItem(data[0][calcDataStr[i]]))


app = QApplication([])
raidtoolapp = RaidToolApp()
raidtoolapp.window.show()
app.exec_()