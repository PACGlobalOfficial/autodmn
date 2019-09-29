# autodmn


## intro

This script will assist with the conversion of an existing masternode collateral; to be usable with the new DIP0003 masternode rollout in progress with PACGlobal.



## requirements

This script requires that you have python3 installed, as well as the requests library (installable via the python 'pip' utility).
Python3 is available at https://www.python.org (TODO).



## using the script


* Once the wallet has been installed and synchronized; the following fields in your configuration (pacglobal.conf) file must be set at a minimum:

```
server=1
daemon=1
rpcuser=testuser
rpcpass=testpass
rpcbind=127.0.0.1
rpcallowip=127.0.0.1
```

This will allow the script to query the collateral amount in the wallet



* At the command line, then run:

```
python.exe autodmn.py3 1.1.1.1:7112
````

(replacing 1.1.1.1:7112 with the ipaddress of your masternode)

This will result in your protx transaction being sent to the network, and your BLS secret key being printed on the screen (required for the next step).




* Once logged onto your Linux masternode, your pacglobal.conf (on the masternode, not the windows wallet) only needs the one line:

```
masternodeblsprivkey=XXXXXXXXXXXXXXXXXXXXXXX
```

