# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from PySide2 import QtWidgets, QtCore, QtGui
import pz_config as pz_config


class PzMessageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PzMessageWidget, self).__init__(parent)
        self.messages = u""


        layout = QtWidgets.QVBoxLayout()
        self.table = QtWidgets.QTableWidget()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        close_btn = QtWidgets.QPushButton()
        self.log_btn = QtWidgets.QPushButton()

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(close_btn)
        hlayout.addWidget(self.log_btn)
        hlayout.setSpacing(2)

        layout.addLayout(hlayout)

        close_btn.clicked.connect(self.close)
        close_btn.setText(u"閉じる")
        self.log_btn.setText(u"ログ")
        self.log_btn.setMaximumWidth(100)
        self.log_btn.clicked.connect(self.log_btn_clicked)
        self.log_btn.setEnabled(False)
        self.setLayout(layout)

        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 20)

    def set_messages(self, datas):
        for data in datas:

            # label.setFlat(True)
            if isinstance(data, list):
                r = self.table.rowCount()
                self.table.setRowCount(r + 1)
                label = QtWidgets.QLabel()
                self.messages += u"[{}]\ndescription: {}\n".format(data[1], data[2])
                if data[0]:
                    label.setText("o")
                    self.messages += u"処理しました\n\n"
                else:
                    label.setText("x")
                    self.messages += u"失敗しました\n\n"
                
                self.messages += u"詳細\n{}\n\n\n\n".format(data[4])

                self.table.setCellWidget(r, 0, label)
                self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(data[2]))
            else:
                self.messages += u"プロセスを中止しました\n\n\n\n"


        self.log_btn.setEnabled(True)

    def log_btn_clicked(self):
        log_path = "{}/puzzle/message.log".format(os.environ["TEMP"])
        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))

        tx = open(log_path, "w")
        tx.write(self.messages.encode("Cp932"))
        tx.close()

        subprocess.Popen(log_path.replace("/", "\\"), shell=True)




class PzStdOutWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PzStdOutWidget, self).__init__(parent)
        layout  = QtWidgets.QVBoxLayout()
        self.text_editor = QtWidgets.QTextEdit()
        layout.addWidget(self.text_editor)
        self.setLayout(layout)
 
        self.cursor = self.text_editor.textCursor()
        self.text_editor.setReadOnly(True)
        self.text_editor.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.process = QtCore.QProcess()
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.output)
        self.process.finished.connect(self.process_finished)

        self.close_button = QtWidgets.QPushButton()
        self.close_button.setText(u"閉じる")
        self.close_button.setEnabled(False)
        layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)
        
    def start_process(self, cmd=None, extra_environs={}, done=None):
        done_path = done
        env = QtCore.QProcessEnvironment.systemEnvironment()
        for k, v in extra_environs.items():
            env.insert(k, "{}".format(v))
        self.process.setProcessEnvironment(env)
        self.process.start(cmd, QtCore.QIODevice.ReadWrite)
 
    def output(self):
        def _add_line(line):
            self.cursor.movePosition(QtGui.QTextCursor.End)
            self.cursor.insertText(line)
            self.cursor.insertBlock()

        read_data = self.process.readAllStandardOutput().data()
        _add_line(str(read_data).replace("\r\n", "\n"))
 
    def process_finished(self):
        self.cursor.insertText("finished...")
        x = PzMessageWidget(self)
        done_path = "{}/puzzle/message.json".format(os.environ["TEMP"])
        info, data = pz_config.read(done_path)
        print 11111111111, info
        print 22222222222, data, done_path
        if data:
            x.set_messages(data["messages"])
        x.show()
        self.close_button.setEnabled(True)

    def error_occurred(self):
        print "error----------------"

if __name__ == '__main__':
    def stdout__TEST():
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForLocale())
        widget = PzStdOutWidget()
        cmd = "E:/daily/20191107/test.bat"
        cmd = r"K:/staff/hattori/KbnToolBox/python/KbnLib/site-packages/python27/puzzle/test/data/test.bat"
        widget.start_process(cmd)
        widget.show()
        sys.exit(app.exec_())

    def messagebox__TEST():
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForLocale())
        widget = PzMessageWidget()
        info, data = pz_config.read("C:/Users/Hattori/AppData/Local/Temp/puzzle/message.json")
        widget.set_messages(data["messages"])
        widget.show()
        sys.exit(app.exec_())

    messagebox__TEST()
