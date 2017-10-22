'''
Created on 07-Sep-2017

@author: Madhukar
'''

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def stop_rds_handler(event, context):
    
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
                isDbInstanceRunning = True if data.get('DBInstanceStatus') == 'available' else False
        if isDbInstanceRunning:
            logger.info('Stopping Db Instance: %s'%DBInstId)
            response_dict =  rds.stop_db_instance(DBInstanceIdentifier = DBInstId)
            '''resp_list = response_dict.get('DBInstance')
            if resp_list is not None:
                return data.get('DBInstanceStatus')
            else:
                logger.error('An error occurred (InvalidDBInstanceState) when calling the StopDBInstance operation: Instance '+DBInstId+' is not in available state.')'''
        else:
            logger.error('An error occurred (InvalidDBInstanceState) when calling the StopDBInstance operation: Instance '+DBInstId+' is not in available state.')
            
    except Exception as e:
        raise str(e)
