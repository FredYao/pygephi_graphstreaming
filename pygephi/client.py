#!/usr/bin/python
# coding: utf-8
#
# Copyright (C) 2012 André Panisson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Allow a Python script to communicate with Gephi using the Gephi Graph Streaming protocol and plugin.
"""

__author__ = 'panisson@gmail.com'

import urllib2
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except:
        raise "Requires either simplejson or Python 2.6!"

class JSONClient(object):
    
    def __init__(self, autoflush=False):
        self.data = ""
        self.autoflush = autoflush
        
    def flush(self):
        if len(self.data) > 0:
            self._send(self.data)
            self.data = ""
        
    def _send(self, data):
        print 'passing'
        pass
        
    def add_node(self, id, flush=True, **attributes):
        self.data += json.dumps({"an":{id:attributes}}) + '\r\n'
        if(self.autoflush): self.flush()
        
    def change_node(self, id, flush=True, **attributes):
        self.data += json.dumps({"cn":{id:attributes}}) + '\r\n'
        if(self.autoflush): self.flush()
    
    def delete_node(self, id):
        self._send(json.dumps({"dn":{id:{}}}))
    
    def add_edge(self, id, source, target, directed=True, **attributes):
        attributes['source'] = source
        attributes['target'] = target
        attributes['directed'] = directed
        self.data += json.dumps({"ae":{id:attributes}}) + '\r\n'
        if(self.autoflush): self.flush()
    
    def delete_edge(self, id):
        self._send(json.dumps({"de":{id:{}}}))
        
    def clean(self):
        self._send(json.dumps({"dn":{"filter":"ALL"}}))


class GephiClient(JSONClient):
    
    def __init__(self, url='http://127.0.0.1:8080/workspace0', autoflush=False):
        JSONClient.__init__(self, autoflush)
        self.url = url
        
    def _send(self, data):
        conn = urllib2.urlopen(self.url+ '?operation=updateGraph', data)
        return conn.read()
    
class GephiFileHandler(JSONClient):
    
    def __init__(self, out):
        JSONClient.__init__(self, autoflush=True)
        self.out = out
        
    def _send(self, data):
        self.out.write(data)
