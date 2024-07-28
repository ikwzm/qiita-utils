#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json
import mimetypes
import argparse
import time

class QiitaItem:

    TOKEN_FILE = ".qiita_token"        
    
    def __init__(self, dry_run=False, debug_mode=0):
        self.token   = self.load_token()
        self.debug   = debug_mode
        self.dry_run = dry_run
        if self.token == None:
            sys.exit("Not Found Access Token")

    def load_token(self):
        token_file_name = os.path.join(os.getcwd(), self.TOKEN_FILE)
        if os.access(token_file_name, os.R_OK):
            with open(token_file_name, "r") as token_file:
                return token_file.read().strip()

        script_path     = os.path.abspath(__file__)
        script_dir      = os.path.dirname(script_path)
        token_file_name = os.path.join(script_dir, self.TOKEN_FILE)
        if os.access(token_file_name, os.R_OK):
            with open(token_file_name, "r") as token_file:
                return token_file.read().strip()
        return None

    def post(self, title, tags, body, private):
        if self.debug > 0:
            print("## post: ")
            print("##   title:       ", end=""); print(title)
            print("##   tags:        ", end=""); print(tags)
            print("##   private:     ", end=""); print(private)
        headers = {
            "Content-Type":  "application/json",
            "authorization": 'Bearer %s' % (self.token),
        }
        data = {
            "body":    body,
            "private": private,
            "title":   title,
            "tags":    [{"name": tag, "version": []} for tag in tags]
        }
        if self.debug > 1:
            print("## qiita_request: ")
            print("##   header:      ", end=""); print(headers)
            print("##   data:        ", end=""); print(json.dumps(data))
        qiita_resp = requests.post(
            "https://qiita.com/api/v2/items",
            headers = headers,
            data = json.dumps(data),
        )
        if self.debug > 1:
            print("## qiita_response: ")
            print("##   status_code: ", end=""); print(qiita_resp.status_code)
            print("##   headers:     ", end=""); print(qiita_resp.headers)
        qiita_content = qiita_resp.content
        qiita_info    = json.loads(qiita_content.decode())
        if self.debug > 1:
            print("## qiita_info:    ", end=""); print(qiita_info)

        if 'url' in qiita_info:
            info = dict()
            info['url']        = qiita_info['url']
            info['id']         = qiita_info['id']
            info['title']      = qiita_info['title']
            info['created_at'] = qiita_info['created_at']
            info['updated_at'] = qiita_info['updated_at']
            info['tags']       = [tag_dict['name'] for tag_dict in qiita_info['tags']]
            return info
        else:
            return None

    def patch(self, id, title, tags, body, private):
        if self.debug > 0:
            print("## patch: ")
            print("##   id:          ", end=""); print(id)
            print("##   title:       ", end=""); print(title)
            print("##   tags:        ", end=""); print(tags)
            print("##   private:     ", end=""); print(private)
        url = "https://qiita.com/api/v2/items/{id}".format(id=id)
        headers = {
            "Content-Type":  "application/json",
            "authorization": 'Bearer %s' % (self.token),
        }
        data = dict()
        if body != None:
            data["body"   ] = body
        if private != None:
            data["private"] = private
        if title != None:
            data["title"  ] = title
        if len(tags) > 0:
            data["tags"   ] = [{"name": tag, "version": []} for tag in tags]
        if self.debug > 1:
            print("## qiita_request: ")
            print("##   url:         ", end=""); print(url)
            print("##   header:      ", end=""); print(headers)
            print("##   data:        ", end=""); print(json.dumps(data))
        qiita_resp = requests.patch(
            url,
            headers = headers,
            data = json.dumps(data),
        )
        if self.debug > 1:
            print("## qiita_response: ")
            print("##   status_code: ", end=""); print(qiita_resp.status_code)
            print("##   headers:     ", end=""); print(qiita_resp.headers)
        qiita_content = qiita_resp.content
        qiita_info    = json.loads(qiita_content.decode())
        if self.debug > 1:
            print("## qiita_info:    ", end=""); print(qiita_info)

        if 'url' in qiita_info:
            info = dict()
            info['url']        = qiita_info['url']
            info['id']         = qiita_info['id']
            info['title']      = qiita_info['title']
            info['created_at'] = qiita_info['created_at']
            info['updated_at'] = qiita_info['updated_at']
            info['tags']       = [tag_dict['name'] for tag_dict in qiita_info['tags']]
            return info
        else:
            return None

    def get(self, id):
        if self.debug > 0:
            print("## get: ")
            print("##   id:          ", end=""); print(id)
        url = "https://qiita.com/api/v2/items/{id}".format(id=id)
        headers = {
            "Content-Type":  "application/json",
            "authorization": 'Bearer %s' % (self.token),
        }
        if self.debug > 1:
            print("## qiita_request: ")
            print("##   url:         ", end=""); print(url)
            print("##   header:      ", end=""); print(headers)
        qiita_resp = requests.get(
            url,
            headers = headers
        )
        if self.debug > 1:
            print("## qiita_response: ")
            print("##   status_code: ", end=""); print(qiita_resp.status_code)
            print("##   headers:     ", end=""); print(qiita_resp.headers)
        qiita_content = qiita_resp.content
        qiita_info    = json.loads(qiita_content.decode())
        if self.debug > 1:
            print("## qiita_info:    ", end=""); print(qiita_info)

        if 'url' in qiita_info:
            info = dict()
            info['url']        = qiita_info['url']
            info['id']         = qiita_info['id']
            info['title']      = qiita_info['title']
            info['created_at'] = qiita_info['created_at']
            info['updated_at'] = qiita_info['updated_at']
            info['body']       = qiita_info['body']
            info['tags']       = [tag_dict['name'] for tag_dict in qiita_info['tags']]
            return info
        else:
            return None
        
