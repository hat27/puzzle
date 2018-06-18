#-*- coding: utf8 -*-

import os
import sys

import datetime
import subprocess

from puzzle.Piece import Piece
import puzzle.pz_env as pz_env

_PIECE_NAME_ = "PzEndDialog"

os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(["PySide", "PySide2", "PyQt4"])

from Qt import QtWidgets, QtCore, QtGui


class PzDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, messages=[]):
        super(PzDialog, self).__init__(parent)
        self.header_list = ["check", "header"]
        self.header_dict = {"check": {"width": 20}}
        self.messages = messages
        self.details = []
        self.close_btn = None
        self.detail_btn = None
        self.widget = None

    def set_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.widget = QtWidgets.QTableWidget()
        self.widget.horizontalHeader().setStretchLastSection(True)
        self.widget.verticalHeader().setDefaultSectionSize(20)
        self.widget.horizontalHeader().setVisible(False)
        self.widget.verticalHeader().setVisible(False)
        self.widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.widget.setAlternatingRowColors(True)
        h_layout = QtWidgets.QHBoxLayout()
        self.close_btn = QtWidgets.QPushButton()
        self.close_btn.setText("close")
        self.detail_btn = QtWidgets.QPushButton()
        self.detail_btn.setText("detail")
        h_layout.addWidget(self.detail_btn)
        h_layout.addWidget(self.close_btn)

        layout.addWidget(self.widget)
        layout.addLayout(h_layout)
        self.setLayout(layout)
        self.set_table()
        self.append_table(self.messages)

        self.detail_btn.clicked.connect(self.detail_btn_clicked)
        self.close_btn.clicked.connect(self.close_btn_clicked)

        stylesheet = """
                            QDialog{background-color: rgb(40, 40, 70)}
                            QTableWidget{background-color: rgb(60, 60, 110); 
                                                    color: rgb(220, 220, 255);
                                                    alternate-background-color: rgb(80, 80, 150)}
                            """
        self.close_btn.setStyleSheet("""
                                                    QPushButton::hover{background-color: rgb(250, 250, 100)}
                                                    QPushButton{border-style: solid; 
                                                                          background-color: rgb(175, 175, 60); 
                                                                          height: 20px};
                                                    """)
        self.detail_btn.setStyleSheet("""
                                                    QPushButton::hover{background-color: rgb(250, 250, 100)}
                                                    QPushButton{border-style: solid; 
                                                                          background-color: rgb(175, 175, 60); 
                                                                          height: 20px};
                                                    """)
        self.setStyleSheet(stylesheet)

        self.show()

    def detail_btn_clicked(self):
        tme = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        path = "{}/{}.txt".format(pz_env.get_temp_directory("log"), tme)
        tx = open(path, "w")
        tx.write("\n".join(self.details))
        tx.close()

        subprocess.Popen(path, shell=True)

    def close_btn_clicked(self):
        self.close()

    def set_table(self):
        self.widget.setColumnCount(len(self.header_list))
        for c, column in enumerate(self.header_list):
            if column in self.header_dict:
                if "width" in self.header_dict[column]:
                    self.widget.setColumnWidth(c, self.header_dict[column]["width"])

    def get_table_list(self, name):
        return self.header_list.index(name)

    def append_table(self, messages):
        for message in messages:
            flg, job_name, desctiption, header, detail = message

            r = self.widget.rowCount()
            self.widget.setRowCount(r+1)
            root = os.environ.get("__PUZZLE_PATH__", "..")
            if flg:
                path = "{}/puzzle/pieces/app/PzEndDialog/icon/ok.png".format(root)
            else:
                path = "{}/puzzle/pieces/app/PzEndDialog/icon/error.png".format(root)
                header = desctiption

            icon_label = QtWidgets.QLabel()
            icon_label.setPixmap(QtGui.QPixmap(path))
            icon_label.setScaledContents(True)
            if job_name:
                self.details.append(job_name.encode("shift_jis"))
            if desctiption:
                self.details.append(desctiption.encode("shift_jis"))
            if header:
                self.details.append(header.encode("shift_jis"))
            if detail:
                self.details.append(detail.encode("shift_jis"))

            self.details.append("")

            self.widget.setCellWidget(r, self.get_table_list("check"), icon_label)
            self.widget.setItem(r, self.get_table_list("header"),
                                              QtWidgets.QTableWidgetItem(header))


class PzEndDialog(Piece):
    def __init__(self, **args):
        super(PzEndDialog, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        header = ""
        detail = ""

        if "__PUZZLE_STANDALONE_PYTHON__" in os.environ:
            import json
            import subprocess
            py_path = "{}\\puzzle\\pieces\\app\\PzEndDialog.py".format(os.environ["__PUZZLE_PATH__"])
            temp = "{}/puzzle/end_dialog".format(os.environ["TEMP"])
            if not os.path.exists(temp):
                os.makedirs(temp)
            tme = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            temp_file = "{}/log_{}.json".format(temp, tme)
            json.dump(self.pass_data["messages"], open(temp_file, "w"), "utf8", indent=4)

            cmd = u'"{}" "{}" "{}"'.format(os.environ["__PUZZLE_STANDALONE_PYTHON__"],
                                                          py_path, temp_file)

            self.logger.debug("temp_file: {}".format(temp_file))
            self.logger.debug("cmd: {}".format(cmd))
            res = subprocess.Popen(cmd,
                                                  shell=False,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE).communicate()
            print res

        else:
            # TODO:  どんな環境でも立ち上がるようにする
            #app = QtWidgets.QApplication(sys.argv)
            x = PzDialog(messages=self.pass_data["messages"])
            x.set_ui()
            #app.exec_()

        return True, self.pass_data, header, detail

