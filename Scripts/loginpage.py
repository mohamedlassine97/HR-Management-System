# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import QtCore, QtGui, QtWidgets
from sqlite3 import Error
from PIL import Image

from ManagerAbstractClass import ManagerAbstractClass
from HRManager import HRManager

from humanresource import Ui_Dialog as HRpage
# custom

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys
import sqlite3
import os
from PIL import Image

con = sqlite3.connect('../DA/HRDatabase.db')
cur = con.cursor()
defaultImg = "person.png"

picture = "person.png"
logo = "../Image/logo.png"

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(731, 528)
        Login.setMinimumSize(QtCore.QSize(731, 528))
        Login.setMaximumSize(QtCore.QSize(731, 528))
        self.layoutWidget = QtWidgets.QWidget(Login)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 280, 351, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_email = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_email.setObjectName("lbl_email")
        self.gridLayout.addWidget(self.lbl_email, 0, 0, 1, 1)
        self.ln_email = QtWidgets.QLineEdit(self.layoutWidget)
        self.ln_email.setObjectName("ln_email")
        self.gridLayout.addWidget(self.ln_email, 0, 1, 1, 2)
        self.lbl_password = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_password.setObjectName("lbl_password")
        self.gridLayout.addWidget(self.lbl_password, 1, 0, 1, 1)
        self.ln_password = QtWidgets.QLineEdit(self.layoutWidget)
        self.ln_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ln_password.setObjectName("ln_password")
        self.gridLayout.addWidget(self.ln_password, 1, 1, 1, 2)
        self.btn_login = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_login.setObjectName("btn_login")

        # button connect
        self.btn_login.clicked.connect(self.login)

        self.gridLayout.addWidget(self.btn_login, 2, 1, 1, 1)
        self.cmb_dept = QtWidgets.QComboBox(self.layoutWidget)
        self.cmb_dept.setObjectName("cmb_dept")
        self.cmb_dept.addItem("")
        self.cmb_dept.addItem("")
        self.gridLayout.addWidget(self.cmb_dept, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(240, 30, 251, 241))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../Images/logo.png"))
        self.label.setObjectName("label")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)



    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Login"))
        self.lbl_email.setText(_translate("Login", "Email"))
        self.ln_email.setPlaceholderText(_translate("Login", "m@gmail.com"))
        self.lbl_password.setText(_translate("Login", "Password"))
        self.ln_password.setPlaceholderText(_translate("Login", "123456789"))
        self.btn_login.setText(_translate("Login", "Login"))
        self.cmb_dept.setItemText(0, _translate("Login", "HR Dept. Manager"))
        self.cmb_dept.setItemText(1, _translate("Login", "Finance Dept. Manager"))

    def UploadImage(self):
        global  picture
        # size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self,'Upload Image','','Image Files (*.jpg *.png)')
        picture = os.path.basename(self.fileName)
        img = Image.open(self.fileName)
        # img = img.resize(size)
        img.save("images/{}".format(picture))


    def login(self):
        if self.cmb_dept.currentIndex() == 0:
            xx = HRManager()
            xx.email = self.ln_email.text()
            xx.password = self.ln_password.text()
            if xx.login():
                try:
                    con = sqlite3.connect('../DA/HRDatabase.db')
                    cur = con.cursor()
                    query = "SELECT name, surname, phone, email, picture FROM managersTable WHERE email='{}'".format(xx.email)

                    xx.name, xx.surname, xx.phone, xx.email, xx.picture = cur.execute(query).fetchone()

                except sqlite3.Error as e:
                    print(e)
                    #print("Infos not found..!")

                global picture
                global logo

                dialog = QtWidgets.QDialog()
                temp = HRpage()
                temp.setupUi(dialog)

                temp.lblNameHome.setText(xx.name)
                temp.lblSurnameHome.setText(xx.surname)
                temp.lblTelHome.setText(xx.phone)
                temp.lblEmailHome.setText(xx.email)
                temp.lblLogoHome.setPixmap(QtGui.QPixmap("../Images/logo.png"))
                temp.lblProfileHome.setPixmap(QtGui.QPixmap("../Images/{}".format(xx.picture)))
                dialog.show()
                Login.close()
                dialog.exec_()

            else:
                QMessageBox.information(self.layoutWidget, "Failed", "User not found")

        else:
            pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
