import logging
import time
from gera2ld.pyserve import Host
from gera2ld.socks.server import SOCKS4Handler, SOCKS5Handler, UDPRelayServer

handler_map = {
    4: SOCKS4Handler,
    5: SOCKS5Handler,
}
udp_server = UDPRelayServer()


async def handle(reader, writer, config, feed=b''):
    start_time = time.time()
    if not feed:
        feed = await reader.readexactly(1)
    version, = feed
    Handler = handler_map[version]
    handler = Handler(reader, writer, config, udp_server)
    _name, len_local, len_remote, _error = await handler.handle()
    proxy = handler.config.get_proxy(host=handler.addr[0],
                                     port=handler.addr[1],
                                     hostname=handler.addr[0])
    proxy_log = ' X' + str(proxy) if proxy else ''
    logging.info('SOCKS %s%s %.3fs <%d >%d',
                 Host(handler.addr).host, proxy_log,
                 time.time() - start_time, len_local, len_remote)
