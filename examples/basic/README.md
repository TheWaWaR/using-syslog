# Config Steps

## Config systemd journual

``` bash
sudo vim /etc/systemd/journald.conf

  RateLimitInterval=30s
  RateLimitBurst=50000
  
sudo systemctl restart systemd-journald
```

## Config rsyslog

``` bash
sudo vim /etc/rsyncd.conf

  $ModLoad imjournal
  $imjournalRatelimitInterval 30
  $imjournalRatelimitBurst 50000

sudo cp rsyslog-local6.conf /etc/rsyslog.d/00-local6-tornado.conf

  if $syslogfacility-text == 'local6' and $syslogtag startswith 'python' then /var/log/tornado-app.log
  & ~
  
sudo systemctl restart rsyslog
```

## Config python logging module (see: `tornado-app.py`)

``` python
import logging
import logging.config
import logging.handlers

class MySysLogHandler(logging.handlers.SysLogHandler):

    def __init__(self, **kwargs):
        ident = kwargs.pop('ident', 'python')
        kwargs.setdefault('facility', 'local6')
        kwargs.setdefault('address', '/dev/log')
        super(MySysLogHandler, self).__init__(**kwargs)
        self.ident = ident

    def format(self, record):
        msg = super(MySysLogHandler, self).format(record)
        return u'{}[{}]: {}'.format(self.ident, record.process, msg)
        
log_config = {
    'version': 1,
    'formatters': {
        'local': {
            'format': '%(asctime)s %(message)s',
        }
    },
    'handlers': {
        'syslog': {
            'class': '{}.MySysLogHandler'.format(__name__),
            'formatter': 'local',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['syslog']
    },
}
logging.config.dictConfig(log_config)

logging.info('Some thing happened!')
```
