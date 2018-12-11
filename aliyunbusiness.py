#!/usr/bin/python
# coding: utf-8
import json
import sys
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkbssopenapi.request.v20171214 import QueryAccountBalanceRequest
from aliyunsdkbssopenapi.request.v20171214 import QueryResourcePackageInstancesRequest

from aliyunsdkcore.profile import region_provider

#request = QueryResourcePackageInstancesRequest.QueryResourcePackageInstancesRequest();
#request = QueryAccountBalanceRequest.QueryAccountBalanceRequest()
#request = QueryAvailableInstancesRequest.QueryAvailableInstancesRequest()

def getAccountBalance(client):
	request = QueryAccountBalanceRequest.QueryAccountBalanceRequest()
	response = client.do_action_with_exception(request)
	return json.loads(response)["Data"]["AvailableAmount"];


def getReMiningCDNFlow(client):
	request = QueryResourcePackageInstancesRequest.QueryResourcePackageInstancesRequest()
	request.set_ProductCode('cdnflowbag');
	response = client.do_action_with_exception(request);
	unitKV = {"B":1,"KB":1024,"MB":1024*1024,"GB":1024*1024*1024,"TB":1024*1024*1024*1024};
	reminingFlow = 0;
	for i in json.loads(response)["Data"]["Instances"]["Instance"]:
		flow = float(i["RemainingAmount"]);
		unit = i["RemainingAmountUnit"];
		reminingFlow = reminingFlow + unitKV[unit] * flow
	return reminingFlow/1024/1024/1024;

def getReMiningCDN(client):
	request = QueryResourcePackageInstancesRequest.QueryResourcePackageInstancesRequest()
        request.set_ProductCode('CDN');
        response = client.do_action_with_exception(request);
	reCDN = float(0);
	for i in json.loads(response)["Data"]["Instances"]["Instance"]:
		if i["RemainingAmountUnit"] == u"万次":
			reCDN = reCDN + float(i["RemainingAmount"])*10000;
		elif i["RemainingAmountUnit"] == u"亿次":
			reCDN = reCDN + float(i["RemainingAmount"])*100000000;
		else:
			reCDN = reCDN + float(i["RemainingAmount"])
	return reCDN;
		

def main():
	fDic = {"accountbalance":getAccountBalance,"reminingcdnflow":getReMiningCDNFlow,"reminingcdn":getReMiningCDN};
	region_provider.modify_point('BssOpenApi', 'business', 'business.aliyuncs.com')
	try:
		aid = sys.argv[2];
		akey = sys.argv[3];
		client = AcsClient(
   			aid,
   			akey,
   			"business"
			);
	except:
		print "please input accessid & accesskey."
	try:
		arg = sys.argv[1];
		print fDic[arg](client);
	except ServerException:
		print "accessid or accesskey error.";
	except KeyError:
		print "unkown args.please input [accountBalance|reminingcdnflow|reminingcdn]"
	

if __name__ == '__main__':
  main()