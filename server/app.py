#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204
# Create a Signup resource with a post() method that responds to a POST /signup request. 
# It should: create a new user; save their hashed password in the database; 
# save the user's ID in the session object; and return the user object in the JSON response.
class Signup(Resource):
    
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        if username and password:
            
            new_user = User(username=username)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            print(new_user)
            session['user_id'] = new_user.id
            
            return new_user.to_dict(), 201

        return {'error': '422 Unprocessable Entity'}, 422

# Add a get() method to your CheckSession resource that responds to a GET /check_session request. 
# If the user is authenticated, return the user object in the JSON response. 
# Otherwise, return an empty response with a 204 status code.

class CheckSession(Resource):
    
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict()
        else:
            return {}, 204

# Create a Login resource with a post() method for logging in that responds to a POST /login request and returns the user as JSON.
class Login(Resource):
    
    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        
        print(username, password)
        user = User.query.filter(User.username == username).first()

        if user.authenticate(password):

            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'error': 'Invalid username or password'}, 401


# Create a Logout resource with a delete() method for logging out that responds to a DELETE /logout request.
class Logout(Resource):
    
    def delete(self):
        session["user_id"] = None

        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
