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
sudo systemctl restart rsyslog
```

## Config python logging module (see: `tornado-app.py`)

``` python
import logging
import logging.config

log_config = {
    'version': 1,
    'formatters': {
        'local': {
            'format': '%(asctime)s %(message)s',
        }
    },
    'handlers': {
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local6',
            'address': '/dev/log',
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
