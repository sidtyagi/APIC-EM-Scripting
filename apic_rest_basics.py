'''
Created on 13-Apr-2017

@author: sidtyagi
'''
#Cisco APIC-EM Python Sandbox v1.1
#Accessing the dcloud APIC EM via the public IP
#https://1.2.3.4/
#1.2.3.4
#un
#pwd

import requests,ast,json,os,xlrd,sys,time
requests.packages.urllib3.disable_warnings()

un="username"
pwd="pwd"

def get_token(un,pwd):
    url= base_url+'/ticket'
    #payload = "{\r\n\t\"password\": \"pwd\",\r\n\t\"username\": \"un\"\r\n}\r\n\r\n"
    #payload = "{\r\n\t\"password\": \""+pwd+"\",\r\n\t\"username\": \""+un+"\"\r\n}\r\n\r\n"
    payload = "{\"password\": \""+pwd+"\",\"username\": \""+un+"\"\r\n}"
    headers = {
        'content-type': "application/json"        
        }
    
    response_rcvd = requests.request("POST", url, data=payload, headers=headers,verify=False)    
    response_text=json.loads(str(response_rcvd.text))
    #print response_text
    
    #response_text_to_dict=ast.literal_eval(str(response_text))
    #st=response_text_to_dict['response']['serviceTicket']
    st=response_text['response']['serviceTicket']
    #print st
    return st

def list_devices():
    url=base_url+'/topology/physical-topology'
    headers={"X-Auth-Token":get_token(un, pwd),
             'content-type': "application/json"
                          }
    response=requests.get(url,headers=headers,verify=False)
    #print response
    #print response.json()
    print json.dumps(response.json(),indent=2,separators=(',',':'))


def list_sw_versions():
    url=base_url+'/network-device'
    headers={"X-Auth-Token":get_token(un, pwd),
             'content-type': "application/json"
                          }
    response=requests.get(url,headers=headers,verify=False)
    #print response
    #print response.json()
    print json.dumps(response.json(),indent=2,separators=(',',':'))

    
    #----Now pulling the Sw versions of each device----#
    
    op_data=response.json()
    print type(op_data)
    node_list=op_data['response']
    print node_list
    
    for node in node_list:
        print 'device is %s'%node['hostname']
        print 'S/w is %s'%node['softwareVersion']


def file_upload():     
    #url = "https://10.66.188.110/api/v1/file/config"
    url = base_url+"/file/config"
    all_files=os.listdir('.')   
    print 'Found the below files in folder---will choose only text files to upload'
    print all_files 
    token=get_token(un, pwd)
    for x in all_files:
        if '.txt' in x:
            print 'Uploading file %s'%x
            name=x    
            #content = open("Configs\\"+x, "r")            
            content = open(x, "r")
            #files = {'fileUpload': (name, content)}    
            #fileUpload is meant to be the file        
            files = {'fileUpload': open(name, 'r')}
            headers = {"X-Auth-Token":token}
            r = requests.post(url, headers=headers,files=files,verify=False)       
            
            #print r
            #print type(r.text)
            print r.text
             
def get_list_of_config_files():           
    url = base_url+"/file/namespace/config"
    token=get_token(un, pwd)
    #payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"fileUpload\"; filename=\"Sample1.txt\"\r\nContent-Type: text/plain\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {        
        'x-auth-token': token   
        }    
    #response = requests.request("GET", url, headers=headers,verify=False)    
    response = requests.get(url, headers=headers,verify=False)
    #print(response.text)
    response_json=response.json()
    #print type(response_json)
    #print response_json
    print json.dumps(response.json(),indent=2,separators=(',',':'))
    for x in response_json['response']:
        print x['name']


def get_file_id(fname):
    url = base_url+"/file/namespace/config"
    token=get_token(un, pwd)
    #payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"fileUpload\"; filename=\"Sample1.txt\"\r\nContent-Type: text/plain\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {        
        'x-auth-token': token   
        }    
    #response = requests.request("GET", url, headers=headers,verify=False)    
    response = requests.get(url, headers=headers,verify=False)
    #print(response.text)
    response_json=response.json()
    #print type(response_json)
    #print response_json
    #print json.dumps(response.json(),indent=2,separators=(',',':'))
    for x in response_json['response']:
        #print x['name']
        if x['name']==fname:
            #print x['id']
            return x['id']
    

def update_file(id,fname):
    url = base_url+"/file/config/"+id
    x=fname
    print 'Updating file %s'%x
    name=x    
    #content = open("Configs\\"+x, "r")            
    content = open(x, "r")
    #files = {'fileUpload': (name, content)}    
    #fileUpload is meant to be the file        
    files = {'fileUpload': open(name, 'r')}
    headers = {"X-Auth-Token":get_token(un, pwd)}
    r = requests.put(url, headers=headers,files=files,verify=False)       
    
    
    #print r
    #print type(r.text)
    print r.text
    #print json.dumps(r.json(),indent=2,separators=(',',':'))


