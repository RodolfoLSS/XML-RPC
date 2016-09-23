from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sqlite3
import datetime

connection = sqlite3.connect('microblog.db') # Conexao do banco de dados
cursor = connection.cursor() # Cursor para executar queries

# Permite varios usuarios
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Cria o Elemento Servidor
server = SimpleXMLRPCServer(("localhost", 8590),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Id para os posts 
idpost = 0

# Cria tabela Topico
try:
	cursor.execute("CREATE TABLE topico (username varchar(50) PRIMARY KEY, sod int, cc int, cd int)")
except:
	cursor.execute("DROP TABLE topico") # dropa a tabela caso ela ja exista
	cursor.execute("CREATE TABLE topico (username varchar(50) PRIMARY KEY, sod int, cc int, cd int)")

# Cria tabela Post
try:
	cursor.execute("CREATE TABLE post (username varchar(50) PRIMARY KEY, sod int, cc int, cd int)")
except:
	cursor.execute("DROP TABLE post") # dropa a tabela caso ela ja exista
	cursor.execute("CREATE TABLE post (id int PRIMARY KEY, time date, username varchar(50), topico varchar(5), texto varchar(100))")

#Usuario segue um Topico
def Follow (nome,topico):
	cursor.execute("SELECT * FROM topico WHERE username=(?)", (nome,))
	x =  cursor.fetchone()
	if x == None:
		if (topico == "#sod"):
			cursor.execute("INSERT INTO topico VALUES (?,?,?,?)",(nome,1,0,0,))
		elif (topico == "#cc"):
			cursor.execute("INSERT INTO topico VALUES (?,?,?,?)",(nome,0,1,0,))
		elif (topico == "#cd"):
			cursor.execute("INSERT INTO topico VALUES (?,?,?,?)",(nome,0,0,1,))
		else:
			return 1
	else:
		if (topico == "#sod"):
			cursor.execute("UPDATE topico SET sod=1 WHERE username=(?)",(nome,))
		elif (topico == "#cc"):
			cursor.execute("UPDATE topico SET cc=1 WHERE username=(?)",(nome,))
		elif (topico == "#cd"):
			cursor.execute("UPDATE topico SET cd=1 WHERE username=(?)",(nome,))
		else:
			return 2
	
	connection.commit()
	return 0
	
server.register_function(Follow, 'follow')

def Unsubscribe(nome, topico):

	try:
		if(topico == "#sod"):
			cursor.execute('UPDATE topico SET sod=0 WHERE username=(?)',(nome,)) # seta 0 no campo do topico o qual o usuario parou de seguir
		elif(topico == "#cc"):
			cursor.execute('UPDATE topico SET cc=0 WHERE username=(?)',(nome,)) # seta 0 no campo do topico o qual o usuario parou de seguir
		elif(topico == "#cd"):
			cursor.execute('UPDATE topico SET cd=0 WHERE username=(?)',(nome,)) # seta 0 no campo do topico o qual o usuario parou de seguir
	except:
		print('Falha ao atualizar a tabela topico.')

	connection.commit() # comita alteracoes feita na tabela
	return 1

server.register_function(Unsubscribe, 'unsubscribe')

# funçao que ira inserir no banco de posts
def InserePost(nome,topico,timestamp,texto):
	global idpost
	if (topico == "#cc" or topico == "#cd" or topico == "#sod"):
		cursor.execute("INSERT INTO post VALUES (?,?,?,?,?)",(int(idpost),timestamp,nome,topico,texto,))
		connection.commit()
		idpost = idpost + 1
		return 1
	else:
		return 0
		
server.register_function(InserePost, 'inserePost')

def RetrieveTime(nome, tempo):

	try:
		
		posts = ''
		cursor.execute("SELECT * FROM topico WHERE username=(?) AND sod=1", (nome,))
		x =  cursor.fetchone()
		if x != None:
			cursor.execute("SELECT username,topico,texto FROM post WHERE time>=(?) AND topico='#sod'",(tempo,)) # procura todos os posts de um determinado usuario a partir do tempo especificado
			results = cursor.fetchall()
			for row in results:
				posts += 'Username:' + row[0] + ' topico:' + row[1] + ' postou: ' + row[2] + '\n'
		
		cursor.execute("SELECT * FROM topico WHERE username=(?) AND cc=1", (nome,))
		x =  cursor.fetchone()
		if x != None:
			cursor.execute("SELECT username,topico,texto FROM post WHERE time>=(?) AND topico='#cc'",(tempo,)) # procura todos os posts de um determinado usuario a partir do tempo especificado
			results = cursor.fetchall()
			for row in results:
				posts += 'Username:' + row[0] + ' topico:' + row[1] + ' postou: ' + row[2] + '\n'
		
		cursor.execute("SELECT * FROM topico WHERE username=(?) AND cd=1", (nome,))
		x =  cursor.fetchone()
		if x != None:
			cursor.execute("SELECT username,topico,texto FROM post WHERE time>=(?) AND topico='#cd'",(tempo,)) # procura todos os posts de um determinado usuario a partir do tempo especificado
			results = cursor.fetchall()
			for row in results:
				posts += 'Username:' + row[0] + ' topico:' + row[1] + ' postou: ' + row[2] + '\n'
		#except:
		#	posts = 'Falha ao executar select query.'
	except:
		posts = "Erro: USERNAME inexistente ou DATA escrita de forma errada"
		
	return posts # retorna posts encontrados

server.register_function(RetrieveTime, 'retrieveTime')

def RetrieveTopic(nome, tempo, topico):
	posts = ''
	if (topico == "#sod"):
		cursor.execute("SELECT * FROM topico WHERE username=(?) AND sod=1",(nome,))
		x =  cursor.fetchone()
	elif (topico == "#cc"):
		cursor.execute("SELECT * FROM topico WHERE username=(?) AND cc=1",(nome,))
		x =  cursor.fetchone()
	elif (topico == "#cd"):
		cursor.execute("SELECT * FROM topico WHERE username=(?) AND cd=1",(nome,))
		x =  cursor.fetchone()
	else:
		return "Erro: Topico digitado nao existente"
	
	try:
		if x != None:
			cursor.execute("SELECT username,topico,texto FROM post WHERE time>(?) AND topico=(?)",(tempo,topico,)) # procura todos os posts de um determinado usuario e topico a partir do tempo especificado
			results = cursor.fetchall()
			for row in results:
				posts += 'Username:' + row[0] + ' topico:' + row[1] + ' postou: ' + row[2] + '\n'
	except:
		posts = 'Erro: NOME inexistente ou DATA digitada de maneira errada'

	return posts # retorna posts encontrados

server.register_function(RetrieveTopic, 'retrieveTopic')

server.serve_forever() # faz a parte Servidor rodar em loop e funcionar ate o fim da execucao do programa
