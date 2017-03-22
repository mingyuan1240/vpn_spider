import json
import os
from urllib import request

VPN_REUSE_TIMES = 5
VPN_PROVIDER = 'http://%s/vpn' % os.environ['VPN_PROVIDER_PORT_80_TCP_ADDR']

class ProxyMiddleware:
    def __init__(self):
        self._get_vpn()
        self.request_count = 0
            
    def _get_vpn(self):
        rsp = request.urlopen(VPN_PROVIDER)
        data = json.loads(rsp.read().decode('utf-8'))
        if data is None:
            return None
        if data['ret'] != 0:
            raise 'get vpn failed: %s' % data['msg']
        else:
            self.vpns = data['servers']

    def _next_vpn(self):
        return None
        l = len(self.vpns)
        if self.request_count >= l * VPN_REUSE_TIMES:
            self._get_vpn()
            self.request_count = 0
            
        l = len(self.vpns)
        if l == 0: return None
        else: return self.vpns[self.request_count // l]
    
    def process_request(self, request, spider):
        vpn = self._next_vpn()
        if vpn:
            request.meta['proxy'] = 'http://%s:%d' % (vpn['host'], vpn['port'])
            self.request_count += 1
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.warning("middleware error: %s", exception)
        return None
