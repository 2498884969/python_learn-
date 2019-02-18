# coding=utf-8

from socket import *

# 1. 创建套接字 
serSocket = socket(AF_INET, SOCK_STREAM)

# 重复使用绑定的信息
# serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# 2.绑定端口
localAddr = ('',7788)
serSocket.bind(localAddr)

# 3.让这个socket变为非阻塞的
serSocket.setblocking(False)

# 4.将socket变为监听套接字（被动）
serSocket.listen(100)

# 用来保存所有已经连接的客户端的信息
clientAddrList = []

while True:
	
	# print '-----主进程‘ ’等待新客户端的到来-----'
	
	# 等待一个新的客户端的到来，即完成三次握手的客户端
	try:
		clientSocket, clientAddr = serSocket.accept()
	except:
		pass
	else:
		print '一个新的客户端到来：%s' % str(clientAddr)
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
				print '------ %s 下线 -------' % str(clientAddr)
		
		
		
		
		
		
		
		
		
	
	