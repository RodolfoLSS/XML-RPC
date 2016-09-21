from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sqlite3

connection = sqlite3.connect('microblog.db') # Conexao do banco de dados
cursor = connection.cursor() # Cursor para executar queries

# Permite varios usuarios
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Cria o Elemento Servidor
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Id para os posts 
id_post = 0

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
	cursor.execute("CREATE TABLE post (id int PRIMARY KEY, time timestamp, username varchar(50), topico varchar(5), texto varchar(100))")

#Usuario segue um Topico
def Follow (nome,topico):
	cursor.execute("SELECT * FROM topico WHERE username=(?)", (nome,))
	x =  cursor.fetchone()
	if x == None:
		if (topico == "#sod"):
			cursor.execute("INSERT INTO topico VALUES (?,?,?,?)",(nome,1,0,0,))
			print(nome)
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
		cursor.execute('SELECT username FROM topico WHERE username=(?),topico=(?))', (nome,), (topico,)) # procura o usuario que deixou de seguir o post
		usuario = cursor.fetchone()
	except:
		print('Falha ao executar select query.')

	try:
		if(topico == "#sod"):
			cursor.execute('UPDATE topico SET sod=0 WHERE username=(?)',(usuario,)) # seta 0 no campo do topico o qual o usuario parou de seguir
		elif(topico == "#cc"):
			cursor.execute('UPDATE topico SET cc=0 WHERE username=(?)',(usuario,)) # seta 0 no campo do topico o qual o usuario parou de seguir
		elif(topico == "#cd"):
			cursor.execute('UPDATE topico SET cd=0 WHERE username=(?)',(usuario,)) # seta 0 no campo do topico o qual o usuario parou de seguir
	except:
		print('Falha ao atualizar a tabela topico.')

	connection.commit() # comita alteracoes feita na tabela
	return 1

server.register_function(Unsubscribe, 'unsubscribe')

# funçao que ira inserir no banco de posts
def InserePost(nome,topico,timestamp,texto):
	try:
		cursor.execute("INSERT INTO post VALUES (?,?,?,?,?,?)",(id_post,timestamp,nome,topico,texto,))
		connection.commit()
		id_post = id_post + 1
		return 1
	except: 
		return 0
		
server.register_function(InserePost, 'inserePost')

def RetrieveTime(nome, tempo):
	
	try:
		cursor.execute('SELECT texto FROM post WHERE username=(?),time>(?))', (nome,), (tempo,)) # procura todos os posts de um determinado usuario a partir do tempo especificado
		posts = cursor.fetchall()
	except:
		print('Falha ao executar select query.')

	return posts # retorna posts encontrados

server.register_function(RetrieveTime, 'retrieveTime')

def RetrieveTopic(nome, tempo, topico):
	
	try:
		cursor.execute('SELECT texto FROM post WHERE username=(?),time>(?),topico=(?)', (nome,), (tempo,), (topico,)) # procura todos os posts de um determinado usuario e topico a partir do tempo especificado
		posts = cursor.fetchall()
	except:
		print('Falha ao executar select query.')

	return posts # retorna posts encontrados

server.register_function(RetrieveTopic, 'retrieveTopic')

#connection.close() # fecha conexao com o banco de dados

server.serve_forever() # faz a parte Servidor rodar em loop e funcionar ate o fim da execucao do programa
