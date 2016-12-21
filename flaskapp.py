from flask import Flask
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def HelloWorld():
	restaurant = session.query(Restaurant).first() #Getting the first restaurant using sqlalchemy
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id) #Getting the item list by id of restaurant
	output = ""
	for item in items :
		output += item.name #Adding the name of item to the output 
		output += "<br>"
		output += item.price
		output += "<br>"
		output += item.description
		output += "<br>" 
		output += "<br>" 
	print output # To output on the console for  debugging reasons
	return output

if __name__ == '__main__':
    app.debug = True #allow flask server to instantly refresh it's own self 
    app.run(host='0.0.0.0', port=5000) #Listening from all address ip in port 5000