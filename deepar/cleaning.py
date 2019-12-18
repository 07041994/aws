import sys
import zipfile
from dateutil.parser import parse
from random import shuffle
import random
import datetime
import os
import s3fs
import boto3
import numpy as np
import pandas as pd
from datetime import datetime


# set random seeds for reproducibility
np.random.seed(42)
random.seed(42)



def lambda_handler(event,context):
    filename=event['file']
    s3_bucket = 'aman19'  # replace with an existing bucket if needed
    s3_prefix = 'product3'
    p2=cleaning(filename)
    bytes_to_write = p2.to_csv(None).encode()
    fs = s3fs.S3FileSystem(key=API_key, secret=Secret_key)
    with fs.open('s3://aman19/file.csv', 'wb') as f:
        f.write(bytes_to_write)
    print(p2)
    return 
    

def cleaning(filename):
    s3_bucket = 'aman19'
    s3_prefix = 'product3'
    s3_data_path = "s3://{}/{}/data_catg".format(s3_bucket, s3_prefix)
    s3_output_path = "s3://{}/{}/output_catg".format(s3_bucket, s3_prefix)
    s3_filepath = "s3://{}/{}".format(s3_bucket,filename )
    #p=pd.read_csv("s3://aman19/wal1.csv")
    s3_client = boto3.client('s3',aws_access_key_id=Api_key',aws_secret_access_key=Secret_key)
    response = s3_client.get_object(Bucket="aman19",Key="wal1.csv")
    p = pd.read_csv(response["Body"])
    
    
    p['cat31']=np.zeros(143)
    p['cat32']=np.zeros(143)
    p['cat1']=np.zeros(143)
    p['cat2']=np.zeros(143)
    p.rename(columns={'cat11':'cat00','cat12':'cat01','cat21':'cat10','cat22':'cat11','cat31':'cat20','cat32':'cat21'}, inplace=True)
    for i in range(0, len(p.iloc[:,6])):
        if p.iloc[i,6] == 0:
            p.iloc[i,6] = random.randint(10000,100000)
    for i in range(0, len(p.iloc[:,7])):
        if p.iloc[i,7] == 0:
            p.iloc[i,7] = random.randint(10000,100000)

    for i in range(143):
        p.iloc[i,8]=random.randint(10000,100000)
        p.iloc[i,9]=random.randint(10000,100000)
    p1=pd.DataFrame()
    p1['Date']=pd.date_range('2012-11-02','2018-10-26',freq='W-FRI')
    p1['cat00']=np.zeros(313)
    p1['IsHoliday']=np.zeros(313)
    p1['cat01']=np.zeros(313)
    p1['cat10']=np.zeros(313)
    p1['cat11']=np.zeros(313)
    p1['cat20']=np.zeros(313)
    p1['cat21']=np.zeros(313)
    p1['cat1']=np.zeros(313)
    p1['cat2']=np.zeros(313)
    for i in range(313):
        p1['cat00'][i]=random.randint(10000,100000)
        p1['cat01'][i]=random.randint(10000,100000)
        p1['cat10'][i]=random.randint(10000,100000)
        p1['cat11'][i]=random.randint(10000,100000)
        p1['cat20'][i]=random.randint(10000,100000)
        p1['cat21'][i]=random.randint(10000,100000)
        p['cat1'][i]=random.randint(10000,100000)
        p['cat2'][i]=random.randint(10000,100000)
    p3=pd.concat([p,p1],axis=0)
    p3.iloc[:,[1,3,4,5,6,7]]=p3.iloc[:,[1,3,4,5,6,7]].astype(int)
    for x in range(143):
        p3.iloc[x,0]=datetime.strftime(datetime.strptime(p3.iloc[x,0],"%m/%d/%Y"),"%Y-%m-%d")
    for x in range(313):
        p3.iloc[x+143,0]=datetime.strftime(p3.iloc[x+143,0],"%Y-%m-%d")
    
    return p3
