import os
import asyncio
import socket
import logging
from datetime import datetime
from optparse import OptionParser
from dataclasses import dataclass 


op = OptionParser('OTUServer')
op.add_option('-w', '--workers', default=2, help='Number of workers')
op.add_option('-r', '--docroot', default='./DOC', help='Root directory for documents')
op.add_option('-a', '--adress', default='localhost', help='Server host')
op.add_option('-p', '--port', default=8080, help='Server port')
op.add_option('-b', '--backlog', default=8, help='Server backlog')
opt, arg = op.parse_args()


OK = 200
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
ERRORS = {
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    METHOD_NOT_ALLOWED: "Method not allowed"
}


@dataclass
class Request():
    str_request:str
    error_method: bool = False
        
    def __post_init__(self):
        self.request = self.str_request.split('\r\n')
        self.method = self.request[0][:3]
        self.ver_protocol = self.request[0][-8:]
        self.req_resurs = self.request[0][4:-8]
        self.valid_method()

    def valid_method(self):
        if self.method in ('GET', 'HEAD'):
            self.error_method = True

        
# @dataclass
# class Response():
#     headers: dict = {'Server' : 'otuserver', 'Date' : '', 'Content-Language' : 'ru' }

#     def __post_init__(self):
#         #self.headers['Date'] = datetime.today().strftime("%a, %d %b %Y %I:%m:%S GTM")
#         pass


def pars_reqest(data):
    
    pass


async def handle_client(client, loop, name):
    request = None
    while True:
        request = (await loop.sock_recv(client, 1024)).decode('utf8')
        if len(request) == 0:
            break
        data = Request(request)
        
        print(data.method, data.ver_protocol, data.req_resurs, '\n', name)
        response = request
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()


async def run_server(server, loop):
    while True:
        for i in range(3):
            client, _ = await loop.sock_accept(server)
            loop.create_task(handle_client(client, loop, f'Worker {i}'))


async def main(opt):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with server:    
        server.bind((opt.adress, opt.port))
        server.listen(opt.backlog)
        server.setblocking(False)
        loop = asyncio.get_running_loop()
        log.info('Start -> Server')
        await loop.create_task(run_server(server, loop))


if __name__ == "__main__":
    print(opt)
    logging.basicConfig(
        level=logging.DEBUG, 
        format='[%(asctime)s] %(levelname).1s %(message)s', 
        datefmt='[%H:%M:%S]'
        )
    log = logging.getLogger()
    try:
        asyncio.run(main(opt))
    except Exception:
        pass
    except KeyboardInterrupt:
        pass