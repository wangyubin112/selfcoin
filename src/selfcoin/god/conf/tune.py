'''
log file

debug: notice for coders to track the process
info: notice for users
warning: maybe happen, caused by expected failure like transmit failure
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
RX_TIMEOUT = 3 # 3s
TX_INTERVAL = 1

# IP_SERVER = 'fe80::20c:29ff:fe94:5a1f' # kali
# IP_SERVER = 'fe80::c4c6:6eb0:d660:ebeb%6' # P50
# IP_SERVER = 'fe80::891:2824:241e:669e%11' # Terrans Force
# IP_SERVER = 'fe80::9764:d3d8:40b0:aaa2%ens33' # Ubuntu of Terrans Force
# IP_SERVER = 'fe80::863e:8db2:5f0d:86b2%enp0s25' # T530
IP_GOD = '::1'
IP_GROUP = 'ff02::7' # multicast

IP_GOD = '127.0.0.1' # for test
IP_GOD = '10.38.32.134' # old_laptop
# IP_GOD = '10.38.34.133' # manjaro t530
IP_GROUP = '127.0.0.1' # for test


PORT_GOD = 20002

ADDR_GOD = IP_GOD, PORT_GOD


TX_BUF = 1024*1024 # note that for my thinkpad with 16G MEM, the maximum tx and rx buf is 2G
RX_BUF = 1024*1024


FO_CH = b'god/data/chain/ver_' + G.VER + b'/'
FO_DB = FO_CH + b'db/'
if not os.path.exists(FO_DB):
    os.makedirs(FO_DB)
PATH_CREDIT = FO_DB + b'credit.db'
PATH_GUIDE = FO_DB + b'guide.db'

'''
folder structure:		
			
god/
	data/
		chain/		
			ver_0/
				db/
					credit_DB: (to do: encrypt)
						table_own: (it is free for own self)
							 name  |    ID     |    pri_key   |   pub_key_x  |   pub_key_y
							own_0  | ID_own_0  |   
							own_1  | ID_own_1  |   
							...
						table_free: (I do not think it is needed for God)
							 name  |    ID     |      credit  
							aid    |   ID_aid  |    1 (partner)
							god    |   ID_god  |    1 (partner)
							name_0 |   ID_0    |    0 (friend)
							name_1 |   ID_1    |    1 (partner)
							name_2 |   ID_2    |    2 (stranger)
							... 
						table_restrict:
							 ID     |      credit  
							ID_0    |    4 (cheat)
							ID_1    |    3 (bankrupt)
							...

					guide_DB:		
						|----------------------------------------------------------------|
						|   ID        |   ch_0   |   m_1   |  ch_1  |   m_2    |   ch_2  | 
						|-------------|----------|------------------|--------------------|				
						|	          |  latest  |       post       |    charge/redeem   |
						|			  |--------------------------------------------------| 
						| ID_OWN(GOD)     i_ch       NULL    NULL       NULL       NULL  |
						| ID_node_0       NULL       i_m     i_ch       i_m        i_ch  |
						| ID_node_1       NULL       i_m     i_ch       i_m        i_ch  |
						|  ...  		                                                 |
					
				ID_GOD/			
					f_chain_0:
						l_0 (chain info): version of chain file
						l_1: the next close line need to be checked
						l_2-l_3: reserved
						l_4: c_charge/c_post
						...
					f_chain_1
					...	

'''

TA_OWN = 'table_own'
TA_FREE = 'table_free'
TA_RESTRICT = 'table_restrict'


P_OWN_NAME = 0
P_OWN_ID = 1
P_OWN_PRI = 2
P_OWN_PUB_X = 3
P_OWN_PUB_Y = 4

P_FREE_NAME = 0
P_FREE_ID = 1
P_FREE_CREDIT = 2

P_RESTRICT_ID = 0
P_RESTRICT_CREDIT = 1

P_GUIDE_ID = 0
P_GUIDE_CH_LAST = 1
P_GUIDE_M_POST = 2
P_GUIDE_CH_POST = 3
P_GUIDE_M_CHRE = 4
P_GUIDE_CH_CHRE = 5
