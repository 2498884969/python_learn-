# coding=utf-8

import socket
import select

servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servSock.bind(('', 7788))

servSock.listen(10)

# ����һ��poll����
poll = select.poll()

# ע��ʱfd���¼���poll
# ���ش���
poll.register(servSock.fileno(), select.POLLIN)

clientSocks = {}
clientAddrs = {}

while True:

	# epoll ���� fdɨ�� -- δ����ָ��ʱ���������ȴ�
	poll_list = poll.poll()
	
	print 'poll_list: ', poll_list
	
	for fd, events in poll_list:
		
		# �����׽��ֱ�����
		if fd == servSock.fileno():
			clientSock, clientAddr = servSock.accept()
			
			print '----- %s coming ------' % str(clientAddr)
			
			clientSocks[clientSock.fileno()] = clientSock
			clientAddrs[clientSock.fileno()] = clientAddr
			
			# �� epoll ��ע���¼�
			poll.register(clientSock.fileno(), select.EPOLLIN)
			
		elif events == select.POLLIN:
			
			recvData = clientSocks[fd].recv(1024)
			
			if len(recvData) > 0:
				print 'recv:%s from %s' % (recvData, str(clientAddrs[fd]))
			else:
				# ��epoll���Ƴ���sock
				
				poll.unregister(fd)
				
				clientSocks[fd].close()
				
				del clientSocks[fd]
				
				print '%s ------ offline ------' % str(clientAddrs[fd])
				
				del clientAddrs[fd]
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
	
	
			
			
	
	
	
	
	
	
	
