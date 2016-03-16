#!/usr/bin/python2

# proxy2 from https://raw.githubusercontent.com/inaz2/proxy2/29b5c525fd462880c08fa1da5f116508bb09ff42/proxy2.py
import proxy2
import re
import ssl
import urlparse
from bs4 import BeautifulSoup


class Proxy(proxy2.ProxyRequestHandler):

    UPSTREAM = 'm.newsmth.net'
    UPSTREAM_COOKIE_DOMAIN = '.newsmth.net'

    SHOW_BLOCKED_SIGN = True
    BLACKLIST = set(i.strip() for i in open('blacklist.txt').readlines() if i.strip() != '')
    URL_UID_REGEXP = re.compile(r'/user/query/(\w+)')
    URL_BLACKLIST_REGEXP = re.compile(r'(/board/\w+(/0)?)|(/article/\w+/\d+)')

    def request_handler(self, req, req_body):
        req.original_host = req.headers['Host']
        req.headers['Host'] = self.UPSTREAM
        req.path = '/' + req.path.split('/', 3)[-1]
        if isinstance(self.connection, ssl.SSLSocket):
            req.path = "https://%s%s" % (req.headers['Host'], req.path)
        else:
            req.path = "http://%s%s" % (req.headers['Host'], req.path)

    def response_handler(self, req, req_body, res, res_body):
        # Modify headers for redirection and cookie domain
        for i, header in enumerate(res.headers.headers):
            key, _, value = header.rstrip().partition(': ')
            if key == 'Location':
                t = urlparse.urlsplit(value)
                if t[1] == self.UPSTREAM:
                    res.headers.headers[i] = 'Location: '\
                                           + urlparse.urlunsplit((t[0], req.original_host) + t[2:])\
                                           + '\r\n'
            elif key == 'Set-Cookie':
                if value.endswith(' domain=' + self.UPSTREAM_COOKIE_DOMAIN):
                    res.headers.headers[i] = 'Set-Cookie: '\
                                           + value.rpartition('; domain=')[0] \
                                           + '; domain='\
                                           + req.original_host.split(':')[0]\
                                           + '\r\n'

        new_page = None
        path = urlparse.urlsplit(req.path)[2]

        # blacklist
        if self.URL_BLACKLIST_REGEXP.match(path):
            soup = BeautifulSoup(res_body, 'html.parser')
            post_list = soup.find(class_='list sec')
            if post_list is not None:
                for post in post_list.children:
                    user = post.find('a', href=self.URL_UID_REGEXP)
                    if user is not None and user.string in self.BLACKLIST:
                        if self.SHOW_BLOCKED_SIGN:
                            new_tag = soup.new_tag('li')
                            new_tag.string = 'BLOCKED'
                            post.replace_with(new_tag)
                        else:
                            post.extract()
                new_page = str(soup)
        return new_page


if __name__ == "__main__":
    proxy2.test(HandlerClass=Proxy)
