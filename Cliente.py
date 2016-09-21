import xmlrpc.client
from tkinter import *
from datetime import datetime

s = xmlrpc.client.ServerProxy('http://localhost:8000')

#funções que estão no servidor
#Follow
def inserir_usuario():
    nome = ("@"+usuario1.get())
    topico = ("#"+topico1.get())
    l = s.follow(nome,topico)

#post
def envia_post():
	nome = ("@"+usuario2.get())
	topico = ("#"+topico2.get())
	texto = (post2.get())
	par3 = datetime.now()
	l = s.inserePost(nome, topico, par3, texto)

#unsubscribe
def deixar_topico():
	nome = ("@"+usuario3.get())
	topico = ("#"+topico3.get())
	l = s.unsubscribe(nome,topico)

#retrievetime
def recupera_tudo():
	nome = ("@"+usuario4.get())
	par3 = (data4.get())
	variavel = s.retrieveTime(nome,par3)

#retrievetopic
def recupera_topico():
	nome = ("@"+usuario5.get())
	topico = ("#"+topico5.get())
	par3 = (data5.get())
	#l = s.retrieveTopic(nome, par3, topico)

###########################################################

##criação da janela de interface gráfica
janela = Tk()
janela.title("Blog de SO")
janela["bg"] = "black"
janela.geometry("1366x768")

##criando o botão de inserção do usuário em um determinado tópico
bt1 = Button(janela, width=60,text="Ingressar em algum tópico", command=inserir_usuario)
bt1.place(x=450,y=100)
##caixa de texto onde será inserido o @Username
usuario1 = Entry(janela)
usuario1.place(x=495,y=130)
lb1 = Label(janela, text = "Nome:")
lb1.place(x=450,y=130)
##caixa de texto onde será inserido o #tópico
topico1 = Entry(janela)
topico1.place(x=720,y=130)
lb1_1 = Label(janela, text = "Tópico:")
lb1_1.place(x=670,y=130)

##criando o botão de inserção de um post
bt2 = Button(janela, width=60,text="Fazer um post", command=envia_post)
bt2.place(x=450,y=160)
##caixa de texto onde será inserido o @Username
usuario2 = Entry(janela)
usuario2.place(x=495,y=190)
lb2 = Label(janela,text="Nome")
lb2.place(x=450,y=190)
##caixa de texto onde será inserido o #tópico
topico2 = Entry(janela)
topico2.place(x=720,y=190)
lb1_2 = Label(janela, text = "Tópico:")
lb1_2.place(x=670,y=190)
##caixa de texto onde será inserido o post
post2 = Entry(janela)
post2.place(x=925,y=190)
lb1_2_2 = Label(janela, text = "Post:")
lb1_2_2.place(x=890,y=190)

##criando o botão de remoção de um usuário de um determinado tópico
bt3 = Button(janela, width=60,text="Deixar de seguir tópico", command=deixar_topico)
bt3.place(x=450,y=220)
##caixa de texto onde será inserido o @Username
usuario3 = Entry(janela)
usuario3.place(x=495,y=250)
lb3 = Label(janela, text = "Nome:")
lb3.place(x=450,y=250)
##caixa de texto onde será inserido o #tópico
topico3 = Entry(janela)
topico3.place(x=720,y=250)
lb3_3 = Label(janela, text = "Tópico:")
lb3_3.place(x=670,y=250)

##criando o botão de recuperação de todos os posts que um usuário faz parte
bt4 = Button(janela, width=60,text="Recupera todos os posts de todos os tópicos", command=recupera_tudo)
bt4.place(x=450,y=280)
##caixa de texto onde será inserido o @Username
usuario4 = Entry(janela)
usuario4.place(x=495,y=310)
lb2 = Label(janela,text="Nome")
lb2.place(x=450,y=310)
##caixa de texto onde será inserido a data
data4 = Entry(janela)
data4.place(x=820,y=310)
lb2 = Label(janela,text="Data(ex: aaaa-mm-dd):")
lb2.place(x=670,y=310)

##O usuário recupera todos os posts, apenas do tópico identificado
bt5 = Button(janela, width=60,text="Recupera todos os posts de um determinado tópico", command=recupera_topico)
bt5.place(x=450,y=340)
##caixa de texto onde será inserido o @Username
usuario5 = Entry(janela)
usuario5.place(x=495,y=370)
lb5 = Label(janela, text = "Nome:")
lb5.place(x=450,y=370)
##caixa de texto onde será inserido o #tópico
topico5 = Entry(janela)
topico5.place(x=720,y=370)
lb3_5 = Label(janela, text = "Tópico:")
lb3_5.place(x=670,y=370)
##caixa de texto onde será inserido a data
data4 = Entry(janela)
data4.place(x=1040,y=370)
lb2 = Label(janela,text="Data(ex: aaaa-mm-dd):")
lb2.place(x=890,y=370)

##método que executa a interface gráfica
janela.mainloop()
