from KE import KE
from KE.client import KE3CONF as CONF


client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'],
            version=3, debug=True)
