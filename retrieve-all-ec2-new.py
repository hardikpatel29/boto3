import boto3

ec2 = boto3.client(service_name='ec2', region_name='us-east-1')

def search(dict, search_name):
    for item in dict:
        if search_name == item['Key']:
            return item['Value']
    return None

def get_ec2_info(ec2, token) -> list:

    response = None
    result = []

    if token != None:
        response = ec2.describe_instances(MaxResults=5, NextToken=token)
    else:
        response = ec2.describe_instances(MaxResults=5)

    token = response.get('NextToken')

    if token == None:
        for i in response.get('Reservations'):
            result.append(i)
        return result
    else:
        result = get_ec2_info(ec2, token)
        for i in response.get('Reservations'):
            result.append(i)
        return result

# Main
try:
    ec2_info = get_ec2_info(ec2, token=None)
    for info_rec in ec2_info:
        id = info_rec.get('Instances')[0].get('InstanceId')
        #name = info_rec.get('Instances')[0].get('InstanceType')
        instance_name = search(info_rec.get('Instances')[0].get('Tags'), 'Name')
        print("Instance ID: {instance_id} Instance Name: {instance_name}".format(instance_id=id, instance_name=instance_name))
        #print("Instance ID: {instance_id} Type Name: {type_name} Instance Name: {instance_name}".format(instance_id=id, type_name=name, instance_name=instance_name))

except Exception as e:
    print("Error: {error}".format(error=e))