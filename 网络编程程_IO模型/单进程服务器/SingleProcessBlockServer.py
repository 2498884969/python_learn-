# coding=utf-8

from socket import *

serSocket = socket(AF_INET, SOCK_STREAM)

# 重复使用绑定的信息
serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

localAddr = ('',7788)

serSocket.bind(localAddr)

# 监听队列中最多存在5个违背接受的对象
serSocket.listen(5)

while True:
	
	print '-----主进程‘ ’等待新客户端的到来-----'
	
	newSocket, destAddr = serSocket.accept()
	
	print '----- 主进程接下来负责处理数据[%s] -----' % str(destAddr)
	
	try:
		while True:
			recvData = newSocket.recv(1024)
			if len(recvData) > 0:
				print '----- recv[%s]: %s -----' % (str(destAddr), recvData)
			else:
				print '----- [%s]客户端已经关闭 -----' %str(destAddr)
	except:
		pass
	finally:
		newSocket.close()
		
serSocket.close()# coding=utf-8

from socket import *

serSocket = socket(AF_INET, SOCK_STREAM)

# 重复使用绑定的信息
serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

localAddr = ('',7788)

serSocket.bind(localAddr)

# 监听队列中最多存在5个违背接受的对象
serSocket.listen(5)

while True:
	
	print '-----主进程‘ ’等待新客户端的到来-----'
	
	newSocket, destAddr = serSocket.accept()
	
	print '----- 主进程接下来负责处理数据[%s] -----' % str(destAddr)
	
	try:
		while True:
			recvData = newSocket.recv(1024)
			if len(recvData) > 0:
				print '----- recv[%s]: %s -----' % (str(destAddr), recvData)
			else:
				print '----- [%s]客户端已经关闭 -----' %str(destAddr)
	except:
		pass
	finally:
		newSocket.close()
		
serSocket.close()