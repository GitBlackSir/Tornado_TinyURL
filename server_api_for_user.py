# -*- coding:UTF-8 -*-
# __Auth__  : @GitBlackSir
# __Date__  : 2018/4/25
# __Email__ : gitblacksir@gmail.com

import json
import getopt
import client as client
import tornado.web
import tornado.ioloop
import conf.conf as conf
import tornado.httpserver
import src.server_api_usage as server_api_usage
import src.is_true_url as is_true_url

class Api_Long_To_Short_URL_Handler(tornado.web.RequestHandler):
    def get(self,*args):
        try:
            if args[0] == '':
                dict = {'status':1,'messages':'EMPTY URL!', 'short_url': None}
                self.write(json.dumps(dict))
            elif args[0].split("/")[2] == "t.1024bit.io":
                dict = {'status':2,'messages':' FORBID INPUT TINYURL!','short_url':None }
                self.write(json.dumps(dict))
            else:
                if is_true_url.is_url(args[0]):
                    if conf.redis_conn.get(args[0]):
                        dict = {'status':3, 'messages':'this short_url from redis', 'short_url': ['http://t.1024bit.io/' + conf.redis_conn.get(args[0]).decode(), ]}
                        self.write(json.dumps(dict))
                    else:
                        id_url_dict = client.get_guid()
                        conf.redis_conn.set(id_url_dict['short_url'], args[0])
                        conf.redis_conn.set(args[0], id_url_dict['short_url'])
                        dict = {'status': 4, 'messages': 'server api for develop successful','short_url': ['http://t.1024bit.io/' + id_url_dict['short_url'], ]}
                        self.write(json.dumps(dict))
                else:
                    dict = {'status': 5, 'messages':'URL INPUT ERRO!', 'short_url':None}
                    self.write(json.dumps(dict))
        except:
            data = {'status': 6, 'messages':'URL ERRO!','short_url':None }
            self.write(json.dumps(data))


class Api_Short_To_Long_URL_Handler(tornado.web.RequestHandler):
    def get(self,*args):
        try:
            if args[0] == '':
                dict = {'status': 0, 'messages': 'EMPTY URL!', 'long_url':None}
                self.write(json.dumps(dict))
            else:
                if is_true_url.is_url(args[0]):
                    try:
                        dict = {'status': 1, 'messages': 'successfully short to lang url', 'long_url': conf.redis_conn.get(args[0].split('/')[3]).decode()}
                        self.write(json.dumps(dict))
                    except:
                        dict = {'status': 2, 'messages': 'url eg:http://t.1024bit.io/+xxxxxxxxx','long_url': None}
                        self.write(json.dumps(dict))
                else:
                    dict = {'status': 3, 'messages': 'URL ERRO!', 'long_url': None}
                    self.write(json.dumps(dict))
        except:
            dict = {'status': 4, 'messages': 'URL ERRO!', 'long_url': None}
class Api_For_User_Application(tornado.web.Application):
    def __init__(self, **settings):
        handlers = [
            (r'/json&convert=(.*)', Api_Long_To_Short_URL_Handler),
            (r'/json&restore=(.*)', Api_Short_To_Long_URL_Handler),
        ]
        settings = {'debug': False,}
        super(Api_For_User_Application, self).__init__(handlers, **settings)

if __name__ == '__main__':
    try:
        # options, args = getopt.getopt(sys.argv[1:], "lhmi:p:d:w:",
        #                               ['list', 'help', 'init_mysql' "ip=", "port=", "datacenter=", "worker="])
        # for name, value in options:
        #     if name in ('-h', '--help'):
        #         server_api_usage.usage()
        #         sys.exit()
        #     if name in ('-l', '--list'):
        #         by_mysql.list_host_mysql()
        #         sys.exit()
        #     elif name in ('-i', '--ip'):
        #         R_ADDRESS = value
        #     elif name in ('-p', '--port'):
        #         PORT = int(value)
        #     elif name in ('-d', '--datacenter'):
        #         DC_ID = int(value)
        #     elif name in ('-w', '--worker'):
        #         WORKER_ID = int(value)
        http_server = tornado.httpserver.HTTPServer(Api_For_User_Application())
        print("Starting ID Server start at %s:%d" % (conf.server_api_for_user['ADDRESS'], conf.server_api_for_user['PORT']))
        http_server.listen(conf.server_api_for_user['PORT'],conf.server_api_for_user['ADDRESS'])
        try:
            tornado.ioloop.IOLoop.instance().start()
        except:
            print('close....')
    except getopt.GetoptError:
        server_api_usage.usage()