#def create_project_rule(site_id,token,hostname,s_no,pid,image,configid):
def create_project_rule(site_id,token,hostname,s_no,pid,configid):
    url=base_url+'/pnp-project/'+site_id+'/device' 
    headers= { 'x-auth-token': token,'content-type' : 'application/json'} 
    '''body = [{
        
        "serialNumber": s_no,
        "platformId":pid,
        "hostName": hostname,
        "configId":configid,
        "imageId":image
        }]
    '''
    body = [{
        
        "serialNumber": s_no,
        "platformId":pid,
        "hostName": hostname,
        "configId":configid,        
        }]
    response = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
    #if response.json():
    #        print(json.dumps(response.json(), indent=2))

def project_name_to_id(token,project_name):    
    url =base_url+"/pnp-project"


    headers= { 'x-auth-token': token, 'content-type' : 'application/json'}
    # look for project by name.  need to get the project id
    search_url = url + '?siteName=%s&offset=1&limit=10' %project_name
    print("GET: %s"  % search_url)
    
    try:
        response = requests.get(search_url, headers=headers, verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    #time.sleep(3)
    # check response.json() for values
    # no match
    # multi match
    # single match

    matches = response.json()['response']
    print matches
    print '*********************'
    
    for k in range(0,len(matches)):
        site_name=matches[k]['siteName']
        
        if project_name in site_name:
            project_id=matches[k]['id']
            print 'The site id is %s=============================================='%project_id
            return project_id
    '''
    if len(matches) <1:
        raise ValueError('No matches found for %s' % project_name)
    elif len(matches) > 1:
        print 'jjjjjjjjjjjjjjjj'
        raise ValueError("multiple matches found for %s" % project_name)
    else:
        project_id = matches[0]['id']
        return project_id
    '''
def create_project(token,project_name):  
    print "Trying to create project %s"%project_name
    url=base_url+'/pnp-project'
    
    headers= { 'x-auth-token': token,'content-type' : 'application/json'}  
    body = [{"siteName": project_name}]
    response = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
    #taskid = response.json()['response']['taskId']
    #print taskid
    response_text=response.text
    #print response_text
    response_text_to_dict=ast.literal_eval(str(response_text))
    task_id=response_text_to_dict['response']['taskId']
    
    #Now look at the above task id    
    print 'Looking at task %s'%task_id
    url=base_url+'/task/'+task_id.strip()
    headers= { 'x-auth-token': token,'content-type' : 'application/json'}
    response = requests.get(url, headers=headers, verify=False)
    response_as_dict=response.json()
    #print response_as_dict
    try:
        response_as_dict2=json.loads(response_as_dict['response']['progress'])#since the value in brackets is unicode
        print response_as_dict2
        site_id=response_as_dict2['siteId'] 
        print site_id
        return site_id
    except:
        return None



def pnp():
    all_projects=os.listdir('Project_Sites')
    token=get_token(un, pwd)    
    for k1 in all_projects:        
        xl_workbook = xlrd.open_workbook('Project_Sites\\'+k1+'\\Device Details.xlsx')
        xl_sheet = xl_workbook.sheet_by_name('Sheet1')
        row_count=xl_sheet.nrows  
        print row_count   
        
        for x in  range(1,row_count):
            hostname= (xl_sheet.cell(x,0).value)
            print hostname+'--------------------------------------'
            
            s_no= (xl_sheet.cell(x,1).value)
            #print s_no
            pid=(xl_sheet.cell(x,2).value)
            #print pid
            config_file=(xl_sheet.cell(x,3).value)
            #print config_file
            #image=(xl_sheet.cell(x,4).value)
            #print image
            site_id=create_project(token,k1)
            #image_id=get_image_id(token,image)
            #print 'IMage ID---------------------------------'
            #print image_id
            #print '========================================'
            print 'the site id for project %s'%k1
            print site_id
            
            if site_id is not None:
                config_id=get_file_id(hostname+'.txt')
                #create_project_rule(site_id,token,hostname,s_no,pid,image_id,config_id)
                create_project_rule(site_id,token,hostname,s_no,pid,config_id)
                
            else:
                config_id=get_file_id(hostname+'.txt')
                print 'here-----------------------'
                site_id=project_name_to_id(token, k1)
                print 'here222-----------------------'
                #create_project_rule(site_id,token,hostname,s_no,pid,image_id,config_id)
                create_project_rule(site_id,token,hostname,s_no,pid,config_id)
            
         
        
#base_url = "https://173.39.116.234/api/v1"
base_url = "https://173.39.117.53/api/v1"
#get_token(un, pwd)
#list_devices()
#list_sw_versions()
#file_upload()
#get_list_of_config_files()
#file_id=get_file_id('Device1.txt')
#update_file(file_id,'Device1.txt')
pnp()