if __name__  == "__main__":
    parser = argparse.ArgumentParser(description='Qiita Post/Patch/Get Itme')
    parser.add_argument('file_name'      , nargs='?', default=None, help='Markdown File Name')
    parser.add_argument('-n', '--dry_run', help='Dry Run'               , action='store_true')
    parser.add_argument('--json'         , help='Output result in json' , action='store_true')
    parser.add_argument('--post'         , help='Post Item'             , action='store_true')
    parser.add_argument('--patch'        , help='Patch user_id'         , action='store', type=str)
    parser.add_argument('--get'          , help='Get user_id'           , action='store', type=str)
    parser.add_argument('-N', '--title'  , help='Qiita Title'           , action='store', type=str)
    parser.add_argument('-T', '--tags'   , help='Qiita Tags'            , action='append')
    parser.add_argument('-d', '--debug'  , help='debug mode'            , action='store', type=int , default=0 )
    private_group = parser.add_mutually_exclusive_group()
    private_group.add_argument('--private', dest='private', action='store_const', const=True ,
                               help='Set private=true')
    private_group.add_argument('--public' , dest='private', action='store_const', const=False,
                               help='Set private=false')
    private_group.set_defaults(private=None)
    with_title_group  = parser.add_mutually_exclusive_group()
    with_title_group.add_argument('--with_title'   , dest='with_title', action='store_const', const=True ,
                                  help='Title is included the Markdown File. Post text without title.')
    with_title_group.add_argument('--without_title', dest='with_title', action='store_const', const=False,
                                  help='Title is not included the Markdown File. Post text as is.')
    with_title_group.set_defaults(with_title=False)
    args = parser.parse_args()

    if args.file_name != None:
        file_name = args.file_name
        lines     = [line.strip() for line in open(file_name)]
    else:
        file_name = None
        lines     = []

    title = None
    if args.with_title == True:
        if lines[0].startswith("# "):
            title = lines[0].removeprefix("# ")
            del lines[:1]
        elif lines[1].startswith("==="):
            title = lines[0]
            del lines[:2]
    if args.title != None:
        title = args.title

    tags = []
    if args.tags != None:
        for tag_list in args.tags: 
            tags = tags + tag_list.split(',')

    if (args.post == True):
        qiita_item = QiitaItem(dry_run=args.dry_run, debug_mode=args.debug)
        if len(lines) == 0:
            sys.exit("Not Body")
        body = "\n".join(lines)
        if title == None:
            sys.exit("Not Title")
        if len(tags) == 0:
            sys.exit("Not Tags")
        if args.private != None:
            private = args.private
        else:
            private = True
        item_info  = qiita_item.post(title, tags, body, private)
        if item_info == None:
            sys.exit("Post Error")
        if args.json == True:
            print(json.dumps(item_info))
        else:
            print(item_info["id"])
    elif (args.patch != None):
        qiita_item = QiitaItem(dry_run=args.dry_run, debug_mode=args.debug)
        qiita_id   = args.patch
        if title == None or len(lines) == 0:
            item_info = qiita_item.get(qiita_id)
            if item_info == None:
                sys.exit("Get Error")
        if title == None:
            title = item_info['title']
        if len(lines) == 0:
            body  = item_info['body']
        else:
            body  = "\n".join(lines)
        item_info  = qiita_item.patch(qiita_id, title, tags, body, args.private)
        if item_info == None:
            sys.exit("Patch Error")
        if args.json == True:
            print(json.dumps(item_info))
        else:
            print("Ok")
    elif (args.get != None):
        qiita_item = QiitaItem(dry_run=args.dry_run, debug_mode=args.debug)
        qiita_id   = args.get
        item_info  = qiita_item.get(qiita_id)
        if item_info == None:
            sys.exit("Get Error")
        if args.json == True:
            print(json.dumps(item_info))
        else:
            print("Ok")
    else:
        parser.print_help()

