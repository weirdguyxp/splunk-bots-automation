#script to create users for bots
#assumes you have one instance called splunk for bots users to use and one instance calles splunkscoring which is your scoring server
#assumes you have the same admin name and pw on both instances
#assumes you only need one role per instance per user

#imports
import csv
import requests
import getpass
import sys

#fix ssl warnings
requests.packages.urllib3.disable_warnings()

#vars to be set before running
splunk = "splunk"
splunkport = "8089"
splunkrole="ess_analyst"
splunkscoring = "splunkscoring"
splunkscoringport = "8089"
splunkscoringrole="ctf_competitor"
sslverify=False
#for in dev functionality
splunkscoringapp = "Capture the Flag"
splunkscoringapplookupname = "ctf_users"

#get creds and other vars at run time
#check if a term or not
if sys.stdin.isatty():
    #get admin
    print("\n--==Glenn's BotS bootstrap script==--\n\nPlease enter admin creds.  This script assumes that both isntances (splunk + splunkscoring) use the same creds.")
    try: 
        admin = input("Username: ") 
    except Exception as error: 
        print('ERROR', error) 
    else: 
        print(admin)
    #get adminpw
    try: 
        adminpw = getpass.getpass("Password: ") 
    except Exception as error: 
        print('ERROR', error) 
    #get csv file name
    try: 
        csvfilename = input("CSV filename (assuming its in this dir, if not use full path): ") 
    except Exception as error: 
        print('ERROR', error) 
    else: 
        print(csvfilename)
    #get adminpw
    try: 
        password = getpass.getpass("Generic password for the user accounts in the CSV (tell users to change this): ") 
    except Exception as error: 
        print('ERROR', error) 
else:
    #this works if your passing args at cli
    admin = sys.stdin.readline().rstrip()
    adminpw = sys.stdin.readline().rstrip()
    csvfilename = sys.stdin.readline().rstrip()
    password = sys.stdin.readline().rstrip()

#read the csv
with open(csvfilename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        #extract user id to create
        user=row[16]
        #print(user)

        #setup users

        #check if csv header
        if user != "Username":

            #splunk
            #establish connection setup to splunk
            splunkurl="https://"+splunk+":"+splunkport+"/services/authentication/users"
            #print(splunkurl)
            #build the splunkbody
            splunkbody={'name': user,'password':password,'roles':splunkrole}
            #make the request to splunk, with ssl checking disabled
            x = requests.post(splunkurl, data = splunkbody, auth = (admin, adminpw), verify=sslverify)
            #print(x.status_code)

            #splunk scoring
            #establish connection setup to splunk
            splunkurl="https://"+splunkscoring+":"+splunkscoringport+"/services/authentication/users"
            #print(splunkurl)
            #build the splunkbody
            splunkbody={'name': user,'password':password,'roles':splunkscoringrole}
            #make the request to splunk, with ssl checking disabled
            y = requests.post(splunkurl, data = splunkbody, auth = (admin, adminpw), verify=sslverify)
            #print(y.status_code)

            #output status
            print("setup splunk and splunkscoring "+user+" with status "+str(x.status_code)+" and "+str(y.status_code)+" respectively.")
        

#upload the csv of users, doesnt work
#splunkcsvurl="https://"+splunkscoring+":"+splunkscoringport+"/servicesNS/nobody/"+splunkscoringapp+"/data/lookup-table-files/"+splunkscoringapplookupname
#headers = {'Content-Type': 'application/json'}
#data = {"eai:data" : "ctf_users.csv"}
#r = requests.post(splunkcsvurl, data, auth = (admin, adminpw), verify=sslverify, headers=headers)
#print(r.status_code)