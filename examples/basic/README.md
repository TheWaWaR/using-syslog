# Config Steps

## Config systemd journual

``` bash
sudo vim /etc/systemd/journald.conf

  RateLimitInterval=30s
  RateLimitBurst=60000
  
sudo systemctl restart systemd-journald
```

## Config rsyslog (see: `rsyslog-local6-tornado-web.conf`)

``` bash
sudo mkdir /var/log/apps
sudo vim /etc/rsyncd.conf

  $imjournalRatelimitInterval 30
  $imjournalRatelimitBurst 60000

sudo cp rsyslog-local6-tornado-web.conf /etc/rsyslog.d/00-local6-tornado-web.conf
sudo systemctl restart rsyslog
```

## Config logrotate (see: `logrotate-tornado-web.conf`)

``` bash
sudo cp logrotate-apps.conf /etc
# [Ref]: https://stackoverflow.com/a/23728801/1274372
sudo cp logrotate-apps.cron /etc/cron.hourly
```

## Config python logging module (see: `tornado-web.py`)

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
