from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import cgi


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                engine = create_engine('sqlite:///restaurantmenu.db')
                # Bind the engine to the metadata of the Base class so that the
                # declaratives can be accessed through a DBSession instance
                Base.metadata.bind = engine

                DBSession = sessionmaker(bind=engine)
                session = DBSession()   
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants :
                    output += '<p>' + restaurant.name + '</p><a href="">Edit</a><br><a href="">Delete</a><br>'

                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<form method='post' action = '/restaurant/new' enctype='multipart/form-data' > "
                output += "Restaurant Name <input type='text' name='name' /> <br> "
                output += "Item Name <input type='text' name='itemName' /> <br> "
                output += "Description <input type='text' name='desc' /> <br> "
                output += "course <input type='text' name='course' /> <br> "
                output += "Price <input type='number' name='price' /> <br> "
                output += "<input type='submit' value='Submit'></form> "
                output += "</html></body>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            engine = create_engine('sqlite:///restaurantmenu.db')
            # Bind the engine to the metadata of the Base class so that the
            # declaratives can be accessed through a DBSession instance
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurantName = fields.get('name')
                itemName = fields.get('itemName')
                description = fields.get('desc')
                course = fields.get('course')
                price = fields.get('price')

            rest = Restaurant(name = restaurantName)
            session.add(rest)
            session.commit

            item = menuItem(name = itemName , description = description , course = course , price = price , restaurant = rest)
            session.add(item)
            session.commit()
            output = ""
            output += "<html><body>"
            output += "<form method='post' action = '/restaurant/new' enctype='multipart/form-data' > "
            output += "Restaurant Name <input type='text' name='name' /> <br> "
            output += "Item Name <input type='text' name='itemName' /> <br> "
            output += "Description <input type='text' name='desc' /> <br> "
            output += "course <input type='text' name='course' /> <br> "
            output += "Price <input type='number' name='price' /> <br> "
            output += "<input type='submit' value='Submit'></form> "
            output += "</html></body>"
            self.wfile.write(output)
            print output
            return
        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()