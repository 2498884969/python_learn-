# coding=utf-8

import socket
import select

servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servSock.bind(('', 7788))

servSock.listen(10)

# ����һ��epoll����
epoll = select.epoll()

# ע��ʱfd���¼���epoll
# ���ش���
epoll.register(servSock.fileno(), select.EPOLLIN | select.EPOLLET)

clientSocks = {}
clientAddrs = {}

while True:

	# epoll ���� fdɨ�� -- δ����ָ��ʱ���������ȴ�
	epoll_list = epoll.poll()
	
	print 'epoll_list: ', epoll_list
	
	for fd, events in epoll_list:
		
		# �����׽��ֱ�����
		if fd == servSock.fileno():
			clientSock, clientAddr = servSock.accept()
			
			print '----- %s coming ------' % str(clientAddr)
			
			clientSocks[clientSock.fileno()] = clientSock
			clientAddrs[clientSock.fileno()] = clientAddr
			
			# �� epoll ��ע���¼�
			epoll.register(clientSock.fileno(), select.EPOLLIN | select.EPOLLET)
			
		elif events == select.EPOLLIN:
			
			recvData = clientSocks[fd].recv(1024)
			
			if len(recvData) > 0:
				print 'recv:%s from %s' % (recvData, str(clientAddrs[fd]))
			else:
				# ��epoll���Ƴ���sock
				
				epoll.unregister(fd)
				
				clientSocks[fd].close()
				
				del clientSocks[fd]
				
				print '%s ------ offline ------' % str(clientAddrs[fd])
				
				del clientAddrs[fd]
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
	
	
			
			
	
	
	
	
	
	
	
