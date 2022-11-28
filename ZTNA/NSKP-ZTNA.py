####################################################################################################
#
# Title : List publishers’ and private apps information leveraging restapiv2
# Description : This script retrieves the list of publishers and private apps
# Date : 2/03/2022
# Version :v1.2
# Usage :This is for POC purposes only.
# Notes :
# Python_version :v3
#
####################################################################################################
# version : 1.0 , First release
# version : 1.1 , Adding Publish DNS field into the table (listprivapp)
# version : 1.2 , Adding Lite privapp version table
####################################################################################################

#!/usr/bin/python

import urllib3
import json
import ssl
import requests
import argparse
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from prettytable import PrettyTable


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tenant", help="Tenant name. '.goskope.com' not necessary.")
parser.add_argument("-k", "--apikey", help="Api Key v2.")
parser.add_argument("-a", "--action", help="Options: listpublisher / listprivapps / listprivappslite")
args = parser.parse_args()

url = "https://" + args.tenant + ".goskope.com/api/v2"

payload={}
headers = { 'Netskope-Api-Token': args.apikey }



def listprivapps (args):
  #response_privapps = requests.request("GET", url + "/steering/apps/private", headers=headers, data=payload, verify=False)

  response_privapps = requests.get(url + "/steering/apps/private", headers=headers, data=payload, verify=False)
  json_data_privapps = json.loads(response_privapps.text)

  response_publishers = requests.request("GET", url + "/infrastructure/publishers", headers=headers, data=payload, verify=False)
  json_data_publishers = json.loads(response_publishers.text)

  y = json.dumps(response_publishers.text)
  countingy = y.count("assessment")
  z = json.dumps(response_privapps.text)
  countingz = z.count("host")

  x = PrettyTable(["Private App name", "Host", "Clientless", "Reachable", "Publisher Name", "Publisher DNS", "TCPlist", "UDPlist"])
  x.align["Private App name"] = "l"
  x._max_width = {"Host": 20, "Publisher Name": 30, "TCPlist" : 40, "UDPlist" : 40}
  x.padding_width = 1

  count = 0
  for json_data in json_data_privapps:
    Private_Name = json_data_privapps['data']['private_apps'][count]['app_name']
    host = json_data_privapps['data']['private_apps'][count]['host']
    clientless = json_data_privapps['data']['private_apps'][count]['clientless_access']
    PublisherDNS = json_data_privapps['data']['private_apps'][count]['use_publisher_dns']
    if json_data_privapps['data']['private_apps'][count]['reachability'] == None:
      Reachable = "N/A"
    else:
      if json_data_privapps['data']['private_apps'][count]['reachability']['reachable'] == True:
        Reachable = ('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
      else:
        Reachable = ('\x1b[6;33;41m' + 'Error!' + '\x1b[0m')

    Publisherlist = []
    for i in range(len(json_data_privapps['data']['private_apps'][count]['service_publisher_assignments'])):
      Publisherlist.append (json_data_privapps['data']['private_apps'][count]['service_publisher_assignments'][i]['publisher_id'])

    count2 = 0
    Publisherlistname = []
    for i in (Publisherlist):
      if json_data_publishers['data']['publishers'][count2]['publisher_id'] in Publisherlist:
          Publisherlistname.append (json_data_publishers['data']['publishers'][count2]['publisher_name'])
          count2 += 1

    TCPlist = []
    UDPlist = []
    count3 = 0

    for i in range(len(json_data_privapps['data']['private_apps'][count]['protocols'])):
      if json_data_privapps['data']['private_apps'][count]['protocols'][count3]['transport'] == "tcp":
        TCPlist.append (json_data_privapps['data']['private_apps'][count]['protocols'][count3]['port'])
        count3 += 1

      else:
        UDPlist.append (json_data_privapps['data']['private_apps'][count]['protocols'][count3]['port'])
        count3 += 1

    x.add_row([Private_Name, host, clientless, Reachable, Publisherlistname, PublisherDNS, TCPlist, UDPlist ])

    count += 1
    x.hrules = 1

  print(x)




def listpublisher (args):
  response_publishers = requests.request("GET", url + "/infrastructure/publishers", headers=headers, data=payload, verify=False)
  getreponse_json = json.loads(response_publishers.text)

  x = PrettyTable(["Publisher name", "CN", "IP Address", "Version", "Registered", "Status"])
  x.align["Publisher name"] = "l"
  x.padding_width = 1

  y = json.dumps(response_publishers.text)
  counting = y.count("assessment")
  count = 0

  while count < counting:
    Publisher_Name = getreponse_json['data']['publishers'][count]['publisher_name']
    CN = getreponse_json['data']['publishers'][count]['common_name']
    Registered = getreponse_json['data']['publishers'][count]['registered']
    if getreponse_json['data']['publishers'][count]['assessment'] == None:
      IP = "N/A"
      Version = "N/A"
    else:
      IP = getreponse_json['data']['publishers'][count]['assessment']['ip_address']
      Version = getreponse_json['data']['publishers'][count]['assessment']['version']
      
    if getreponse_json['data']['publishers'][count]['status'] == "connected":
      Status = ('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
    else:
      Status = ('\x1b[6;33;41m' + 'Error!' + '\x1b[0m')
    x.add_row([Publisher_Name,CN, IP, Version, Registered, Status])
    count += 1

  print(x)


def listprivappslite (args):

  response_privapps = requests.get(url + "/steering/apps/private", headers=headers, data=payload, verify=False)
  json_data_privapps = json.loads(response_privapps.text)

  z = json.dumps(response_privapps.text)
  countingz = z.count("host")

  x = PrettyTable(["Host", "ID", "PublisherDNS"])
  x.align["Host"] = "l"
  x._max_width = {"Host": 40}
  x.padding_width = 1

  count = 0
  for json_data in json_data_privapps:
    host = json_data_privapps['data']['private_apps'][count]['host']
    print (host)
    ID = json_data_privapps['data']['private_apps'][count]['app_id']
    PublisherDNS = json_data_privapps['data']['private_apps'][count]['use_publisher_dns']

    x.add_row([host, ID, PublisherDNS])

    count += 1
    x.hrules = 1

  print(x)



def noaction ():
  #defaulterrormessage
  print ("")
  print ("No action selected. Please review help for more information.")
  print ("")

if __name__ == "__main__":
  if args.action == "listprivapps":
    listprivapps (args)
  elif args.action == "listpublisher":
    listpublisher (args)
  elif args.action == "listprivappslite":
    listprivappslite (args)
  else:
    noaction ()