import os

import web

env = os.environ.get("WEB_ENV", "development")
print "Environment: %s" % env

#DB = web.database(dbn='postgres', db='app', user='fixme', pw='')

# Default settings. Override below
web.config.debug = True
cache = False
email_errors = ''
web.config.smtp_server='127.0.0.1'
web.config.smtp_port=25

if env == 'production':
    web.config.debug = False
    cache = True
    email_errors = 'fixme@example.com'
elif env == 'staging':
    dac_host = '192.168.1.1:8000'
    web.config.debug = True
    cache = False
    email_errors = 'fixme@example.com'

elif env == "test":
    pass
    #DB = web.database(dbn='postgres', db='app_test', user='fixme', pw='')
