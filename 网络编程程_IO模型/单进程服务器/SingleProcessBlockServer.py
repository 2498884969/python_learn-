# coding=utf-8

from socket import *

serSocket = socket(AF_INET, SOCK_STREAM)

# �ظ�ʹ�ð󶨵���Ϣ
serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

localAddr = ('',7788)

serSocket.bind(localAddr)

# ����������������5��Υ�����ܵĶ���
serSocket.listen(5)

while True:
	
	print '-----�����̡� ���ȴ��¿ͻ��˵ĵ���-----'
	
	newSocket, destAddr = serSocket.accept()
	
	print '----- �����̽���������������[%s] -----' % str(destAddr)
	
	try:
		while True:
			recvData = newSocket.recv(1024)
			if len(recvData) > 0:
				print '----- recv[%s]: %s -----' % (str(destAddr), recvData)
			else:
				print '----- [%s]�ͻ����Ѿ��ر� -----' %str(destAddr)
	except:
		pass
	finally:
		newSocket.close()
		
serSocket.close()# coding=utf-8

from socket import *

serSocket = socket(AF_INET, SOCK_STREAM)

# �ظ�ʹ�ð󶨵���Ϣ
serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

localAddr = ('',7788)

serSocket.bind(localAddr)

# ����������������5��Υ�����ܵĶ���
serSocket.listen(5)

while True:
	
	print '-----�����̡� ���ȴ��¿ͻ��˵ĵ���-----'
	
	newSocket, destAddr = serSocket.accept()
	
	print '----- �����̽���������������[%s] -----' % str(destAddr)
	
	try:
		while True:
			recvData = newSocket.recv(1024)
			if len(recvData) > 0:
				print '----- recv[%s]: %s -----' % (str(destAddr), recvData)
			else:
				print '----- [%s]�ͻ����Ѿ��ر� -----' %str(destAddr)
	except:
		pass
	finally:
		newSocket.close()
		
serSocket.close()