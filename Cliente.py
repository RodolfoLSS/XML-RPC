import xmlrpc.client
from tkinter import *

s = xmlrpc.client.ServerProxy('http://localhost:8596')

#funções
def inserir_usuario():
    nome = ("@"+usuario1.get()+"\n")
    topico = ("#"+topico1.get())
    l = s.follow(nome,topico)

janela = Tk()
janela.title("Blog de SO")
janela["bg"] = "blue"
janela.geometry("1366x768")
bt1 = Button(janela, width=60,text="Ingressar em algum tópico", command=inserir_usuario)
bt1.place(x=450,y=100)
usuario1 = Entry(janela)
usuario1.place(x=495,y=130)
lb1 = Label(janela, text = "Nome:")
lb1.place(x=450,y=130)
########################
topico1 = Entry(janela)
topico1.place(x=720,y=130)
lb1_1 = Label(janela, text = "Tópico:")
lb1_1.place(x=670,y=130)
#bt2 = Button(janela, width=50,text="Fazer um post")
#bt2.place(x=450,y=160)
#usuario = Entry(janela)
#usuario.place(x=450)
janela.mainloop()

var = 1
while var == 1:
	opcao = input("1 - Ingressar em tópico\n2 - Fazer um post\n3 - Deixar de seguir um determinado tópico\n0 - Sair\nOpcao:")
	if (int(opcao) == 0):
		break
	elif(int(opcao) == 1):
		Username = ("@" + input("Digite o nome do usuário:")+"\n")
		Topico = ("#" + input("Digite o tópico em que quer participar:"))
		l = s.follow(Username,Topico)
	elif(int(opcao) == 2):
		Username = ("Postado por: "+"@" + input("Nome do usuário:")+"\n")
		Topico = ("#" + input("Tópico em que fará o post:"))
		Texto = (input("Texto a ser postado:"))
		l = s.post(Username, Topico, Texto)
	elif(int(opcao) == 3):
		Username = ("@" + input("Digite o nome do usuário:")+"\n")
		Topico = ("#" + input("Digite o tópico em que deseja deixar de seguir:"))
		l = s.unsubscribe(Username, Topico)
 #Print (list of available methods)
#print s.system.listMethods()
