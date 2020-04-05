import sys
import os
import json
import uuid
import logging
from queue import Queue


class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.users['naja'] = {'nama': 'Naja', 'Kota': 'Pekalongan', 'password': 'pkl', 'incoming': {},
                               'outgoing': {}}
        self.users['arini'] = {'nama': 'Arini', 'Kota': 'Bojonegoro', 'password': 'bjn', 'incoming': {},
                               'outgoing': {}}
        self.users['awin'] = {'nama': 'Awin', 'Kota': 'Solo', 'password': 'slo',
                                   'incoming': {}, 'outgoing': {}}
        self.users['yuki'] = {'nama': 'Yuki', 'Kota': 'Bojonegoro', 'password': 'bjn', 'incoming': {},
                                 'outgoing': {}}

    def proses(self, data):
        j = data.split(" ")
        try:
            command = j[0].strip()
            if (command == 'login'):
                username = j[1].strip()
                password = j[2].strip()
                logging.warning("AUTH: login {} {}".format(username, password))
                return self.autentikasi_user(username, password)
            elif (command == 'chat'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning(
                    "CHAT: session {} send message from {} to {}".format(sessionid, usernamefrom, usernameto))
                return self.send_message(sessionid, usernamefrom, usernameto, message)

            elif (command == 'kotakmasuk'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("Kotak_Masuk: {}".format(sessionid))
                return self.get_inbox(username)
            elif (command == 'user_on'):
                sessionid = j[1].strip()
                logging.warning("LIST USER: {}".format(sessionid))
                return self.user_on()
            elif (command == 'logout'):
                sessionid = j[1].strip()
                logging.warning("LOGOUT: {}".format(sessionid))
                return self.logout(sessionid)

            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        if (username not in self.users):
            return {'status': 'ERROR', 'message': 'User Tidak Ada'}
        if (self.users[username]['password'] != password):
            return {'status': 'ERROR', 'message': 'Password Salah'}
        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {'username': username, 'userdetail': self.users[username]}
        return {'status': 'OK', 'tokenid': tokenid}

    def get_user(self, username):
        if (username not in self.users):
            return False
        return self.users[username]

    def send_message(self, sessionid, username_from, username_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[username_from].put(message)
        except KeyError:
            outqueue_sender[username_from] = Queue()
            outqueue_sender[username_from].put(message)
        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def get_inbox(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())

        return {'status': 'OK', 'messages': msgs}

    def user_on(self):
        token = list(self.sessions.keys())
        user_on = ""
        for i in token:
            user_on = user_on + self.sessions[i]['username'] + ", "
        return {'status': 'OK', 'message': '{}'.format(user_on)}

    def logout(self, sessionid):
        del self.sessions[sessionid]
        return {'status': 'OK', 'messages': "logout success"}


if __name__ == "__main__":
    j = Chat()
    sesi = j.proses("login naja pkl")
    print(sesi)
    # sesi = j.autentikasi_user('messi','surabaya')
    # print sesi
    tokenid = sesi['tokenid']
    print(j.proses("chat {} arini hai rin ".format(tokenid)))
    print(j.proses("chat {} awin hai win ".format(tokenid)))
    print(j.proses("chat {} yuki hai yuk ".format(tokenid)))

    print("isi mailbox dari awin")
    print(j.get_inbox('awin'))
    print("isi mailbox dari arini")
    print(j.get_inbox('arini'))
    print("isi mailbox dari yuki")
    print(j.get_inbox('yuki'))
