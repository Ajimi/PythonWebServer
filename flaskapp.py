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
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one() # get the restaurant id using the route
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
	return output

@app.route('/restaurant/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"
    
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True #allow flask server to instantly refresh it's own self 
    app.run(host='0.0.0.0', port=5000) #Listening from all address ip in port 5000