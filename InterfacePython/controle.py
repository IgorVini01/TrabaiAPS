from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QFrame, QMessageBox
from PyQt5 import QtGui
import psycopg2

def cadastro():

    login.hide()
    formulario.show()


def cadastrar():

    cpf = formulario.lineEdit.text()
    email = formulario.lineEdit_2.text()
    senha = formulario.lineEdit_3.text()
    
    if(cpf=="" or email=="" or senha==""):
        QMessageBox.about(formulario, "Alerta", "CAMPO VAZIO !!!")
        return 1
    
    con = psycopg2.connect(database='Cinema', user='postgres', password='12345')
    cur = con.cursor()
    cur.execute("select cpf from usuario where cpf='%s';"%(cpf))
    l = cur.fetchall()
    con.close()

    if (len(l) > 0):
        QMessageBox.about(formulario, "Alerta", "CPF JA CADASTRADO !!!")
        return 1
    
    if (len(cpf) != 11):
        QMessageBox.about(formulario, "Alerta", "CPF INVÁLIDO !!!")
        return 1
    
    inv = False
    for i in cpf:
        if(not i.isdigit()):
            inv = True
            break
    
    if(inv):
        QMessageBox.about(formulario, "Alerta", "CPF INVÁLIDO !!!")
        return 1
    
    if (len(senha) < 5 or len(senha) > 15):
        QMessageBox.about(formulario, "Alerta", "SENHA INVÁLIDA !!!")
        return 1
    
    cnt = 0
    p = -1

    for i in range(len(email)):
        if (email[i]=='@'):
            cnt+=1
            p = i
    
    if(cnt!=1):
        QMessageBox.about(formulario, "Alerta", "EMAIL INVÁLIDO !!!")
        return 1
    
    if(p==0 or p==len(email)-1):
        QMessageBox.about(formulario, "Alerta", "EMAIL INVÁLIDO !!!")
        return 1
    
    con = psycopg2.connect(database='Cinema', user='postgres', password='12345')
    cur = con.cursor()
    cur.execute("insert into usuario values('%s','%s','%s');"%(cpf,email,senha))
    con.commit()
    con.close()

    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

    QMessageBox.about(formulario, "Alerta", "CADASTRO REALIZADO !!!")

def loginn():

    formulario.hide()
    login.show()


def logar():
    
    cpf = login.lineEdit.text()
    senha = login.lineEdit_3.text()

    con = psycopg2.connect(database='Cinema', user='postgres', password='12345')
    cur = con.cursor()
    cur.execute("select cpf,senha from usuario where cpf='%s';"%(cpf))
    l = cur.fetchall()
    con.close

    if (len(l)==0):
        QMessageBox.about(login,"Alerta", "CPF NÃO CADASTRADO !!!")
        return 1

    if(senha != l[0][1]):
        QMessageBox.about(login, "Alerta", "SENHA INCORRETA !!!")
        return 1

    QMessageBox.about(login, "Alerta", "BEM-VINDO !!!")


app=QtWidgets.QApplication([])
formulario=uic.loadUi("Telas/formulario.ui")
login=uic.loadUi("Telas/login.ui")


formulario.pushButton.clicked.connect(cadastrar)
formulario.pushButton_2.clicked.connect(loginn)


login.pushButton_2.clicked.connect(cadastro)
login.pushButton.clicked.connect(logar)

login.show()
app.exec()