'''
Created on 07-Sep-2017

@author: Admin
'''

import boto3
import logging
import json
from datetime import datetime
from pytz import timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def controller_rds_handler(event, context):
    
    try:
        DBInstRegion = event['db_instance_region']
        rds = boto3.client('rds', region_name=DBInstRegion)
        arn_list = []
        response_dict = rds.describe_db_instances()
        resp_list = response_dict.get('DBInstances')
        if resp_list is not None:
            for data in resp_list:
                arn_list.append(data.get('DBInstanceArn'))
        
            for arn in arn_list:
                print(arn)
                response_dict = rds.list_tags_for_resource(
                    ResourceName=arn
                )
                resp_list = response_dict.get('TagList')
                tags_dict = {}
                if len(resp_list) != 0:
                    for tag in resp_list:
                        if tag.get('Key') == 'start_time':
                            tags_dict['start_time'] = tag.get('Value') 
                        if tag.get('Key') == 'stop_time':
                            tags_dict['stop_time'] = tag.get('Value') 
                        if tag.get('Key').lower() == 'auto_schedule':
                            tags_dict['auto_schedule'] = True if tag.get('Value').lower() == 'true' else False
                if tags_dict and 'auto_schedule' in tags_dict:
                    if tags_dict['auto_schedule']:
                        invoke_sub_handler(tags_dict, arn)
    except Exception as e:
        raise e
                        
def invoke_sub_handler(Tags, InstArn):
    
    try:
        db_instance_id = InstArn.split(':')[6]
        db_instance_region = InstArn.split(':')[3]
        print(db_instance_id)
        lambda_client = boto3.client('lambda', region_name=db_instance_region)
        
        db_instance_start_time = datetime.strptime(Tags['start_time'], '%H:%M:%S')
        print('Instance start_time: {}'.format(db_instance_start_time.strftime('%H:%M:%S')))
        db_instance_stop_time = datetime.strptime(Tags['stop_time'], '%H:%M:%S')
        print('Instance stop_time: {}'.format(db_instance_stop_time.strftime('%H:%M:%S')))    
        
        db_instance_start_hour = db_instance_start_time.hour
        db_instance_start_min = db_instance_start_time.minute
        db_instance_stop_hour = db_instance_stop_time.hour
        db_instance_stop_min = db_instance_stop_time.minute
        
        date_format = '%d-%m-%Y %H:%M:%S %Z%z'
        current_utc_datetime = datetime.now(timezone('UTC'))
        #print('UTC: {}'.format(current_utc_datetime.strftime(date_format)))
        current_ist_datetime = current_utc_datetime.astimezone(timezone('Asia/Calcutta'))
        print('Current time in IST: {}'.format(current_ist_datetime.strftime(date_format)))
        current_ist_hour = current_ist_datetime.hour
        current_ist_min = current_ist_datetime.minute
        
        start_db_instance = True if db_instance_start_hour == current_ist_hour else False
        stop_db_instance = True if db_instance_stop_hour == current_ist_hour else False
        
        payload = {}
        payload['db_instance_id'] = db_instance_id
        payload['db_instance_region'] = db_instance_region
        if start_db_instance:
            response = lambda_client.invoke_async(
                FunctionName='start_rds_handler',
                InvokeArgs=json.dumps(payload)
            )
            
        elif stop_db_instance:
            response = lambda_client.invoke_async(
                FunctionName='stop_rds_handler',
                InvokeArgs=json.dumps(payload)
            )        
    except Exception as e:
        raise e
        