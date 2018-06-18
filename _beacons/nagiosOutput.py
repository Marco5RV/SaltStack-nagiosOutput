# -*- coding: utf-8 -*-
'''
Beacon to monitor multiple services with Nagios
.. versionadded:: 2018.3.0
:depends: null
'''

# Python libss
from __future__ import absolute_import, unicode_literals
import logging
import re
import subprocess 
import time
import math
import os


# Saltstack libs
from salt.ext.six.moves import map

log = logging.getLogger(__name__)

__virtualname__ = 'nagios_output' # Beacon's in the pillar

def __virtual__(): # 
   if __grains__['kernel'] != 'Linux':
     return False, 'This beacon only can be exucute in a linux-base system'
   return __virtualname__
   
def validate(config): # Valid the beacon's syntax
    '''
    Valid the beacon's config
    '''
    # beacon's config must be a list
    
    if not isinstance(config, list): # Checks if the instance is a list 
        return False, ('Invalid configuration'
                       'this beacons must be a list')
    
    return True, 'Valid Configuration'


def beacon(config):
    '''
    Beacon that execute Nagios's plugins in a minion
    .. code-block:: yaml
        beacons:
          nagiosOutput:
            instance_name01: # Name of the instance
              - command: "Command name or route"
              - params: "Command's params"
              - threshold: From which type alerts the beacon will be executed (0 : All alerts, 1: All but "OK", 2: Only CRITICAL and UNKNOWN, 3: Only UNKNOWN )
              - interval: Execute Inverval
            instance_name02: # Name of the next instance
              - command: "Command name or route"
              - params: "Command's params"
              - threshold: From which type alerts the beacon will be executed (0 : All alerts, 1: All but "OK", 2: Only CRITICAL and UNKNOWN, 3: Only UNKNOWN )
              - interval: Execute Inverval 

    '''
    _config = {}
    ret = []
    hashState = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"} # Posible states
    list(map(_config.update, config))    
    # Save all the needed information in the ret variable  
    for key, value in _config.iteritems(): # for each instances
      timeStamp = math.trunc(int(time.time()))
      if os.path.isfile("/executionRutine/"+ key):
        with open("/executionRutine/"+ key, "r") as outfile:
          data = outfile.read()
      else:
        with open("/executionRutine/"+ key, "w+") as outfile:
          outfile.write(str(timeStamp))
        continue         
      try:    
        if timeStamp >= int(data) + int(value['interval']):
          subprocess.check_output(value['command'] + " " + value['params'], shell=True)
          with open("/executionRutine/"+ key, "w") as outfile:
            outfile.write(str(timeStamp))
        else:
          continue
      except subprocess.CalledProcessError as e:
        state = e.returncode
        alertObject ={ 
          "instance": key,
          "output": e.output,
          "state": hashState[state],
          "timeStamp": value['interval']          
        }
      else:
        respond = subprocess.check_output(value['command'] + " " + value['params'], shell=True)
        state = subprocess.check_output('echo $?', shell=True)
        alertObject ={
          "instance": key,
          "output": respond,
          "state": hashState[0],
          "timeStamp": timeStamp, 
        }
      if int(state) >= int(value['threshold']):
        ret.append(alertObject)   
    return ret
