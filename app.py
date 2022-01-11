from flask import Flask,render_template,request,redirect
import random
import requests
import json
from interact_with_DB import interact_db
from flask import jsonify

 # ,render_template,request,redirect
# from interact_with_DB import interact_db
###### App setup
app = Flask(__name__)
app.config.from_pyfile('settings.py')

###### Pages
## Homepage
from pages.homepage.homepage import homepage
app.register_blueprint(homepage)

## About
from pages.about.about import about
app.register_blueprint(about)

## Assignment10
from pages.Assignment10.Assignment10 import assignment10
app.register_blueprint(assignment10)

## Catalog
from pages.catalog.catalog import catalog
app.register_blueprint(catalog)



###### Components
## Main menu
from components.main_menu.main_menu import main_menu
app.register_blueprint(main_menu)




@app.route('/assignment11/outer_source/<variable>')
def req_fronted(variable):
    if(variable=='front'):
        return render_template('outer_source.html',front=True)
    else:
        return render_template('outer_source.html')

def get_users(num):
    users = []
    for i in range(num):
        random_n = random.randint(1, 10)
        res = requests.get(f'https://reqres.in/api/users/{random_n}')
        # res = requests.get ('https://reqres.in/api/users?page=2')
        res = res.json()
        users.append(res)
    return users

@app.route('/assignment11/outer_source_backend')
def req_backend():
    random_n = random.randint(1, 10)
    # if "number" in request.args:
    #     num = int(request.args['number'])
    user =requests.get(f'https://reqres.in/api/users/{random_n}')
    user=user.json()
    return  render_template('outer_source.html',user=user)

@app.route('/assignment11/users')
def users():
    query = 'select * from users;'
    users = interact_db(query=query, query_type='fetch')
    users_json=[]
    content={}
    for user in users:
        content={'id':user[0],'name':user[1],'email':user[2],'create date':user[3],'password':user[4]}
        users_json.append(content)
        content={}
    # return render_template('users_json.html', users=jsonify(users_json))
    return jsonify(users_json)




@app.route  ('/assignment12/restapi_users',defaults={'user_id':-1})
@app.route  ('/assignment12/restapi_users/<int:user_id>')
def db_users_func(user_id):
    if user_id==-1:
        user_dict={}
        query = "select * from users"
        users = interact_db(query=query, query_type='fetch')
        for user in users:
            user_dict[f'user_{user.id}']={
                'name': user.name,
                'email': user.email,
                'orders': 100,
            }
    else:
        query = "select * from users where id='%s';"%(user_id)
        users = interact_db(query=query, query_type='fetch')
        #print(type(user_id)) # print to the console
        if len(users)==0 :
            user_dict={
                'status': 'faild',
                'message':'user not found'
                }
        else:
            user_dict={
                f'id':users[0].id,
                'name':users[0].name,
                'email':users[0].email,
            }
    return jsonify(user_dict)
