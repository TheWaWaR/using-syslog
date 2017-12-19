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

# Benchmark

## Setup rsyslog rate limit for benckmark
```
sudo vim /etc/systemd/journald.conf

  RateLimitInterval=10s
  RateLimitBurst=60000
  
sudo systemctl restart systemd-journald

sudo vim /etc/rsyncd.conf

  $imjournalRatelimitInterval 0
  $imjournalRatelimitBurst 0

sudo systemctl restart rsyslog

```

## Start tornado application with 6 processes

``` bash
python tornado-app.py --log-to-stderr --logging=debug --processes=6

  Args(port=8877, processes=6, redis-key=tornado:2017-12-19_17:47:18)
    
```

## Benchmarking with `wrk`

``` bash
wrk -t12 -c400 -d30s http://127.0.0.1:8877/

    Running 30s test @ http://127.0.0.1:8877/
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency   345.31ms   98.93ms 676.80ms   69.40%
        Req/Sec    97.06     60.68   390.00     67.45%
      30390 requests in 30.05s, 6.40MB read
    Requests/sec:   1089.50
    Transfer/sec:    218.11KB
```

## Count logs (success!!)

``` bash
redis-cli

  127.0.0.1:6379> get tornado:2017-12-19_17:47:18
  "30784"
  
sudo wc -l /var/log/apps/tornado-web.log

  30784 /var/log/apps/tornado-web.log
```
