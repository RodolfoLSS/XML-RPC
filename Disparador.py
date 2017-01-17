from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import datetime
from random import randint

# Permite varios usuarios
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Cria o Elemento Servidor
server = SimpleXMLRPCServer(("localhost", 8590),
                            requestHandler=RequestHandler)

server_call = xmlrpc.client.ServerProxy('http://localhost:8591')
server_call2 = xmlrpc.client.ServerProxy('http://localhost:8592')

#Usuario segue um Topico
def FollowDisparador(nome, topico):
		
	aleatory_number = (randint(0,1))

	if aleatory_number == 0:
		try:
			resp = server_call.follow(nome, topico)
		except:
			resp = server_call2.follow(nome, topico)	
	else:
		try:
			resp = server_call2.follow(nome, topico)
		except:
			resp = server_call.follow(nome, topico)		

	return 0
	
server.register_function(FollowDisparador, 'followDisparador')

def InserePostDisparador(nome,topico,timestamp,texto):

	aleatory_number = (randint(0,1))

	if aleatory_number == 0:
		try:
			resp = server_call.inserePost(nome,topico,timestamp,texto)
		except:
			resp = server_call2.inserePost(nome,topico,timestamp,texto)	
	else:
		try:
			resp = server_call2.inserePost(nome,topico,timestamp,texto)
		except:
			resp = server_call.inserePost(nome,topico,timestamp,texto)		

	return 0

server.register_function(InserePostDisparador, 'inserePostDisparador')

def UnsubscribeDisparador(nome, topico):

	aleatory_number = (randint(0,1))

	if aleatory_number == 0:
		try:
			resp = server_call.unsubscribe(nome,topico)
		except:
			resp = server_call2.unsubscribe(nome,topico)	
	else:
		try:
			resp = server_call2.unsubscribe(nome,topico)
		except:
			resp = server_call.unsubscribe(nome,topico)		

	return 0

server.register_function(UnsubscribeDisparador, 'unsubscribeDisparador')

def RetrieveTimeDisparador(nome, tempo):

	aleatory_number = (randint(0,1))

	if aleatory_number == 0:
		try:
			resp = server_call.retrieveTime(nome,tempo)
		except:
			resp = server_call2.retrieveTime(nome,tempo)	
	else:
		try:
			resp = server_call2.retrieveTime(nome,tempo)
		except:
			resp = server_call.retrieveTime(nome,tempo)		

	return resp

server.register_function(RetrieveTimeDisparador, 'retrieveTimeDisparador')

def RetrieveTopicDisparador(nome, tempo, topico):

	aleatory_number = (randint(0,1))

	if aleatory_number == 0:
		try:
			resp = server_call.retrieveTopic(nome,tempo, topico)
		except:
			resp = server_call2.retrieveTopic(nome,tempo, topico)	
	else:
		try:
			resp = server_call2.retrieveTopic(nome,tempo, topico)
		except:
			resp = server_call.retrieveTopic(nome,tempo, topico)		

	return resp

server.register_function(RetrieveTopicDisparador, 'retrieveTopicDisparador')

def PollDisparador(topico, data1, data2):

	aleatory_number = (randint(0,1))

	if aleatory_number == 0:
		try:
			resp = server_call.poll(topico,data1, data2)
		except:
			resp = server_call2.poll(topico,data1, data2)
	else:
		try:
			resp = server_call2.poll(topico,data1, data2)
		except:
			resp = server_call.poll(topico,data1, data2)

	return resp

server.register_function(PollDisparador, 'pollDisparador')

server.serve_forever() # faz a parte Servidor rodar em loop e funcionar ate o fim da execucao do programa
