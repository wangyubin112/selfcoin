'''
c : card
ch : chain
s : socket
f : file
fo : folder
l : line
m : mutual
i : index
p : position/pointer
G : globall
T : tune

'''


'''

TRADE protocol:
    deferred trade (need server to involve):
        (pay)    demand newest mutual card    --> server
        (server) demand ack                   --> pay
        (pay)    pay                          --> server
        (server) pay ack                      --> pay

        (earn)   demand newest mutual card    --> server
        (server) demand ack                   --> earn
        (earn)   earn                         --> server
        (server) earn ack                     --> earn
        (earn)   earn                         --> group(multicast)

    immediate trade (): 
        (pay)    pay                          --> earn
        (earn)   pay ack                      --> pay
        (earn)   earn                         --> group(multicast)
        
        interact with server for deferred trade:
            (earn)   earn                         --> server
            (server) earn ack                     --> earn

            (pay)    pay                          --> server
            (server) pay ack                      --> pay

POST protocol:
    (post)   launch           --> server
    (server) close            --> post
    if post does not receive close card
    (post)   demand           --> server
    (server) demand ack       --> post

WATCH protocol:








Below is details of each card with protocol of ROOT, POST, CHARGE, REDEEM, TRADE, DEMAND:
ROOT:
    god ROOT:
        version:                                   --> P_VER: 0
        time:                                      --> P_TIME: 1
        type:           ROOT                       --> P_TYPE: 2

        god ID:                                    --> P_ID_GOD: 3
        god ID:                                    --> P_ID_GOD: 4
        mutual index:                              --> P_I_M: 5
        root content hash:                         --> P_POST: 6

        remained coin:   b58encode_int(0)          --> P_COIN_REST: -6 
        previous mutual chain index:               --> P_I_CH_M_PRE: -5
        chain index:     b58encode_int(0)          --> P_I_CH: -4
        previous hash:   real ID hash              --> P_HASH_PRE: -3
        sign:                                      --> P_SIGN: -2
        hash:                                      --> P_HASH: -1

POST:
    node POST:
        version:                                   --> P_VER: 0
        time:                                      --> P_TIME: 1
        type:           POST                       --> P_TYPE: 2

        god ID:                                    --> P_ID_GOD: 3
        post ID:                                   --> P_ID_POST: 4
        mutual index:                              --> P_I_M: 5
        post content hash:                         --> P_POST: 6

        post sign:                                 --> P_SIGN: -2
        post hash:                                 --> P_HASH: -1

    god POST:
        c_post_node: post sign and hash is discard
        
        remained coin:                             --> P_COIN_REST: -6 
        previous mutual chain index:               --> P_I_CH_M_PRE: -5
        chain index:                               --> P_I_CH: -4
        previous hash:                             --> P_HASH_PRE: -3        
        sign:                                      --> P_SIGN: -2
        hash:                                      --> P_HASH: -1

    node POST:
        c_post_god: ack hash is discard

        remained coin:                             --> P_COIN_REST: -6 
        previous mutual chain index:               --> P_I_CH_M_PRE: -5
        chain index:                               --> P_I_CH: -4
        previous hash:                             --> P_HASH_PRE: -3        
        sign:                                      --> P_SIGN: -2
        hash:                                      --> P_HASH: -1


CHARGE: (used in Init: the first root card)
    node charge:
        version:                                    --> P_VER: 0
        time:                                       --> P_TIME: 1
        type:              CHARGE                   --> P_TYPE: 2

        god ID:                                     --> P_ID_GOD: 3
        node ID:                                    --> P_ID_node: 4
        mutual index:           b58encode_int(0)    --> P_I_M: 5
        charge content hash:    hash_ID_real        --> P_POST: 6

        sign:
        hash:
     
    GOD charge: (If TX to charge node directly, use ACK and no need to TX c_charge_node part)
        c_charge_node: hash is discard              --> P_CHARG_NODE: 7
        
        charge coin:            COIN_CREDIT         --> P_COIN_CHRE: 8

        remained coin:                              --> P_COIN_REST: -6         
        pre mutual chain index: b58encode_int(0)    --> P_I_CH_M_PRE: -5
        chain index:                                --> P_I_CH: -4
        pre hash:                                   --> P_HASH_PRE: -3        
        sign:                                       --> P_SIGN: -2
        hash:                                       --> P_HASH: -1

    node charge:
        c_charge_god: hash is discard

        remained coin:          b58encode_int(0)    --> P_COIN_REST: -6        
        pre mutual chain index: b58encode_int(0)    --> P_I_CH_M_PRE: -5
        chain index:            b58encode_int(0)    --> P_I_CH: -4
        pre hash:               b58encode_int(0)    --> P_HASH_PRE: -3        
        sign:                                       --> P_SIGN: -2
        hash:                                       --> P_HASH: -1

REDEEM:
    node redeem:
        version:                                    --> P_VER: 0
        time:                                       --> P_TIME: 1
        type:              REDEEM                   --> P_TYPE: 2

        god ID:                                     --> P_ID_GOD: 3
        node ID:                                    --> P_ID_node: 4
        mutual index:                               --> P_I_M: 5
        redeem content hash:                        --> P_POST: 6

        sign:
        hash:
     
    GOD redeem: (If TX to redeem node directly, use ACK and no need to TX c_charge_node part)
        c_redeem_node: hash is discard
        
        redeem coin:            COIN_CREDIT         --> P_COIN_CHRE: 8

        remained coin:                              --> P_COIN_REST: -6        
        pre mutual chain index:                     --> P_I_CH_M_PRE: -5
        chain index:                                --> P_I_CH: -4
        pre hash:                                   --> P_HASH_PRE: -3        
        sign:                                       --> P_SIGN: -2
        hash:                                       --> P_HASH: -1

    node redeem:
        c_redeem_god: hash is discard

        remained coin:                              --> P_COIN_REST: -6        
        pre mutual chain index:                     --> P_I_CH_M_PRE: -5
        chain index:                                --> P_I_CH: -4
        pre hash:                                   --> P_HASH_PRE: -3        
        sign:                                       --> P_SIGN: -2
        hash:                                       --> P_HASH: -1

TRADE:
    pay:
        version:                                    --> P_VER: 0
        time:                                       --> P_TIME: 1
        type: PAY                                   --> P_TYPE: 2
        
        pay ID:                                     --> P_ID_PAY: 3
        earn ID:                                    --> P_ID_EARN: 4
        mutual index:                               --> P_I_M: 5
        trade coin:                                 --> P_COIN_TRADE: 6
        
        pay remained coin:                          --> P_COIN_REST: -6        
        previous mutual chain index:                --> P_I_CH_M_PRE: -5
        chain index:                                --> P_I_CH: -4
        previous hash:                              --> P_HASH_PRE: -3        
        sign:                                       --> P_SIGN: -2
        hash:                                       --> P_HASH: -1

    earn: (If TX to pay node directly, use ACK and no need to TX c_charge_node part)
        card_pay: pay hash is discarded
               card subtype is change from PAY --> EARN
        earn remained coin:                         --> P_COIN_REST: -6        
        previous mutual chain index:                --> P_I_CH_M_PRE: -5
        chain index:                                --> P_I_CH: -4
        previous hash:        
        sign:
        hash: 

    pay/earn ack(from Aid in deferred trade):
        version:
        time:
        type: ACK
        
        acker(server) ID:                          --> P_ID_ACK
        source card hash:                          --> P_HASH_SRC
        content: success or fail                   --> P_CONTENT

        acker(server) sign:
        acker(server) hash:

DEMAND:
    demand: (TX to Aid or other nodes)
        version:
        time: 
        type: DEMAND
        
        demand(earn) ID:                          --> P_ID_DEMAND: 3
        demanded(pay) ID:                         --> P_ID_DEMANDED: 4
        mutual index:                             --> P_I_M: 5
        chain index:                              -->        

        own(earn) sign:
        own(earn) hash:
        
    demand ack:
        version:
        time:
        type: ACK
        
        acker(server) ID:                        --> P_ID_ACK
        source card hash:                        --> P_HASH_SRC
        content:                                 --> P_CONTENT

        acker(server) sign:
        acker(server) hash:
'''


