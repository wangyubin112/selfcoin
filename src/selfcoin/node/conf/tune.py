import socket
from common import globall as G

# # find the IP address automate
# hostname = socket.gethostname()
# addrs = socket.getaddrinfo(hostname, None)



# udp for clie_ECC_KEYnt
IP_NODE = 'fe80::c4c6:6eb0:d660:ebeb' # for my thinkpad
IP_AID = 'fe80::20c:29ff:fe94:5a1f' # kali
IP_GROUP = 'ff02::7' # multicast

IP_NODE = '127.0.0.1' # for test
IP_AID = '127.0.0.1' # for test
IP_GOD = '127.0.0.1' # for test
IP_GROUP = '224.0.0.1' # for test

IP_GOD = 'fe80::9c2f:2b65:59eb:12dc%enp0s25' # t530
IP_GOD = '10.38.32.134' # old_laptop
# IP_GOD = '10.38.32.141' # t440p
# IP_GOD = 'fe80::1c71:e636:2185:1462' # p50 manjaro

PORT_NODE = 20000
PORT_AID = 20001
PORT_GOD = 20002
PORT_GROUP = 21000


ADDR_NODE = IP_NODE, PORT_NODE
ADDR_AID = IP_AID, PORT_AID
ADDR_GOD = IP_GOD, PORT_GOD
ADDR_GROUP = IP_GROUP, PORT_GROUP



TX_ATTEMPT = 3
RX_TIMEOUT = 3 # 3s
TX_INTERVAL = 1

 
TX_BUF = 1024*1024 # note that for my thinkpad with 16G MEM, the maximum tx and rx buf is 2G
RX_BUF = 1024*1024


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


# credit level
FRIEND = 0 # can be trusted
PARTNER = 1 # not trustworthy, need check
BANKRUPT = 2 # only allow spending coin that is earned
CHEAT = 3 # blacklist


FO_CH = b'node/data/chain/ver_' + G.VER + b'/'
FO_DB = FO_CH + b'db/'
if not os.path.exists(FO_DB):
    os.makedirs(FO_DB)
PATH_CREDIT = FO_DB + b'credit.db'
PATH_GUIDE = FO_DB + b'guide.db'



'''
folder structure:		
			
node/
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
						table_free:
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
						table_guide: 
							ch_0: the last chain index, it is chain index of each ID
							m_1 : the last post mutual index with ID_GOD;
							      the last pay mutual index with ID_node
							ch_1: the last chain index correspond t0 m_1, it is chain index for ID own
							m_2 : the last charge/redeem mutual index with ID_GOD;
							      the last earn mutual index with ID_node
							ch_2: the last chain index correspond to m_2, it is chain index for ID own
							---------------------------------------------------------------------------
							|	ID        |   ch_0   |    m_1    |    ch_1    |    m_2    |    ch_2   |
							---------------------------------------------------------------------------
							---------------------------------------------------------------------------
							|  for own	  |	 ch_last |		   NULL           |        NULL           |
							|-------------------------------------------------------------------------|
							|  ID_OWN         i_ch        NULL        NULL         NULL        NULL   

							---------------------------------------------------------------------------
							|  for GOD	  |	 ch_last |		   post           |     charge/redeem     |
							|-------------------------------------------------------------------------|
							   ID_GOD         i_ch        i_m         i_ch         i_m         i_ch   

							---------------------------------------------------------------------------
							|  for node   |	 ch_last |		    pay           |        earn           |
							|-------------------------------------------------------------------------|
							   ID_node_0      i_ch        i_m         i_ch         i_m         i_ch   
							   ID_node_1      i_ch        i_m         i_ch         i_m         i_ch   
							    ...                                                                   

				ID_OWN/												
					f_chain_0:
						l_0 (chain info): version of chain file
						l_1: the next close line need to be checked
						l_2-l_3: reserved
						l_4: c_trade
						...
					f_chain_1
					...


				ID_GOD_WATCH/
					f_chain_0:
						l_0 (chain info): version of chain file
						l_1: the next close line need to be checked
						l_2-l_3: reserved
						l_4: c_post
						...
					f_chain_1
					...

				ID_0_WATCH/
					f_chain_0:
					f_chain_1:
					...

				ID_1_WATCH/
				.
				.
				.				


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
P_GUIDE_M_PAY = 2
P_GUIDE_CH_PAY = 3
P_GUIDE_M_EARN = 4
P_GUIDE_CH_EARN = 5

P_GUIDE_M_POST = 2
P_GUIDE_CH_POST = 3
P_GUIDE_M_CHRE = 4
P_GUIDE_CH_CHRE = 5

