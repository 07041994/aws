import sys
from dateutil.parser import parse
import json
from random import shuffle
import random
import datetime
import os
import boto3
import sagemaker
import numpy as np
import datetime

from datetime import datetime


# set random seeds for reproducibility
np.random.seed(42)
random.seed(42)




def lambda_handler(event,context):
    endpoint=event["endpoint"]
    #file=event['file']
    #s3_bucket = 'aman199'  # replace with an existing bucket if needed
    #s3_prefix = 'product3'
    #s3_client = boto3.client('s3',aws_access_key_id='AKIAIRR6OFVAQA2UHCGQ',aws_secret_access_key='N2wG8jgYWAOW8vk3F5XA1X5frwLWB78vOLhc5Avj')
    #response = s3_client.get_object(Bucket="aman199",Key=file)
    #p = pd.read_csv(response["Body"])
    #p2=p.iloc[:,1:]
    sagemaker_session = sagemaker.Session()
    role='arn:aws:iam::293818325886:role/service-role/AmazonSageMaker-ExecutionRole-20180823T092944'
    predictor = sagemaker.predictor.RealTimePredictor(endpoint,sagemaker_session=sagemaker_session, content_type="application/json")
    rea=getpredictionresult(10,[],[0,0,0])
    results=predictor.predict(rea)
    #plot=plotSeries(results1,10,test_ts=p2.iloc[420:456,1], truth=False, truth_data=None, truth_label=None)
    return results
    
    
    
    #plt.savefig(plo, format='png')
    #s31 = boto3.resource('s3')
    #bucket1 = s31.Bucket('aman199')
    #bucket1.put_object(Body=plot, ContentType='image/png', Key=KEY)
    #print(plo)
    
    
    
def getpredictionresult(sample,target,cat):
    request = json.dumps({
    "instances": [
        {"start":"2010-02-05 00:00:00","cat":cat,"target":target},
        ],
    "configuration": {
         "num_samples": sample,
         "output_types": ["mean", "quantiles","samples"],
         "quantiles": ["0.5", "0.9"]}})
    
    return request