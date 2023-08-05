#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 ZoomEye Developers (https://www.zoomeye.org)
"""

__author__ = "nixawk"
__version__ = "1.0.6"
__license__ = "GPL-2.0"
__description__ = ("ZoomEye is a search engine for cyberspace "
                   "that lets the user find specific network components"
                   "(ip, services, etc.).")
__classes__ = ["ZoomEye"]
__funcs__ = [
    "login",
    "dork_search",
    "resources_info",
    "show_site_ip",
    "show_ip_port",
    "zoomeye_api_test"
]


import requests
import getpass
import sys


raw_input = raw_input if sys.version_info.major <= 2 else input


class ZoomEye(object):
    def __init__(self, username=None, password=None, api_key=''):
        self.username = username
        self.password = password

        self.token = ''
        self.api_key = api_key
        self.zoomeye_login_api = "https://api.zoomeye.org/user/login"
        self.zoomeye_dork_api = "https://api.zoomeye.org/{}/search"
        self.zoomeye_history_api = "https://api.zoomeye.org/both/search?history=true&ip={}"

    def login(self):
        """Please access https://www.zoomeye.org/api/doc#login
        """
        data = '{{"username": "{}", "password": "{}"}}'.format(self.username,
                                                               self.password)
        resp = requests.post(self.zoomeye_login_api, data=data)
        if resp and resp.status_code == 200 and 'access_token' in resp.json():
            self.token = resp.json().get('access_token')
        return self.token

    def dork_search(self, dork, page=0, resource='host', facet=['ip']):
        """Search records with ZoomEye dorks.

        param: dork
               ex: country:cn
               access https://www.zoomeye.org/search/dorks for more details.
        param: page
               total page(s) number
        param: resource
               set a search resource type, ex: [web, host]
        param: facet
               ex: [app, device]
               A comma-separated list of properties to get summary information
        """
        result = []
        if isinstance(facet, (tuple, list)):
            facet = ','.join(facet)

        zoomeye_api = self.zoomeye_dork_api.format(resource)
        headers = {'Authorization': 'JWT %s' % self.token,
                   'API-KEY': self.api_key,
                  }
        params = {'query': dork, 'page': page + 1, 'facet': facet}
        resp = requests.get(zoomeye_api, params=params, headers=headers)
        if resp and resp.status_code == 200 and 'matches' in resp.json():
            matches = resp.json().get('matches')
            # total = resp.json().get('total')  # all matches items num
            result = matches

            # Every match item incudes the following information:
            # geoinfo
            # description
            # check_time
            # title
            # ip
            # site
            # system
            # headers
            # keywords
            # server
            # domains

        return result
        
    def history_ip(self, ip):
        """Query IP History Information .

        param: ip
        """
        result = []

        zoomeye_api = self.zoomeye_history_api.format(ip)
        headers = {'Authorization': 'JWT %s' % self.token,
                   'API-KEY': self.api_key,
                  }
        resp = requests.get(zoomeye_api, headers=headers)
        if resp and resp.status_code == 200 and 'data' in resp.json():
            matches = resp.json()
            print(matches.get('count'))
            result = matches
        return result

    def resources_info(self):
        """Resource info shows us available search times.

        host-search: total number of available host records to search
        web-search: total number of available web records to search
        """
        data = None
        zoomeye_api = "https://api.zoomeye.org/resources-info"
        headers = {'Authorization': 'JWT %s' % self.token,
                   'API-KEY': self.api_key,
                  }
        resp = requests.get(zoomeye_api, headers=headers)
        if resp and resp.status_code == 200 and 'plan' in resp.json():
            data = resp.json()

        return data


def show_site_ip(data):
    if data:
        for i in data:
            print(i.get('site'), i.get('ip'))


def show_ip_port(data):
    if data:
        for i in data:
            print(i.get('ip'), i.get('portinfo').get('port'))


def zoomeye_api_test():
    zoomeye = ZoomEye()
    zoomeye.api_key = raw_input('ZoomEye API-KEY(If you don\'t use API-KEY , Press Enter): ')
    zoomeye.username = raw_input('ZoomEye Username: ')
    zoomeye.password = getpass.getpass(prompt='ZoomEye Password: ')
    if zoomeye.username != "" and zoomeye.password != "":
        zoomeye.login()
    print(zoomeye.resources_info())

    data = zoomeye.dork_search('solr')
    show_site_ip(data)

    data = zoomeye.dork_search('country:cn')
    show_site_ip(data)

    data = zoomeye.dork_search('solr country:cn')
    show_site_ip(data)

    data = zoomeye.dork_search('solr country:cn', resource='web')
    show_ip_port(data)


if __name__ == "__main__":
    zoomeye_api_test()
