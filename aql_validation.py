#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Author : Oguzcan Pamuk
Desc   : This code has been developed to perform syntax validation of AQL queries on QRadar.

Req    : 
            - pip3 install requests
            - QRadar IP / Port
            - QRadar SEC Token
            - Query Input File Path

'''

import sys,os,csv
import time
import urllib3
import requests

QUERY_INPUT_FILE = "queries.csv"
RESULT_OUTPUT_FILE = "output.csv"
QRADAR_IP_PORT = ""
BASE_URL = "https://" + QRADAR_IP_PORT + "/api/ariel/searches"
QRADAR_KEY = ''
SLEEP = 10
CERTIFICATION_VERIFICATION = False

def readQueryFile():
    queries = []
    if not (os.path.exists(QUERY_INPUT_FILE)):
        return None

    with open(QUERY_INPUT_FILE,'r') as fp:
        csvreader = csv.reader(fp)
        try:
            for input in csvreader:
                qradarQuery = input[0]
                queries.append(qradarQuery)
        except Exception as error:
            print('An exception occurred in read file operations: {}'.format(error))
            sys.exit()

    return queries

def main():

    if (QUERY_INPUT_FILE == "" or RESULT_OUTPUT_FILE == "" or QRADAR_IP_PORT == "" or QRADAR_KEY == ""):
        print ("Before you begin, please fill in the required fields.")
        sys.exit()

    urllib3.disable_warnings()
    queries = readQueryFile()
    headers = {
        'SEC': QRADAR_KEY
    }
    SQL = "Select * FROM events WHERE "
    url = BASE_URL +"?query_expression="
    fpOut = open(RESULT_OUTPUT_FILE, 'w')
    writer = csv.writer(fpOut)
    writer.writerow(["Query","Result"])
    for query in queries:
        urlQuery = SQL + query
        json_data = requests.post(url + urlQuery, headers=headers, verify=CERTIFICATION_VERIFICATION).json()
        if ('http_response' in json_data):
            writer.writerow([query,"Not_Valid"])
        else:
            search_id = json_data['search_id']
            time.sleep(SLEEP)
            urlResult = BASE_URL + "/" + search_id + "/" + "results"
            json_data = requests.get(urlResult, headers=headers, verify=CERTIFICATION_VERIFICATION).json()
            writer.writerow([query,"Valid"])
        
    fpOut.close()

if __name__ == '__main__':
    main()