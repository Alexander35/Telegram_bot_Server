# Telegram_bot_Server and Notifier_zabbix_package 
This is a simple client-server app for send some messages to the telegram bot. (And receive this in the Telegram Messenger)

It uses a general_server_client and protobuf_asset packages which is implements a client -server intermediate and format of the message.

## Let's do it!

### 1. Install it.
	You need to python 3.6. 
	I recommend you to use a conda for make a virtual enveronment.
###	Install dependencies:

	pip install git+https://github.com/Alexander35/general_server_client.git

	pip install git+https://github.com/Alexander35/protobuf_asset.git

	pip install protobuf

	pip install py-zabbix 
	for (Notifier_zabbix_package)

	pip install pyTelegramBotAPI 
	for (Telegram_bot_Server)

	create working directory for client and server( if you plans to use a one machine) 

	git clone https://github.com/Alexander35/Telegram_bot_Server.git
	for (Telegram_bot_Server)

	git clone https://github.com/Alexander35/Notifier_zabbix_package.git
	for (Notifier_zabbix_package)

### 2. Configure

	make a config.ini files for Notifier_zabbix_package and Telegram_bot_Server

	copy it from .config.ini files in repos and change it 

	Telegram_bot_Server example:

	[SERVER] # Server conf

	Host = localhost # Hostname or IP
	Port = 5555 # TCP Port

	[TELEGRAMBOT] # bot conf

	token = 499992190:AAG53DSDFDFssVfSDFSDFSDFWRWHHH # token from BotFather
	chat_id = -1034534534539990 # number of the chat or channel

	[DAEMON] # Daemon conf for Linux 

	app = app_name # name of service
	pid = /where/your/pid/file.pid # pid file
	chdir = /app/working/directory # working directory

	Notifier_zabbix_package example:

	[SERVER] # We are connects to this server

	Host = 10.55.555.105 # hostname or IP 
	Port = 5555 # TCP port

	[ZABBIX] # zabbix server sesction

	Url = http://10.55.555.106/zabbix/ # zabbix page
	User = Admin # permitted user
	Password = AdminAdminAdmin # password for zabbix user


	Also, you need to configure all the tasks do you have to use for retreiving a data from zabbix server.

	copy file .requests.json to requests.json 
	and write some tasks to it

	All the tasks is a jast zabbix API requests from official documentation 
	https://www.zabbix.com/documentation/3.4/manual/api

	but you should to write only payload staff of the requests
	See the example below:

	#start the file

	{

	#get all known hosts with status 1

	"host.get": 
	[
		{
	    	"status" : 1,
		    "output" :

		    # retreive the values for each host  

			[
				"hostid",
				"host"
			]
		}
	],

	#get all triggers vith value == 1
	#in the output we fetch the output section

	"trigger.get":
	[

		# task number 0

		{
	        "output":
	        [
	        	"triggerid",
	            "description",
	            "priority"
	        ],
	        "filter": 
	        {
	            "value": 1
	        }
		},

		#task number 1
		#this task fetch info about some trigger 15243
	
		{
			"triggerids": "15243",
        	"output":
        	[ 
    			"description", 
    			"value"
    		]
        }
    ]
```}```

In the trigger.get section we have a 2 tasks wich numbered as 0 and 1.

So, you can include any task you need into this file.


### Make a service 

You can make a service to Linux by the folowing steps:

### 2.1 make a .service file

make a .service file like in the example below:
```
[Unit]
Description=TelegramBotServer

[Service]
Type=forking
PIDFile=/path/to/Telegram_bot_Server/pid/telegram-bot-service.pid
WorkingDirectory=/path/to/Telegram_bot_Server

User=uour_user_who_will_use_a_server
Group=group_of_this_user

Environment=RACK_ENV=production

OOMScoreAdjust=-1000

ExecStart=/path/to/Telegram_bot_Server/start.sh
ExecStop=/path/to/Telegram_bot_Server/stop.sh
ExecReload=/path/to/Telegram_bot_Server/restart.sh
TimeoutSec=300

[Install]
WantedBy=multi-user.target
```


where the start.sh contains:
```
\#!/bin/bash
\#some conf staff like a conda env activate 
python telegram_bot.py -d # execute the server in the daemon mode
```
so, stop.sh can be with this stop command:
```
python telegram_bot.py -s 
```
restarts. sh - is a combine file with stop and start comands

### 2.2 Enable service

for setup and enable the service you should to 
put a .service file into a  /etc/systemd/system which includes a users confs

to enable service you should to run
```
sudo systemctl enable SERVICE_NAME
```
### 2.3 Make a cron task for Notifier

use a 
```
crontab -e 
```
a following command invoke hourly a notify.sh with some config of virtual envs or something else and run the zabbix_notifier with two params

[task and number of the subtask in the request.json]
```
00 * * * * /path/to/Notifier_zabbix_package/notify_task.sh trigger.get 0
```
### 3. Work

The Server (Telegram_bot_Server) can use a flags -s for stop or -d for demonize. If you use it without flags - it will run like a standars program with blocking a command line

The Client (Notifier_zabbix_package)

can be start with required params

task and number, where the task is the name of function which will be invoked from requests.json and the Number - is the num from 0 to Number of items .


### Contacts
```
You can send me a mail. if you have some questions
E-mail: alexander.ivanov.35@gmail.com
```