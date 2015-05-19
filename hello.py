#-*-coding:utf-8-*- 

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import hashlib
import lxml
from lxml import etree

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class WeChatHandler(tornado.web.RequestHandler):
    def get(self):
        # 配置微信接口
        signature = self.get_argument('signature', 'none')
        timestamp = self.get_argument('timestamp', 'none')
        nonce = self.get_argument('nonce', 'none')
        echostr = self.get_argument('echostr', 'none')
        token = "nebula14"
        l = [token,timestamp,nonce]
        l.sort()
        sha1 = hashlib.sha1()
        print "signature", signature
        map(sha1.update,l)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            self.write(echostr)

    def POST(self):
        str_xml = self.request.body #获得post来的数据
        signature = self.get_argument('signature', 'none')
        self.write(str_xml)
        print "signature", signature
        print "post", str_xml
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/wechat", WeChatHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
