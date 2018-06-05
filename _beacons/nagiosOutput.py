# -*- coding: utf-8 -*-
'''
Beacon to monitor multiple services with Nagios
.. versionadded:: 2018.3.0
:depends: null
'''

# Python libs
from __future__ import absolute_import, unicode_literals
import logging
import re
import subprocess 
import time
import math

# Saltstack libs
from salt.ext.six.moves import map

log = logging.getLogger(__name__)

__virtualname__ = 'nagiosOutput' # Beacon's in the pillar

def __virtual__(): # 
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
    timeStamp = math.trunc(int(time.time()))  # timeStamp to compare the interval given
    list(map(_config.update, config))    
    # Save all the needed information in the ret variable
    for key, value in _config.iteritems(): # for each instances
      if timeStamp % int(value['interval']) != 0:
        continue      
      try:
        subprocess.check_output(value['command'] + " " + value['params'], shell=True)
      except subprocess.CalledProcessError as e:
        state = e.returncode
        alertObject ={ 
          "instance": key,
          "output": e.output,
          "state": hashState[state]
        }
      else:
        respond = subprocess.check_output(value['command'] + " " + value['params'], shell=True)
        state = subprocess.check_output("echo $?", shell=True) 
        alertObject ={
          "instance": key,
          "output": respond,
          "state": hashState[int(state)]
        }
      if int(state) >= int(value['threshold']):
        ret.append(alertObject)   
return ret
