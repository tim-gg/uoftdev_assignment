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
import webapp2
import jinja2
import os
import flickr
import random

template_dir = os.path.join(os.path.dirname(__file__), 'Templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                              autoescape=True)

flickr.API_KEY = '4058a7100b1de8eda3a30ce8453e8305'
flickr.API_SECRET = '5e7418d854f4c4f1'

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_cookie(self, name):
        username_cookie = self.request.cookies.get(str(name))
        username = None
        if username_cookie:
            user_val = check_secure_val(username_cookie)
            if user_val:
                username = str(user_val)
        return username

class MainHandler(Handler):
    def get(self):
        self.render('front.html', pic='')
    def post(self):
        keyword = self.request.get('keyword')
        photos = flickr.photos_search(tags=keyword)

        if photos:
            p = random.choice(photos)
            url = 'https://farm%s.staticflickr.com/%s/%s_%s.jpg'%(p.farm, p.server, p.id, p.secret)
            print(url)
            self.render('front.html', pic=url)
        else:
            error = "Results Not Found"
            elf.render('front.html', error=error)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
