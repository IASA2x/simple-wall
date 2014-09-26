import markdown
import os.path, re
import torndb, tornado.auth, tornado.httpserver
import tornado.ioloop, tornado.options, tornado.web
import unicodedata

from tornado.options import define, options
define("port", default = 8001)
define("mysql_host", default = "127.0.0.1:3306")
define("mysql_user", default="root")
define("mysql_database", default = "simplewall")
define("mysql_password", default = "")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler)
			]
		root = os.path.dirname(__file__)
		settings = {
			'template_path' : os.path.join(root, 'templates'),
			'static_path' : os.path.join(root, 'static')
			}
		tornado.web.Application.__init__(self, handlers, **settings)
		self.db = torndb.Connection(
			host=options.mysql_host, database=options.mysql_database,
			user=options.mysql_user, password=options.mysql_password)



class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

class HomeHandler(BaseHandler):
	def get(self):
		messages = self.db.query("SELECT * FROM posts")
		self.render("home.html", messages=messages)
	def post(self):
		s = self.get_argument("content")
		self.db.query("insert into posts(body, ip) values('aa','bb');")
		# insert to database

		self.redirect("/")
def main():
	application = Application()
	http_server =tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__=="__main__":
	main()

