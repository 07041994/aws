import sys
import json
from random import shuffle
import random
import datetime
import os
import boto3
import s3fs
import numpy as np
import pandas as pd
import datetime

np.random.seed(42)
random.seed(42)



def lambda_handler(event,context):
    file=event['file']
    
    s3_client = boto3.client('s3',aws_access_key_id='AKIAIRR6OFVAQA2UHCGQ',aws_secret_access_key='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')
    response = s3_client.get_object(Bucket="aman19",Key=file)
    p = pd.read_csv(response["Body"])
    p2=p.iloc[:,1:]
    s3_path1,traini,tes=train_test(p2)
    print(traini)
    print(tes)
    return {'path':s3_path1}
    
def write_dicts_to_file(path, data):
    with open(path, 'wb') as fp:
        for d in data:
            fp.write(json.dumps(d,separators=(',', ':')).encode("utf-8"))
            fp.write("\n".encode('utf-8'))    

s3 = boto3.resource('s3')
def copy_to_s3(local_file, s3_path, override=False):
    assert s3_path.startswith('s3://')
    split = s3_path.split('/')
    bucket = split[2]
    path = '/'.join(split[3:])
    buk = s3.Bucket(bucket)
    
    #if len(list(buk.objects.filter(Prefix=path))) > 0:
     #   if not override:
      #      print('File s3://{}/{} already exists.\nSet override to upload anyway.\n'.format(s3_bucket, s3_path))
       #     return
        #else:
         #   print('Overwriting existing file')
    with open(local_file, 'rb') as data:
        print('Uploading file to {}'.format(s3_path))
        buk.put_object(Key=path, Body=data)

def train_test(p2):
    startdate=p2.iloc[0,0]
    prediction_length=36
    training =  [{"start":str(startdate),"cat":[0,0,0],"target":p2.iloc[:,1][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[0,0,1],"target":p2.iloc[:,3][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[0,1,0],"target":p2.iloc[:,4][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[0,1,1],"target":p2.iloc[:,5][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[1,0,0],"target":p2.iloc[:,6][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[1,0,1],"target":p2.iloc[:,7][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[1,1,0],"target":p2.iloc[:,8][:-prediction_length].tolist()},
                {"start":str(startdate),"cat":[1,1,1],"target":p2.iloc[:,9][:-prediction_length].tolist()}]


    test     =  [{"start":str(startdate),"cat":[0,0,0],"target":p2.iloc[:,1].tolist()},
                {"start":str(startdate),"cat":[0,0,1],"target":p2.iloc[:,3].tolist()},
                {"start":str(startdate),"cat":[0,1,0],"target":p2.iloc[:,4].tolist()},
                {"start":str(startdate),"cat":[0,1,1],"target":p2.iloc[:,5].tolist()},
                {"start":str(startdate),"cat":[1,0,0],"target":p2.iloc[:,6].tolist()},
                {"start":str(startdate),"cat":[1,0,1],"target":p2.iloc[:,7].tolist()},
                {"start":str(startdate),"cat":[1,1,0],"target":p2.iloc[:,8].tolist()},
                {"start":str(startdate),"cat":[1,1,1],"target":p2.iloc[:,9].tolist()}]
    
    
    #%%time
    write_dicts_to_file("/tmp/traind2.json", training)
    write_dicts_to_file("/tmp/testd2.json", test)
    
    s3_bucket = 'aman19'  # replace with an existing bucket if needed
    s3_prefix = 'product3'
    s3_data_path = "s3://{}/{}/data_catg".format(s3_bucket, s3_prefix)
    
    #%%time
    copy_to_s3("/tmp/traind2.json", s3_data_path + "/train/traind2.json")
    copy_to_s3("/tmp/testd2.json", s3_data_path + "/test/testd2.json")
    s3filesystem = s3fs.S3FileSystem()
    with s3filesystem.open(s3_data_path + "/test/testd2.json", 'rb') as fp:
        print(fp.readline().decode("utf-8")[:100] + "...")
    s3filesystem = s3fs.S3FileSystem()
    with s3filesystem.open(s3_data_path + "/train/traind2.json", 'rb') as fp:
        print(fp.readline().decode("utf-8")[:100] + "...")
    
    return s3_data_path,training,test