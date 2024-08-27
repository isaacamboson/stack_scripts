import boto3

def lambda_handler(event, context):
    
        #instantiate the ec2 boto3 ec2 class        
        ec2 = boto3.resource('ec2')
        
        #Get a list of instances and filter them by running status
        try:     
            instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
            
        except DataNotFoundError as error:
            if error.response['Error']['Code'] == 'DataNotFoundError':
                print("There were no running instances found")
           
        #loop through the list of instances and again filter on all instances that have Backup-Yes key Value pair            
        for instance in instances.filter(
                   Filters=[
                   {
                      'Name': 'tag:Backup',
                      'Values': ['Yes',]
                   }
                   ]):
                       
            # loop through all volumes of instances returned print and call snapshot creation function                 
            for volume in instance.volumes.all():                              
          
                    print("Backing up volume " + volume.id + " of size " + str(volume.size) + " For instance " + instance.id)
                    # print(f'Volume {volume.id} ({volume.size} GiB) -> {volume.state}')
                     
                    #creating snapshots for the instances                     
                    try:
                         snapshot = ec2.create_snapshot(VolumeId=volume.id, Description='EBS Backup')
                     
                         #Tag EBS Volume with instance it belongs to                     
                         snapshot.create_tags(Tags=[{'Key': 'EBS_Instance','Value': instance.id}])
                         
                    except EXCEPTION:
                         print("Snapshot could not be created")
                 
        return{'status': '200'}


#Inline policy that was added to the Lambda role 
"""
{
	"Version": "2012-10-17",
	"Statement": [{
			"Effect": "Allow",
			"Action": [
				"logs:*"
			],
			"Resource": "arn:aws:logs:*:*:*"
		},
		{
			"Effect": "Allow",
			"Action": "ec2:Describe*",
			"Resource": "*"
		},
		{
			"Effect": "Allow",
			"Action": [
				"ec2:CreateSnapshot",
				"ec2:DeleteSnapshot",
				"ec2:CreateTags",
				"ec2:ModifySnapshotAttribute",
				"ec2:ResetSnapshotAttribute"
			],
			"Resource": [
				"*"
			]
		}
	]
}
"""