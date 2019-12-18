from __future__ import print_function 
#from ipywidgets import interact, interactive, fixed, interact_manual 
#import ipywidgets as widgets 
#from ipywidgets import IntSlider, FloatSlider, Checkbox 

import sys 
#from urllib.request import urlretrieve 
import zipfile 
from dateutil.parser import parse 
import json 
from random import shuffle 
import random 
import datetime 
import os 
 
import boto3 

import sagemaker 
import numpy as np 
#import pandas as pd 
#import matplotlib.pyplot as plt 
import datetime 
 
from datetime import datetime 
 
# set random seeds for reproducibility 
np.random.seed(42) 
random.seed(42) 
 
 
 
 
 
def lambda_handler(event,context): 
    path=event['path'] 
    endpoint_name=training(path) 
    return {'endpoint':endpoint_name} 
     
     
     
     
def training(path):
    s3_bucket = path.split('/')[2]  # replace with an existing bucket if needed 
    s3_prefix =  path.split('/')[3] 
    s3_output_path = "s3://{}/{}/output_catg".format(s3_bucket, s3_prefix) 
    image_name = sagemaker.amazon.amazon_estimator.get_image_uri('us-east-2', "forecasting-deepar", "latest") 
    role = 'arn:aws:iam::293818325886:role/service-role/AmazonSageMaker-ExecutionRole-20180823T092944' 
    sagemaker_session = sagemaker.Session() 
 
    estimator = sagemaker.estimator.Estimator( 
        sagemaker_session=sagemaker_session, 
        image_name=image_name, 
        role=role, 
        train_instance_count=1, 
        train_instance_type='ml.c4.2xlarge', 
        base_job_name='kaggle', 
        output_path=s3_output_path 
    ) 
    freq = 'W' 
    prediction_length = 36 
    context_length = 36 
                 
    hyperparameters = { 
        "time_freq": freq, 
        "context_length": str(context_length), 
        "prediction_length": str(prediction_length), 
        "num_cells": "40", 
        "num_layers": "3", 
        "likelihood": "gaussian", 
        "epochs": "400", 
        "mini_batch_size": "32", 
        "learning_rate": "0.00001", 
        "dropout_rate": "0.05", 
        "early_stopping_patience": "10", 
        "cardinality":[2,2,2] 
     
    } 
                         
     
    estimator.set_hyperparameters(**hyperparameters) 
    s3_data_path = "s3://{}/{}/data_catg".format(s3_bucket, s3_prefix) 
    data_channels = { 
        "train": "{}/train/traind2.json".format(s3_data_path), 
        "test": "{}/test/testd2.json".format(s3_data_path) 
    } 
    estimator.fit(inputs=data_channels, wait=True) 
    
    job_name = estimator.latest_training_job.name 
  
    endpoint_name = sagemaker_session.endpoint_from_job( 
        job_name=job_name, 
        initial_instance_count=1, 
        instance_type='ml.m4.xlarge', 
        deployment_image=image_name, 
        role=role 
    ) 
    return endpoint_name 