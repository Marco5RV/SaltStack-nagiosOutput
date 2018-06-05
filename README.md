# SaltStack-nagiosOutput
Customized beacon to execute nagios plugins in a salt-minion with multiple instances 

# Usage
In order to make possible to use this beacon, the nagiosOutput.py should be placed in a "\__beacon_" named folder in one of our file_roots. More information of [file_roots](https://docs.saltstack.com/en/latest/topics/tutorials/states_pt4.html) and [custumized modules](https://docs.saltstack.com/en/latest/ref/modules/) in the [SaltStack documentation](https://docs.saltstack.com/en/latest/contents.html)

Now we'll move on to an example:
### Schema in yaml code
```
beacons:
  nagiosOutput:
    - instance01:  # Name of the instance
      command: "Command name or route"
      params: "Command's params"
      threshold: From which type alerts the beacon will be executed
      interval: Execution interval
    - instance02:
      command:
      params:
      threshold:
      interval:
      .
      .
      .
    - instanceN
      command:
      params:
      threshold:
      interval:
```

- Command data type must be a string 
- params data type must be a string 
- threshold data type must be an integer between 0 and 3 both included ( 0 : All alerts, 1: All but "OK", 2: Only CRITICAL and UNKNOWN, 3: Only UNKNOWN ) 
- interval must be an integer 

### Working example
```
beacons:
  nagiosOutput:
    - icmp_check:
        command: check_icmp
        params: 8.8.8.8
        threshold: 0
        interval: 60
```
In the salt event bus we should see, something like this:
```
salt/beacon/<Minion-name>/nagiosOutput/	{
    "_stamp": "<TimeStamp>", 
    "id": "<Minion-id>", 
    "instance": "icmp_check", 
    "output": "OK - 8.8.8.8: rta 30.042ms, lost 0%|rta=30.042ms;200.000;500.000;0; pl=0%;40;80;; rtmax=30.159ms;;;; rtmin=29.986ms;;;; \n", 
    "state": "OK"
}
```
# Comments
This beacon solves a very specific situation.
This beacon will work only in Linux based systems.
this beacon has much room for improvement especially in the interval part
