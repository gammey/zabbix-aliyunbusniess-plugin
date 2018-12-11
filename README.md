# zabbix-aliyunbusniess-plugin

1.install aliyun python sdk

pip install aliyun-python-sdk-core aliyun-python-sdk-bssopenapi

2.Submit application for the aliyun bussiness API

http://page.aliyun.com/form/act522746710/index.htm


3.command introduce

python aliyunbusiness.py [objectname] [aliyun-accessid] [aliyun-accesskey]

objectname include :

accountbalance：阿里云账户余额

reminingcdnflow： 阿里云CDN流量包剩余流量

reminingcdn： 阿里云CDN HTTPS请求包剩余请求次数


4.Config zabbix-agentd 

Add the next line to the zabbix-agentd.conf:

UserParameter=aliyun.business[*],python /[script path]/aliyunbusiness.py $1 $2 $3

Reload zabbix-agentd


5.Add Item

if your accessid is "aliyunaccessid" and your accesskey = "aliyunaccesskey" 

Item key : aliyun.business[accountbalance,aliyunaccessid,aliyunaccesskey]

Type of information :Numeric(float).

Units : ￥

Item key : aliyun.business[reminingcdnflow,aliyunaccessid,aliyunaccesskey]

Type of information :Numeric(float).

Units : GB

Item key : aliyun.business[reminingcdn,aliyunaccessid,aliyunaccesskey]

Type of information :Numeric(float).

Units : Times


