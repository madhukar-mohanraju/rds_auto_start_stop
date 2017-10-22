'''
Created on 07-Sep-2017

@author: Madhukar
'''

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def start_rds_handler(event, context):
    
    try:
        DBInstId = event['db_instance_id']
        DBInstRegion = event['db_instance_region']
        isDbInstanceRunning = False
        logger.info('Got event: {}'.format(event))
        rds = boto3.client('rds', region_name=DBInstRegion)
        response_dict = rds.describe_db_instances(
            DBInstanceIdentifier = DBInstId,
        )
        resp_list = response_dict.get('DBInstances')
        if resp_list is not None:
            for data in resp_list:
                isDbInstanceRunning = True if data.get('DBInstanceStatus') == 'stopped' else False
        if isDbInstanceRunning:
            logger.info('Starting Db Instance: %s'%DBInstId)
            response_dict =  rds.start_db_instance(DBInstanceIdentifier = DBInstId)
            '''resp_list = response_dict.get('DBInstance')
            if resp_list is not None:
                return data.get('DBInstanceStatus')
            else:
                logger.error('An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance '+DBInstId+' is not in stopped state.')'''
        else:
            logger.error('An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance '+DBInstId+' is not in stopped state.')
    
    except Exception as e:
        raise str(e)
