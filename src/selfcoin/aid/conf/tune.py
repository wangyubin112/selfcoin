'''
log file

debug: notice for coders to track the process
info: notice for users
warn: maybe happen, caused by expected failure like transmit failure
error: should not happen, caused by malicious action, but no danger to system
critical: should not happen, caused by system failure or code bug, lead to system crash
'''
import os
import logging
import logging.config
import concurrent_log_handler

filepath = os.path.join(os.path.dirname(__file__), 'logging.py')
logging.config.fileConfig(filepath)
LOGGER = logging.getLogger()


OWN_ID = None
OWN_NAME = None
OWN_PRV_KEY_INT = None
OWN_PUB_KEY_INT_X = None
OWN_PUB_KEY_INT_Y = None


from common import globall as G

# udp for server and group
TX_ATTEMPT = 3
RX_TIMEOUT = 3 # 2s
TX_INTERVAL = 1

# IP_SERVER = 'fe80::20c:29ff:fe94:5a1f' # kali
# IP_SERVER = 'fe80::c4c6:6eb0:d660:ebeb%6' # P50
# IP_SERVER = 'fe80::891:2824:241e:669e%11' # Terrans Force
# IP_SERVER = 'fe80::9764:d3d8:40b0:aaa2%ens33' # Ubuntu of Terrans Force
# IP_SERVER = 'fe80::863e:8db2:5f0d:86b2%enp0s25' # T530
IP_SERVER = '::1'
IP_GROUP = 'ff02::7' # multicast

IP_SERVER = '127.0.0.1' # for test
IP_GROUP = '127.0.0.1' # for test
IP_TEST = '127.0.0.1' # for test


PORT_SERVER = 20001

ADDR_SERVER = IP_SERVER, PORT_SERVER

ADDR_TEST = IP_TEST, PORT_SERVER


# PORT_GROUP_TRADE = 21001
# PORT_GROUP_WATCH = 21002
# PORT_GROUP_POST = 21003

# ADDR_GROUP_TRADE = IP_GROUP, PORT_GROUP_TRADE
# ADDR_GROUP_WATCH = IP_GROUP, PORT_GROUP_WATCH
# ADDR_GROUP_POST = IP_GROUP, PORT_GROUP_POST



TX_BUF = 1024*1024 # note that for my thinkpad with 16G MEM, the maximum tx and rx buf is 2G
RX_BUF = 1024*1024


FO_CH = b'server/data/chain/ver_' + str(G.VER).encode() + b'/'
F_CREDIT = FO_CH + b'credit.db'
'''
folder structure:		
			
server/
	data/
		chain/		
			ver_0/
				credit_DB:					
					restrict_table:
						 ID     |      credit  
						ID_0    |    3 (cheat)
						ID_1    |    2 (bankrupt)
						...			

				ID_0/
					guide_own: i_ch (latest)
					guide_DB:
						    ID        |     own_pay      |     partner_pay  
						ID_POST       |   i_m     i_ch   |   i_m (NULL) i_ch (NULL)
						ID_partner_0  |   i_m     i_ch   |   i_m        i_ch
						ID_partner_1  |   i_m     i_ch   |   i_m        i_ch
						...  									
					
					f_chain_0:
						l_0 (chain info): version of chain file
						l_1: the next close line need to be checked
						l_2-l_3: reserved
						l_4: c_trade
						...
					f_chain_1
					...


				ID_1/
					guide_own: i_ch (latest)
					guide_DB:
						    ID        |     own_pay      |     partner_pay  
						ID_POST       |   i_m     i_ch   |   i_m (NULL) i_ch (NULL)
						ID_partner_0  |   i_m     i_ch   |   i_m        i_ch
						ID_partner_1  |   i_m     i_ch   |   i_m        i_ch
						...    
					
					f_chain_0:
					f_chain_1:
					...

				ID_2/
				.
				.
				.				


'''