# coding=utf-8

__author__ = 'huangyouxiang'
__copyright__ = 'Copyright 15-6-10'

import socket

from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer


class Connection(object):
    # todo..陌陌群难点?
    clients = set()

    def __init__(self, stream, address):
        Connection.clients.add(self)
        self.stream = stream
        self.address = address
        self.stream.set_close_callback(self.on_close)
        self.read_message()

        self.keep_alive()
        print "connection count = ", len(Connection.clients)
        #print "A new user has entered the chat room.", address

    def read_message(self):
        self.stream.read_until('\n', self.broadcast_messages)

    def broadcast_messages(self, data):
        # print "User said:", data[:-2], self.address
        for conn in Connection.clients:
            conn.send_message(data)
        self.read_message()

    def send_message(self, data):
        try:
            self.stream.write(data)
        except:
            # todo.. 连接半关闭状态?
            self.stream.close_fd()
            Connection.clients.remove(self)

    def on_close(self):
        print "A user has left the chat room.", self.address
        Connection.clients.remove(self)

    def keep_alive(self):
        # todo..[test] 1个package的负担就可以激活连接?? 服务器宕机呢
        self.stream.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.stream.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
        self.stream.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 5)
        self.stream.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 20)


class IMServer(TCPServer):
    def handle_stream(self, stream, address):
        # todo.. 分服,每个服务器的负载
        # todo.. 重启时client重新连接消息
        Connection(stream, address)


if __name__ == '__main__':
    im = IMServer()
    im.listen(8000)
    IOLoop.instance().start()