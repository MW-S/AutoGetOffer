# initUI.py
import sys,  re, os, subprocess
from PyQt5 import QtWidgets
# 定义槽函数来打开文件夹选择对话框
from UI.MyMainWindow import MyMainWindow
from AutoFindWork import sendResumeByKeyword

def is_url(s):
    # 正则表达式匹配网址
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return bool(pattern.match(s))


def is_empty(s):
    return not bool(s.strip())


def startChrome():
    current_directory = os.getcwd()
    print(current_directory)
    # 指定bat文件的路径
    bat_file_path = f'{current_directory}/startChromeDebug.bat'
    # 执行bat文件
    os.system(f'start cmd /k "{bat_file_path}"')


def startFindOffer(ui):
    try:
        keywordLst=ui.getKeywordLst()
        acquireTags=ui.getWorkLifeLst()
        addressTags=ui.getWorkAddressLst()
        count=ui.spinBox.value()
        print(keywordLst, acquireTags, addressTags, count)
        sendResumeByKeyword(keywordLst, acquireTags, addressTags, count, True)
    except Exception as e:
        print(f"except:{e}")


def run():
    try:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = MyMainWindow()
        ui.setupUi(MainWindow)
        ui.pushButton.clicked.connect(startChrome)
        ui.executeButton.clicked.connect(lambda: startFindOffer(ui))
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"except:{e}")
    finally:
        print("final print")




