from flask import Flask, render_template, url_for, request, redirect, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker, joinedload
from database_setup import Base, User, Category, Items
from flask import session as login_session
import random
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, jsonify, make_response
import requests
import string
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

# Google Connect Client ID
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read(

))['web']['client_id']
CLIENT_SECRET_FILE = 'client_secrets.json'

# Database connection
engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine

# Session Created
DBSession = sessionmaker(bind=engine)
session = DBSession()


# A route to login page and it creates an anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x
                    in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state,
                           login_session=login_session)


# Homepage, it shows the latest 8 items
@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Items).order_by(desc(Items.id)).limit(8)
    if 'username' not in login_session:
        return render_template('publichome.html', categories=categories,
                               items=items)
    else:
        return render_template('home.html', categories=categories, items=items)


# A page to show all items under a selected category
@app.route('/catalog/<string:catalog_name>/items')
def showCategoryItems(catalog_name):
    categories = session.query(Category).order_by(asc(Category.name)).all()
    catalogName = session.query(Category).filter_by(name=catalog_name).one()
    items = session.query(Items).filter_by(category_id=catalogName.id).all()
    creator = getUserInfo(catalogName.user_id)
    if 'username' not in login_session:
        return render_template('publicitems.html', catalogName=catalogName,
                               items=items, categories=categories)
    else:
        return render_template('items.html', catalogName=catalogName,
                               items=items, categories=categories)


# A page to show a selected item with its description
@app.route('/catalog/<string:catalog_name>/items/<string:item_name>')
def showItem(catalog_name, item_name):
    itemCategory = session.query(Items).filter_by(name=item_name).one()
    creator = getUserInfo(itemCategory.user_id)
    if 'username' not in login_session:
        return render_template('publicitemCategory.html', item=itemCategory,
                               creator=creator)
    if creator.id != login_session['user_id']:
        return render_template('publicitemCategory.html', item=itemCategory,
                               creator=creator)
    else:
        return render_template('itemCategory.html', item=itemCategory,
                               creator=creator)


# CRUD - Create a new item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    categories = session.query(Category).filter_by(name=Category.name).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        itemToAdd = Items(name=request.form['name'],
                          description=request.form['description'],
                          category_id=request.form['category'],
                          user_id=login_session['user_id'])
        session.add(itemToAdd)
        session.commit()
        flash("The item '%s' successfully added." % itemToAdd.name)
        return redirect(url_for('catalog'))
    else:
        return render_template('newItem.html', categories=categories)


# CRUD - Update or Edit a selected item
@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editCatalogItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    itemToEdit = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    creator = getUserInfo(itemToEdit.user_id)
    if creator.id != login_session['user_id']:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            itemToEdit.name = request.form['name']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['category']:
            itemToEdit.category_id = request.form['category']
        session.add(itemToEdit)
        session.commit()
        flash("Item '%s' Successfully Edited" % itemToEdit.name)
        return redirect(url_for('showCategoryItems',
                                catalog_name=itemToEdit.category.name))
    else:
        return render_template('edititem.html', item=itemToEdit,
                               categories=categories)


# CRUD - Delete a selected item
@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteCatalogItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Items).filter_by(name=item_name).one()
    categoryName = session.query(Category
                                 ).filter_by(name=category.category.name).one()
    itemToDelete = session.query(Items).filter_by(name=item_name).one()
    creator = getUserInfo(itemToDelete.user_id)
    if creator.id != login_session['user_id']:
        return redirect('/login')
    elif request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("The item has been deleted successfully")
        return redirect(url_for('showCategoryItems',
                                catalog_name=categoryName.name))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# JSON end points which will show all categories and their items
# and description
@app.route('/catalog.JSON')
def categoriesWithItemsJSON():
    everything = []
    categories = session.query(Category).all()
    for category in categories:
        category_items = session.query(Items
                                       ).filter_by(category_id=category.id)
        result = {}
        test = {}
        result['id'] = category.id
        result['category name'] = category.name
        test['test'] = [item.serialize for item in category_items]
        if test['test'] != []:
            result['items'] = [item.serialize for item in category_items]
        everything.append(result)
    return jsonify(Category=everything)


# JSON to show all categories only
@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


# JSON to show a selected category and its items
@app.route('/catalog/<string:catalog_name>/JSON')
def categoryItemsJSON(catalog_name):
    category = session.query(Category).filter_by(name=catalog_name).all()
    for cat_id in category:
        categoryItems = session.query(Items
                                      ).filter_by(category_id=cat_id.id).all()
        return jsonify(categoryItems=[categoryItem.serialize
                                      for categoryItem in categoryItems])


# JSON to show a selected item only
@app.route('/catalog/<string:catalog_name>/items/<string:item_name>/JSON')
def itemJSON(catalog_name, item_name):
    categoryItem = session.query(Items).filter_by(name=item_name).all()
    theItem = categoryItem
    for item in categoryItem:
        theItem = item
    return jsonify(categoryItem=[theItem.serialize])


# This is to create a new user if does not exist
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# A helper function to get a user ID if it exist by their ID
def getUserInfo(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except not user:
        return None


# A helper function to get user ID by their email if it exist
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except not user:
        return None


# Google Connect to get users lgo in by their google accounts
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    # print code
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    # print "done!"
    return output


# This is to disconnect google users (Log Out) from the app
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    # Checking if user is connected or not
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % (
        login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # Delete all login session for the user logged in
    if result['status'] == '200':
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        del login_session['user_id']
        del login_session['gplus_id']
        del login_session['access_token']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Log out is called to check if user is google user to disconnect or other
# accounts. You can add facebook accounts and use this to log them out if
# provider equals facebook and not google. Howerver, we have google only.
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            # print "google is disconnecting"
            gdisconnect()
            flash("You have been logged out successfully.")
        return redirect(url_for('catalog'))
    else:
        print "provider is not Called ERROR"
        flash("You were not logged in")
        return redirect(url_for('catalog'))


# Important to add a the end to run the app
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
