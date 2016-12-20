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
import random
import string
import os
import json
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

signupPath = os.path.join(os.path.dirname(__file__), 'signupform.html')
loginPath = os.path.join(os.path.dirname(__file__), 'loginform.html')
welcomePath = os.path.join(os.path.dirname(__file__), 'welcome.html')
blogviewpath = os.path.join(os.path.dirname(__file__), 'BlogView.html')


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # def Cookie(self, *a):
    #     return self.response.set_cookie('cookie', *a, path='/', secure=True)

    def Hash_Pass(self, userpassword):
        return hashlib.md5(userpassword).hexdigest()

    def random_generator(self):
        return ''.join([random.choice(string.ascii_uppercase + string.digits) for x in range(6)])


class UserDetails(ndb.Model):
    USERNAME = ndb.StringProperty(required=True)
    PASSWORD = ndb.StringProperty(required=True)
    EMAILID = ndb.StringProperty(required=True)
    CREATED = ndb.DateTimeProperty(auto_now_add=True)

    # this function handles the creation of the datastore kind and entities etc..,


class Cookies(ndb.Model):
    USER = ndb.StringProperty(required=True)
    COOKIE = ndb.StringProperty(required=True)


class UserBlogDetails(ndb.Model):
    USERNAME = ndb.StringProperty(required=True)
    TITILE = ndb.StringProperty(required=True)
    HEADING = ndb.StringProperty(required=True)
    DISCRIPTION = ndb.StringProperty(required=True)
    CREATED = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
    def get(self):
        blogcontent = UserBlogDetails.query().order(-ndb.DateTimeProperty('CREATED'))
        cookie = self.request.cookies.get('user', "")

        if (cookie == ""):
            template_value = {"userName": "",
                              "blogcontent": blogcontent
                              }
            self.write(template.render(welcomePath, template_value))

        else:
            user = Cookies.query(Cookies.COOKIE == cookie).get()

            template_value = {"userName": str(user.USER),
                              "blogcontent": blogcontent
                              }
            self.write(template.render(welcomePath, template_value))
            #
            # def post(self):
            #     blogcontents = UserBlogDetails.query().order(-ndb.DateTimeProperty('CREATED'))
            #     for blogcontent in blogcontents:
            #         self.response.out.write(
            #             '<button>View</button><h>Title: %s</h> &nbsp;&nbsp; <h>UserName: %s</h><br><hr> ' % (
            #                 blogcontent.TITILE, blogcontent.USERNAME))


class Logout(Handler):
    def get(self):
        self.response.delete_cookie('user')
        self.redirect('/')


class Login(Handler):
    # This function will handles the login protocol deeds
    # def get(self):
    #     template_value = {"error": ""}
    #     self.write(template.render(loginPath, template_value))

    def post(self):
        userName = self.request.get("userName")
        userPassword = self.request.get("password")
        password = self.Hash_Pass(userPassword)

        if (userName and userPassword):
            # q = UserDetails.query(ndb.StringProperty('USERNAME ')== userName)
            # q= UserDetails.get_by_id(userName)
            if UserDetails.query(UserDetails.USERNAME == userName).get():
                user = UserDetails.query(UserDetails.USERNAME == userName).get()
                u = Cookies.query(Cookies.USER == userName).get()
                if user.PASSWORD == password:
                    self.response.headers.add_header('Set-Cookie', '%s=%s' % ("user", str(u.COOKIE)))
                else:
                    self.response.out.write("Invalid username or password")
            else:
                # template_value = {
                #     "error": "Invalid details",
                #     "name": userName,
                #     "password": "",
                # }
                self.response.out.write("Invalid user details")
        else:
            # template_value = {
            #     "error": "Please fill the details",
            #     "name": userName,
            #     "password": "",
            #     "emailId": ""}
            # self.write(template.render(loginPath, template_value))
            self.response.out.write("please fill the fields")


