#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import hashlib
import webapp2
import os
from google.appengine.ext import db
from google.appengine.ext.webapp import template

signupPath = os.path.join(os.path.dirname(__file__), 'signupform.html')
loginPath = os.path.join(os.path.dirname(__file__), 'loginform.html')
welcomePath = os.path.join(os.path.dirname(__file__), 'welcome.html')


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # def Cookie(self, *a):
    #     return self.response.set_cookie('cookie', *a, path='/', secure=True)

    def Hash_Pass(self, userpassword):
        return hashlib.md5(userpassword).hexdigest()


class UserDetails(db.Model):
    USERNAME = db.StringProperty(required=True)
    PASSWORD = db.StringProperty(required=True)
    EMAILID = db.StringProperty(required=True)
    CREATED = db.DateTimeProperty(auto_now_add=True)
    # this function handles the creation of the datastore kind and entities etc..,


class MainPage(Handler):
    def get(self):
        userName = self.request.cookies.get('user', "")
        template_value = {"userName": userName}
        self.write(template.render(welcomePath, template_value))


class Logout(Handler):
    def get(self):
        self.response.delete_cookie('user')
        # self.response.headers.add_header('Set-Cookie', 'user=')
        self.redirect('/')


class Login(Handler):
    # This function will handles the login protocol deeds
    def get(self):
        template_value = {"error": ""}
        self.write(template.render(loginPath, template_value))

    def post(self):
        userName = self.request.get("userName")
        userPassword = self.request.get("password")
        password = self.Hash_Pass(userPassword)

        if (userName and userPassword):
            q = UserDetails.all().filter('USERNAME =', userName).get()
            if (q.USERNAME == userName and q.PASSWORD == password):
                self.response.headers.add_header('Set-Cookie', '%s=%s' % ("user", str(userName)))
                self.redirect('/')

            else:
                template_value = {
                    "error": "Invalid details",
                    "name": userName,
                    "password": "",
                }
                self.write(template.render(loginPath, template_value))
        else:
            template_value = {
                "error": "Please fill the details",
                "name": userName,
                "password": "",
                "emailId": ""}
            self.write(template.render(loginPath, template_value))


class Signup(Handler):
    def get(self):
        template_value = {"error": ""}
        self.write(template.render(signupPath, template_value))

    def post(self):
        userName = self.request.get("username")
        userPassword = self.request.get("password")
        emailId = self.request.get("emailId")

        password = self.Hash_Pass(userPassword)

        if (userName and password and emailId):
            userDetails = UserDetails(USERNAME=userName, PASSWORD=password, EMAILID=emailId, key_name=userName)
            userDetails.put()

            self.redirect('/')
        else:
            template_value = {
                "error": "plz fil",
                "name": userName,
                "password": password,
                "emailId": emailId
            }
            self.write(template.render(signupPath, template_value))


app = webapp2.WSGIApplication([('/', MainPage), ('/login', Login), ('/signup', Signup), ('/logout', Logout)],
                              debug=True)
