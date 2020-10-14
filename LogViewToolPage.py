from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
from LogFind import logFind
import xlwt
import os


class LogViewTool(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resource\\UI\\LogViewTool.ui")

        # 选择多选
        # self.ui.list_conditions.setSelectionMode(
        #    QAbstractItemView.ExtendedSelection)
        self.ui.list_conditions.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        self.ui.tableCentent.horizontalHeader().setStretchLastSection(True)
        # 宽列自动分配
        self.ui.tableCentent.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 宽列手动调整
        self.ui.tableCentent.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.ui.tableCentent.setColumnWidth(0, 200)

        self.ui.btn_add.clicked.connect(self.addContent)
        self.ui.btn_delete.clicked.connect(self.deleContent)
        self.ui.btn_clear.clicked.connect(self.clearContent)
        self.ui.btn_open.clicked.connect(self.openLog)
        self.ui.btn_export.clicked.connect(self.excelExport)

        file = open('temp.txt')
        while True:
            text = file.readline()
            text = text.strip('\n')
            self.ui.list_conditions.addItem(text)
            print(text)
            if not text:
                break
        file.close()

    def addContent(self):
        text = self.ui.lineEdit.text()
        self.ui.list_conditions.addItem(text)
        self.ui.lineEdit.clear()

        file_txt = 'temp.txt'
        with open(file_txt, "a") as file:
            file.write(text + "\n")

    def deleContent(self):
        list_id = self.ui.list_conditions.currentRow()
        dele_text = self.ui.list_conditions.currentItem().text()
        print(list_id)
        print(dele_text)
        self.ui.list_conditions.takeItem(list_id)

        with open("temp.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("temp.txt", "w", encoding="utf-8") as f_w:
            for line in lines:
                if dele_text in line:
                    continue
                f_w.write(line)

    def clearContent(self):
        self.ui.list_conditions.clear()
        with open("temp.txt", 'w') as f:
            f.truncate()

    def openLog(self):
        list_find = []
        filePath, _ = QFileDialog.getOpenFileName(
            self.ui,             # 父窗口对象
            "选择要打开的日志",  # 标题
            r".",        # 起始目录
            "日志类型 (*.log *.log*)"  # 选择类型过滤项，过滤内容在括号中
        )
        print('打开日志的路径：%s' % filePath)
        str_query = self.ui.list_conditions.currentItem().text()
        print('选择查询条件：%s' % str_query)

        items = logFind(filePath, str_query)

        print(items)
        #items = [['燕十三','21','Male','武林大侠','11','1'],['萧十一郎','21','Male','武功好','1','1']]

        for i in range(len(items)):
            item = items[i]
            row = self.ui.tableCentent.rowCount()
            self.ui.tableCentent.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.ui.tableCentent.setItem(row, j, item)

    def excelExport(self):
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        print('保存路径：%s' % filePath)

        # 保存excel
        xl = xlwt.Workbook(encoding='utf-8')
        sheet = xl.add_sheet('日志数据统计', cell_overwrite_ok=True)

        rows = self.ui.tableCentent.rowCount()

        for i in range(rows):
            save_list = []
            for j in range(7):
                try:
                    data = self.ui.tableCentent.item(i, j).text()
                    save_list.append(data)
                except:
                    data = ''
                    save_list.append(data)
                sheet.write(i, j, save_list[j])

        xl.save(filePath+'/log_save.xls')

#app = QApplication([])
#window = LogViewTool()
# window.ui.show()
# app.exec_()