# card type
ROOT = b'0'
PAY = b'1'
EARN = b'2'
POST = b'3'
CHARGE = b'4'
REDEEM = b'5'
WATCH = b'6' # i_ch
DEMAND = b'7' # i_m
ACK = b'8'


## position of specific attribute in a card
P_VER = 0
P_TIME = 1
P_TYPE = 2

P_ID = 3
P_ID_DEMAND = 3
P_ID_DEMANDED = 4

P_ID_PAY = 3
P_ID_EARN = 4
P_ID_GOD = 3
P_ID_NODE = 4
P_I_M = 5
P_POST = 6

P_COIN_TRADE = 6
P_COIN_REST = -6
P_COIN_CHRE = 8

P_I_CH_M_PRE = -5
P_I_CH = -4
P_HASH_PRE = -3
P_SIGN = -2
P_HASH = -1

# for ack
P_ID_ACK = 3
P_HASH_SRC = 4
P_CONTENT = 5

'''
chain file name:
    example: 'version_ID_index'
    version: for upgrade (different version may have different line len and key len, even change of structure of chain records)
    ID: pub_key (may upgrade to increase len)
    index: for organization (file only contains no more than fixed num of line based on version)
chain file content:
    head:
        line 0 (chain info) version of chain file
        line 1: the next close line need to be checked
        line 2-3: reserved
    body:
        line 4-end:

'''
# LEN_L: len of line, visiable and invisible character, include '\n'
# NUM_L_HEAD: the number of line in head of chain file
# NUM_L_BODY: the number of line in body of chain file

# INDEX_L_MAX = 2**32

VER_0 = b'0' # ver 0 for test
VER_1 = b'1'
VER_PRIVACY = b'10' # to do fo privacy
VER = VER_0
NUM_L_HEAD = 4
NUM_L_BODY = 10**5
LEN_L = 1024 # all character, include '\n'
LEN_ID = 44
LEN_NAME = 20
LEN_KEY = LEN_ID
# CHAIN = {   
#     VER_0: {
#         TRADE: {
#             'LEN_L': 1024, 'NUM_L_HEAD': 4, 'NUM_L_BODY': 10**5
#         },
#         POST: {
#             'LEN_L': 1024, 'NUM_L_HEAD': 4, 'NUM_L_BODY': 10**5
#         }
#     },
#     VER_1: {
#         TRADE: {
#             'LEN_L': 1024, 'NUM_L_HEAD': 4, 'NUM_L_BODY': 10**5
#         },
#         POST: {
#             'LEN_L': 1024, 'NUM_L_HEAD': 4, 'NUM_L_BODY': 10**5
#         }
#     }
# }

NUM_I_M = 2**32

# god node
COIN_CREDIT = 100000
NAME_GOD = b'god'
ID_REAL_GOD_TEST = b'XXXXXX19901211XXXX' # this is for test
ID_REAL_GOD = ID_REAL_GOD_TEST # real ID for god
# key
NUM_B_ODEV = 1