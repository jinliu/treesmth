#!/usr/bin/python2


import proxy2
import ssl


class Proxy(proxy2.ProxyRequestHandler):
    UPSTREAM = 'm.newsmth.net'

    def request_handler(self, req, req_body):
        req.headers['Host'] = self.UPSTREAM
        req.path = '/' + req.path.split('/', 3)[-1]
        if isinstance(self.connection, ssl.SSLSocket):
            req.path = "https://%s%s" % (req.headers['Host'], req.path)
        else:
            req.path = "http://%s%s" % (req.headers['Host'], req.path)


if __name__ == "__main__":
    proxy2.test(HandlerClass=Proxy)
