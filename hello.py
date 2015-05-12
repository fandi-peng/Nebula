import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import hashlib


from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

class WeChatHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_argument('signature', 'none')
        timestamp = self.get_argument('timestamp', 'none')
        nonce = self.get_argument('nonce', 'none')
        echostr = self.get_argument('echostr', 'none')
        self.write(signature + " " + timestamp + " " + nonce + " " + echostr + " ")
        token = "nebula14"

        l = [token,timestamp,nonce]
        l.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,l)
        hashcode = sha1.hexdigest()
         
 
        if hashcode == signature:
            self.write(hashcode)
            #return echostr

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/wechat", WeChatHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()