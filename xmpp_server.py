# coding=utf-8

__author__ = 'huangyouxiang'
__copyright__ = 'Copyright 15-6-11'

import mailer

from sleekxmpp.componentxmpp import ComponentXMPP


if __name__ == '__main__':
    muc = ComponentXMPP("test", "mimi", host="127.0.0.1", port=9090)
    if muc.connect():
        muc.process(block=False)