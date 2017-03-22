import os
import json
from urllib import request

VPN_PROVIDER = 'http://%s/vpn' % os.environ['VPN_PROVIDER_PORT_80_TCP_ADDR']

class VpnUploaderPipeline:
    def process_item(self, item, spider):
        data = dict(host=item['host'], port=item.get('port'))
        request.urlopen(VPN_PROVIDER, data=json.dumps(data).encode('utf-8'))
        return item
