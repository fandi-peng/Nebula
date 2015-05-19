#-*-coding:utf-8-*- 

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import hashlib
import lxml
from lxml import etree
from wechat_sdk import WechatBasic
import json

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

        # 实例化 wechat
        wechat = WechatBasic(token=token)

        #l = [token,timestamp,nonce]
        #l.sort()
        #sha1 = hashlib.sha1()
        #map(sha1.update,l)
       # hashcode = sha1.hexdigest()
       # if hashcode == signature:
       #     self.write(echostr)

   # def POST(self):
        body_text = json.loads(self.request.body)
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            # 对 XML 数据进行解析 (必要, 否则不可执行 response_text, response_image 等操作)
            wechat.parse_data(body_text)
            # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
            message = wechat.get_message()

            response = None
            if message.type == 'text':
                if message.content == 'wechat':
                    response = wechat.response_text(u'^_^')
                else:
                    response = wechat.response_text(u'文字')
            elif message.type == 'image':
                response = wechat.response_text(u'图片')
            else:
                response = wechat.response_text(u'未知')

            # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
            print response
    #    str_xml = self.request.body #获得post来的数据
    #    self.write(str_xml)
    #    xml = etree.fromstring(str_xml)#进行XML解析
    #    content=xml.find("Content").text#获得用户所输入的内容
    #    msgType=xml.find("MsgType").text
    #    fromUser=xml.find("FromUserName").text
    #    toUser=xml.find("ToUserName").text


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/wechat", WeChatHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
