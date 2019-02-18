# coding=utf-8

import socket
import select

servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servSock.bind(('', 7788))

servSock.listen(10)

# 创建一个poll对象
poll = select.poll()

# 注册时fd和事件到poll
# 边沿触发
poll.register(servSock.fileno(), select.POLLIN)

clientSocks = {}
clientAddrs = {}

while True:

	# epoll 进行 fd扫描 -- 未超过指定时间则阻塞等待
	poll_list = poll.poll()
	
	print 'poll_list: ', poll_list
	
	for fd, events in poll_list:
		
		# 监听套接字被激活
		if fd == servSock.fileno():
			clientSock, clientAddr = servSock.accept()
			
			print '----- %s coming ------' % str(clientAddr)
			
			clientSocks[clientSock.fileno()] = clientSock
			clientAddrs[clientSock.fileno()] = clientAddr
			
			# 向 epoll 中注册事件
			poll.register(clientSock.fileno(), select.EPOLLIN)
			
		elif events == select.POLLIN:
			
			recvData = clientSocks[fd].recv(1024)
			
			if len(recvData) > 0:
				print 'recv:%s from %s' % (recvData, str(clientAddrs[fd]))
			else:
				# 从epoll中移除该sock
				
				poll.unregister(fd)
				
				clientSocks[fd].close()
				
				del clientSocks[fd]
				
				print '%s ------ offline ------' % str(clientAddrs[fd])
				
				del clientAddrs[fd]
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
	
	
			
			
	
	
	
	
	
	
	
