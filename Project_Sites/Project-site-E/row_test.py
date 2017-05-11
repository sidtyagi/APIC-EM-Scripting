'''
Created on 13-Apr-2017

@author: sidtyagi
'''
#Cisco APIC-EM Python Sandbox v1.1
#Accessing the dcloud APIC EM via the public IP
#https://173.39.116.234/
#173.39.116.153
#admin
#C1sco12345

import requests,ast,json,os,xlrd,sys,time
requests.packages.urllib3.disable_warnings()

xl_workbook = xlrd.open_workbook('Device details.xlsx')
xl_sheet = xl_workbook.sheet_by_name('Sheet1')
row_count=xl_sheet.nrows
print row_count
