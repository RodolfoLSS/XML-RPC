from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sqlite3

connection = sqlite3.connect('microblog.db') # Conexao do banco de dados
cursor = connection.cursor() # Cursor para executar queries

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8596),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

# Cria tabela Topico
cursor.execute('''CREATE TABLE topico
					(username varchar(50), sod int, cc int, cd int, PRIMARY KEY username)''')

# Cria tabela Post
cursor.execute('''CREATE TABLE post
					(id int, time timestamp, username varchar(50), topico varchar(5), texto varchar(100), PRIMARY KEY id)''')


def Follow (username,topico):
	c.execute('SELECT * FROM topico WHERE username=?', username)
	x =  c.fetchone()
	
	if x == None:
		if (topico == "#sod"):
			c.execute("INSERT INTO topico VALUES (?,?,?)",username,1,0,0)
		elif (topico == "#cc"):
			c.execute("INSERT INTO topico VALUES (?,?,?)",username,0,1,0)
		elif (topico == "#cd"):
			c.execute("INSERT INTO topico VALUES (?,?,?)",username,0,0,1)
		else:
			return 1
	else:
		if (topico == "#sod"):
			c.execute("UPDATE topico SET sod=1 WHERE username=?",username)
		elif (topico == "#cc"):
			c.execute("UPDATE topico SET cc=1 WHERE username=?",username)
		elif (topico == "#cd"):
			c.execute("UPDATE topico SET cd=1 WHERE username=?",username)
		else:
			return 1
	return 0
	
server.register_function(Follow())

def Unsubscribe(nome, topico):

	try:
		cursor.execute('SELECT username FROM topico WHERE username=?,topico=?)', nome, topico) # procura o usuario que deixou de seguir o post
		usuario = cursor.fetchone()
	except:
		print('Falha ao executar select query.')

	try:
		if(topico == "#sod"):
			cursor.execute('UPDATE topico SET sod=0 WHERE username=?',usuario) # seta 0 no campo do topico o qual o usuario parou de seguir
		elif(topico == "#cc"):
			cursor.execute('UPDATE topico SET cc=0 WHERE username=?',usuario) # seta 0 no campo do topico o qual o usuario parou de seguir
		elif(topico == "#cd"):
			cursor.execute('UPDATE topico SET cd=0 WHERE username=?',usuario) # seta 0 no campo do topico o qual o usuario parou de seguir
	except:
		print('Falha ao atualizar a tabela topico.')

	connection.commit() # comita alteracoes feita na tabela
	return 1

server.register_function(Unsubscribe, 'unsubscribe')

# funçao que ira inserir no banco de posts
def insere_post(id_post,username,topico,timestamp,texto):
	try:
		c.execute("INSERT INTO post VALUES (?,?,'?','?','?',?)",int(id_post),timestamp,username,topico,texto)
		conn.commit()
		return 1
	except: 
		return 0
		
server.register_function(insere_post())

def RetrieveTime(nome, tempo):
	
	try:
		cursor.execute('SELECT texto FROM post WHERE username=?,time>?)', nome, tempo) # procura todos os posts de um determinado usuario a partir do tempo especificado
		posts = cursor.fetchall()
	except:
		print('Falha ao executar select query.')

	try:
		for row in posts:
			print(row + '\n') # printa na tela os posts
	except:
		print('Falha ao atualizar a tabela topico.')

	return 1

server.register_function(RetrieveTime, 'retrieveTime')

def RetrieveTopic(nome, tempo, topico):
	
	try:
		cursor.execute('SELECT texto FROM post WHERE username=?,time>?,topico=?', nome, tempo, topico) # procura todos os posts de um determinado usuario e topico a partir do tempo especificado
		posts = cursor.fetchall()
	except:
		print('Falha ao executar select query.')

	try:
		for row in posts:
			print(row + '\n') # printa na tela os posts
	except:
		print('Falha ao atualizar a tabela topico.')

	return 1

server.register_function(RetrieveTopic, 'retrieveTopic')

connection.close() # fecha conexao com o banco de dados
# Run the server's main loop
server.serve_forever()
