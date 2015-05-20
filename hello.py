#-*-coding:utf-8-*- 

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import hashlib
import lxml
from lxml import etree
import time

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
        map(sha1.update,l)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            self.write(echostr)

    def post(self):
        body_text = """
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[%s]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    <MsgId>6038700799783131222</MsgId>
                    </xml>
                    """
        str_xml = self.request.body #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        reply = body_text % (fromUser, toUser, str(int(time.time())), msgType, "you just said" + content)
        print reply
        self.write(reply)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/wechat", WeChatHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
