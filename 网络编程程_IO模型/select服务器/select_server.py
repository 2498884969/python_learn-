# coding=utf-8

import select
import socket
import sys

serSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
localAddr = ('',7788)
serSocket.bind(localAddr)
serSocket.listen(5)

inputs = [serSocket, sys.stdin]
clientAddrs = {}

while True:
	
	# 调用select函数，阻塞等待
	readable, writeable, exceptional = select.select(inputs, [], [])
	
	# 数据到达-循环
	for sock in readable:
	
		# 监听到有新的连接
		if sock == serSocket:
			clientSock, clientAddr = sock.accept()
			# select 监听到的socket
			inputs.append(clientSock)
			clientAddrs[clientSock] = clientAddr
			print '%s coming' % str(clientAddr)
		
		# 监听到键盘输入
		elif sock == sys.stdin:
			cmd = sys.std.readline()
			print cmd
			
		# 有效数据到达
		else:
			# 读取客户端发送的数据
			data = sock.recv(1024)
			if len(data) > 0:
				sock.send(data)
			else:
				# 移除inputs中的socket
				inputs.remove(sock)
				sock.close()
				print '----- %s offline -----' % str(clientAddrs[sock])
				del clientAddrs[sock]
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	

