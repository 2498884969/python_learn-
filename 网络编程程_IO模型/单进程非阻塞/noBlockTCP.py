# coding=utf-8

from socket import *

# 1. �����׽��� 
serSocket = socket(AF_INET, SOCK_STREAM)

# �ظ�ʹ�ð󶨵���Ϣ
# serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# 2.�󶨶˿�
localAddr = ('',7788)
serSocket.bind(localAddr)

# 3.�����socket��Ϊ��������
serSocket.setblocking(False)

# 4.��socket��Ϊ�����׽��֣�������
serSocket.listen(100)

# �������������Ѿ����ӵĿͻ��˵���Ϣ
clientAddrList = []

while True:
	
	# print '-----�����̡� ���ȴ��¿ͻ��˵ĵ���-----'
	
	# �ȴ�һ���µĿͻ��˵ĵ�����������������ֵĿͻ���
	try:
		clientSocket, clientAddr = serSocket.accept()
	except:
		pass
	else:
		print 'һ���µĿͻ��˵�����%s' % str(clientAddr)
		clientSocket.setblocking(False)
		clientAddrList.append((clientSocket, clientAddr))
		
	for clientSocket, clientAddr in clientAddrList:
		try:
			recvData = clientSocket.recv(1024)
		except:
			pass
		else:
			if len(recvData) > 0:
				print '%s: %s' % (str(clientAddr),recvData)
			else:
				clientSocket.close()
				clientAddrList.remove((clientSocket, clientAddr))
				print '------ %s ���� -------' % str(clientAddr)
		
		
		
		
		
		
		
		
		
	
	