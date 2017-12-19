# using-syslog
How to use syslog. application examples &amp; rsyslog configurations.

# Basic Goals
* [x] Multiple process support, high performace (powered by rsyslog)
* [x] Seprate log file by application name
* [x] Log with python std logging module (No need to change current code)
* [x] Log rotate by file size (50MB)
  - Previous file: app-logfile.log.1
  - More archives: app-logfile.log.2.gz, app-logfile.log.3.gz, app-logfile.log.4.gz
  - Remove older log file

# References
* How to configure logging to syslog in Python?
  - https://stackoverflow.com/a/3969772/1274372
* Basic Configuration of Rsyslog
  - https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/s1-basic_configuration_of_rsyslog
* What is the local6 (and all other local#) facilities in syslog?
  - https://unix.stackexchange.com/questions/90842/what-is-the-local6-and-all-other-local-facilities-in-syslog
* Working With Queues In Rsyslog
  - https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/s1-working_with_queues_in_rsyslog
* Centos/Linux setting logrotate to maximum file size for all logs
  - https://stackoverflow.com/a/23728801/1274372
