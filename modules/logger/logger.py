import logging
import syslog
from modules.config.config import Config
#from modules.mqtt.mqtt import Mqtt_Worker
from logging.handlers import RotatingFileHandler

class Logger():
    def __init__(self):
        self.conf = Config().conf
        #self.mqtt = Mqtt_Worker()

        log_formatter=logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        logfile=self.conf['LOGGING']['path']

        handler = RotatingFileHandler(logfile)
        handler.setFormatter(log_formatter)
        handler.setLevel(eval("logging."+self.conf["LOGGING"]["standardlvl"]))
        self.logger=logging.getLogger('Server')
        self.logger.setLevel(eval("logging."+self.conf["LOGGING"]["standardlvl"]))
        self.logger.addHandler(handler)
        syslog.setlogmask(syslog.LOG_UPTO(eval('syslog.LOG_'+self.conf['LOGGING']['syslvl'])))


    def debug(self,msg):
        self.logger.debug(str(msg))
        syslog.syslog(syslog.LOG_DEBUG, str(msg))
        #self.mqtt.send(topic='sign/log/box/debug',payload=str(msg),retain=False)

    def info(self,msg):
        self.logger.info(str(msg))
        syslog.syslog(syslog.LOG_INFO, str(msg))
        #self.mqtt.send(topic='sign/log/box/info', payload=str(msg), retain=False)

    def warning(self,msg):
        self.logger.warning(str(msg))
        syslog.syslog(syslog.LOG_WARNING, str(msg))
        #self.mqtt.send(topic='sign/log/box/warning', payload=str(msg), retain=False)

    def error(self,msg):
        self.logger.error(str(msg))
        syslog.syslog(syslog.LOG_ERR, str(msg))
        #self.mqtt.send(topic='sign/log/box/error', payload=str(msg), retain=False)


    def critical(self,msg):
        self.logger.critical(str(msg))
        syslog.syslog(syslog.LOG_CRIT, str(msg))
        #self.mqtt.send(topic='sign/log/box/critical', payload=str(msg), retain=False)