class Signup(Handler):
    def get(self):
        template_value = {"error": ""}
        self.write(template.render(signupPath, template_value))

    def post(self):
        userName = self.request.get("username")
        userPassword = self.request.get("password")
        emailId = self.request.get("emailId")
        password = self.Hash_Pass(userPassword)
        secure = self.random_generator()

        if (userName and password and emailId):

            if (UserDetails.query().filter(UserDetails.USERNAME == userName).get()):
                template_value = {
                    "error": "username already exist",
                    "name": "",
                    "password": "",
                    "emailId": emailId
                }
                self.write(template.render(signupPath, template_value))
            else:
                secure = self.Hash_Pass(self.random_generator())
                Cookie = Cookies(USER=userName, COOKIE=secure)
                Cookie.put()
                userDetails = UserDetails(USERNAME=userName, PASSWORD=password, EMAILID=emailId, id=secure)
                userDetails.put()
                self.redirect('/')
        else:
            template_value = {
                "error": "please fill all the fields",
                "name": userName,
                "password": "",
                "emailId": emailId
            }
            self.write(template.render(signupPath, template_value))


class BlogCreation(Handler):
    def get(self):
        title = self.request.get("title")
        heading = self.request.get("heading")
        discription = self.request.get("discription")
        if (title and heading and discription):
            cookie = self.request.cookies.get('user', "")
            user = Cookies.query(Cookies.COOKIE == cookie).get()
            userBlogForm = UserBlogDetails(TITILE=title, HEADING=heading, DISCRIPTION=discription,
                                           USERNAME=str(user.USER))
            userBlogForm.put()
        else:
            self.response.out.write("Please fill the all the fields")


class BlogContent(Handler):
    def get(self, id):
        q = UserBlogDetails.get_by_id(int(id))
        c = list(str(q.CREATED))
        template_value = {"title": str(q.TITILE),
                          "heading": str(q.HEADING),
                          "discription": str(q.DISCRIPTION),
                          "username": str(q.USERNAME),
                          "id": ''.join(id[23:-1]),
                          "created": ''.join(c[0:16])
                          }
        self.write(template.render(blogviewpath, template_value))


class DeleteBlog(Handler):
    def post(self):
        id = self.request.get("id")
        q = UserBlogDetails.get_by_id(int(id))
        # q.key.delete()
        q.key.delete()
        self.response.out.write("Successfully deleted!")
        self.redirect('/')



class BlogEdit(Handler):
    def get(self, id):
        q = UserBlogDetails.get_by_id(int(id))
        c = list(str(q.CREATED))
        template_value = {"etitle": str(q.TITILE),
                          "eheading": str(q.HEADING),
                          "ediscription": str(q.DISCRIPTION),
                          "username": str(q.USERNAME),
                          "created": ''.join(c[0:16]),
                          "id": id
                          }
        self.write(template.render(blogviewpath, template_value))

    def post(self, id):
        etitle = self.request.get("etitle")
        eheading = self.request.get("eheading")
        ediscription = self.request.get("ediscription")
        q = UserBlogDetails.get_by_id(int(id))
        q.TITILE = etitle
        q.HEADING = eheading
        q.DISCRIPTION = ediscription
        q.put()
        self.redirect('/')



        # c = list(str(q.CREATED))
        # template_values = {"title": str(q.TITILE),
        #                    "heading": str(q.HEADING),
        #                    "discription": str(q.DISCRIPTION),
        #                    }
        # # json.dumps is used to convert the python dictionary objects to json objects
        # test = json.dumps(template_values)
        # self.response.out.write("editing is working")

        # def post(self):
        #     title = self.request.get("title")
        #     etitle = self.request.get("etitle")
        #     eheading = self.request.get("eheading")
        #     ediscription = self.request.get("ediscription")
        #     if (etitle and eheading and ediscription):
        #         q = UserBlogDetails.query(UserBlogDetails.TITILE == title).get()
        #         q.TITILE = etitle
        #         q.HEADING = eheading
        #         q.DISCRIPTION = ediscription
        #         q.put()
        #     else:
        #         self.response.out.write("Please fill the all the fields")


app = webapp2.WSGIApplication(
    [('/', MainPage), ('/login', Login), ('/signup', Signup), ('/logout', Logout), ('/blogcreation', BlogCreation),
     ('/blogcontent/(\d+)', BlogContent), ('/deleteblog', DeleteBlog), ('/blogedit/(\d+)', BlogEdit)],
    debug=True)


# for blogcontent in blogcontents.iter( ):
# it to iterate the perticular proper
#      test = ""+ str(blogcontent)
# blogcontents = UserBlogDetails.query().fetch() it is used to get the complete kind from the data store
# blogcontents = UserBlogDetails.query().order(ndb.DateTimeProperty('CREATED')) it is used to create an ordered list
