selfcoin
===


schedule
----
| features                                      | status        |
| --------                                      | :-----:       |
| God init and start                            | Complete      |
| node regist and login                         | Complete      |
| immediate post between node and God           | Complete      |
| immediate charge between node and God         | Complete      |
| immediate trade between nodes                 | Ongoing       |
| Aid init and start                            | TODO          |
| deferred post between node/God and Aid        | TODO          |
| deferred charge between node/God and Aid      | TODO          |
| deferred trade between node and Aid           | TODO          |
| privacy                                       | TODO          |
| security (DB and etc.)                        | TODO          |
| anti-DOS attack                               | TODO          |
| virtual assets interface                      | TODO          |
| optimize                                      | TODO          |


crypto
---
selfcoin/commom/ellipticcurve is referred from https://github.com/starkbank/ecdsa-python. Since it is based on python2, need to be translated to python3. The revises are listed as following:
1. add * before tuple in func parameter and call
2. unicode -> str in fromPem() of der.py (this is for openSSL?)
3. (int, long) -> int in der.py

TODO:
1. The lib fastecdsa is faster using C, replace lib ecdsa-python in release.
2. ECC can not resist quantum computing in the near future, plan to replace it with other algorithm.

