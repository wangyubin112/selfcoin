# logging.py
[loggers]
keys=root

[logger_root]
level=DEBUG
handlers=consoleHandler
#consoleHandler, concurrentRotateFileHandler
#,timedRotateFileHandler,errorTimedRotateFileHandler

#################################################
[handlers]
keys=consoleHandler,timedRotateFileHandler,errorTimedRotateFileHandler,rotateFileHandler,errorRotateFileHandler,concurrentRotateFileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

# rotate based on time
[handler_timedRotateFileHandler]
class=handlers.TimedRotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('server/data/log/debug.log', 'h')
# args=('server/data/log/debug.log', when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False)

[handler_errorTimedRotateFileHandler]
class=handlers.TimedRotatingFileHandler
level=WARN
formatter=simpleFormatter
args=('server/data/log/error.log', 'h')

# rotate based on file size
[handler_rotateFileHandler]
class=handlers.RotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('server/data/log/debug.log', 'w', 2000000, 2)
# args=('server/data/log/debug.log', mode='w', maxBytes=2000000, backupCount=2, encoding=None, delay=0)

[handler_errorRotateFileHandler]
class=handlers.RotatingFileHandler
level=WARN
formatter=simpleFormatter
args=('server/data/log/error.log', 'w', 2000000, 2)





## multiprocess log, and rotate based on file size
[handler_concurrentRotateFileHandler]
class=handlers.ConcurrentRotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('server/data/log/debug.log', 'a', 2*1024*1024, 2)








#################################################
[formatters]
keys=simpleFormatter, multiLineFormatter

[formatter_simpleFormatter]
#format= %(levelname)s %(processName)s %(asctime)s:   %(message)s
format=%(asctime)s - %(processName)s - %(threadName)s - %(levelname)s - %(filename)s(line %(lineno)d) - %(funcName)s - %(message)s
#format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[formatter_multiLineFormatter]
format= ------------------------- %(levelname)s -------------------------
 Time:      %(asctime)s
 Thread:    %(threadName)s
 File:      %(filename)s(line %(lineno)d)
 Message:
 %(message)s

datefmt=%Y-%m-%d %H:%M:%S