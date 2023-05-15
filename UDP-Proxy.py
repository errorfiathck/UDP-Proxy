from platform import node, system, release; Node, System, Release = node(), system(), release() 
from optparse import OptionParser
import socket
import logging
from time import sleep
from os import system, name; system('clear' if name == 'posix' else 'cls')


r='\033[1;31m'
g='\033[32;1m' 
y='\033[1;33m'
w='\033[1;37m'

def printLow(Str):
    for char in Str:
        print(char, end='', flush=True)
        sleep(.01)

printLow(f'{r}███████╗██████╗ ██████╗  ██████╗ ██████╗               ███████╗██╗ █████╗ ████████╗\n{r}██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗              ██╔════╝██║██╔══██╗╚══██╔══╝\n{w}█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝              █████╗  ██║███████║   ██║   \n{w}██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗              ██╔══╝  ██║██╔══██║   ██║   \n{g}███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║██╗███████╗██╗██║     ██║██║  ██║   ██║   \n{g}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   \n{y}Info:\n    {g}[+] {y}TelegramPv: {w}@Error_fiat\n    {g}[+] {y}Github: {w}https://github.com/errorfiathck\n   \n{y}system:\n    {g}[+] {y}Platform: {w}{System}\n    {g}[+] {y}Node: {w}{Node}\n    {g}[+] {y}Release: {w}{Release}\n\n')


logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def parse_args():
    parser = OptionParser()

    parser.add_option('--bind-address',
                      help='The address to bind, use 0.0.0.0 for all ip address.')
    parser.add_option('--port',
                      help='The port to listen, eg. 623.',
                      type=int)
    parser.add_option('--dst-ip',
                      help='Destination host ip, eg. 192.168.3.101.')
    parser.add_option('--dst-port',
                      help='Destination host port, eg. 623.',
                      type=int)

    return parser.parse_args()

(options, args) = parse_args()


def recv():
    sock_src = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_dst = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_addr = (options.bind_address, options.port)
    dst_addr = (options.dst_ip, options.dst_port)
    sock_src.bind(recv_addr)

    while True:
        data, addr = sock_src.recvfrom(65565)
        if not data:
            logger.error('an error occured')
            break
        logger.debug('received: {0!r} from {1}'.format(data, addr))
        sock_dst.sendto(data, dst_addr)
        data, _  = sock_dst.recvfrom(65565)
        sock_src.sendto(data, addr)

    sock_src.close()
    sock_dst.close()


if __name__ == '__main__':
    parse_args()
    try:
        recv()
    except KeyboardInterrupt:
        exit(0)
