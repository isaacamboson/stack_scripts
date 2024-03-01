#!/usr/bin/python

import boto3, botocore
from botocore.exceptions import ClientError
import creds as c
import json


# creating aws s3 function that creates bucket(s)
def aws_s3_create_bucket(**args):

    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        create_bucket_response = s3_client.create_bucket(Bucket = args["bucket_name"])
            
        if create_bucket_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("New S3 bucket created -", create_bucket_response["ResponseMetadata"]["HTTPHeaders"]["location"])

    except ClientError as error:
        print(error.response)

# aws_s3_create_bucket(role_service = "sts", service = "s3", bucket_name = "stackbuckisaac444")

#====================================================================================================================================================================

def aws_s3_delete_bucket(**args):

    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        delete_bucket_response = s3_client.delete_bucket(Bucket = args["bucket_name"])
                    
        if delete_bucket_response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            print("S3 bucket '{}' has been deleted".format(args["bucket_name"]))

    except ClientError as error:
        print(error.response)

# aws_s3_delete_bucket(role_service = "sts", service = "s3", bucket_name = "stackbuckisaac444")
        
#====================================================================================================================================================================

def aws_s3_upload_content(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
        
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        for each_file in args["upload_files"]:
            upload_response = s3_client.upload_file(each_file, args["bucket_name"], Key = each_file)
            print("'{}' has been uploaded to the s3 bucket - '{}'".format(each_file, args["bucket_name"]))

    except ClientError as error:
        print(error.response)
    
# aws_s3_upload_content(role_service = "sts", service = "s3", upload_files = ["test_isaac.py", "test_loop.py", "testopen.py"], bucket_name = "stackbuckisaacsep23")

#====================================================================================================================================================================

def aws_s3_empty_bucket(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #using the list_objects_v2 function in boto3 to lists the objects (up to 1,000) in the bucket
        response = s3_client.list_objects_v2(Bucket = args["bucket_name"])
        
        #iterating through the response to pull the objects' 'Keys' in the bucket
        for content in response["Contents"]:
            delete_reponse = s3_client.delete_object(Bucket = args["bucket_name"], Key = content["Key"])
            if delete_reponse["ResponseMetadata"]["HTTPStatusCode"] == 204:
                print("'{}' has been deleted from the bucket - '{}'.".format(content["Key"], args["bucket_name"]))
               
    except ClientError as error:
        print(error.response)

# aws_s3_empty_bucket(role_service = "sts", service = "s3", bucket_name = "stack-buck1-isaac")    
        
#====================================================================================================================================================================

def aws_s3_list_content(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #using the list_objects_v2 function in boto3 to lists the objects (up to 1,000) in the bucket
        response = s3_client.list_objects_v2(Bucket = args["bucket_name"])

        #iterating through the response to pull the objects' 'Keys' in the bucket
        for content in response["Contents"]:
            print(content["Key"])

    except ClientError as error:
        print(error.response)

# aws_s3_list_content(role_service = "sts", service = "s3", bucket_name = "stackbuckisaacsep23")

#====================================================================================================================================================================

def aws_s3_enable_disable_versioning(**args):
    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #assigning a versioning configuration to the bucket
        versioning_repsonse = s3_client.put_bucket_versioning(Bucket = args["bucket_name"], VersioningConfiguration = {"Status": args["versioning_status"]})
        
        #checking if the versioning was applied to the s3 bucket
        if versioning_repsonse["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("Versioning configuration change successfully applied to bucket - '{}'.".format(args["bucket_name"]))
        
        #using the 'get_bucket_versioning' verify the new versioning configuration for the s3 bucket
        versioning_response1 = s3_client.get_bucket_versioning(Bucket = args["bucket_name"])
        print("The versioning configuration for s3 bucket - '{}' is {}.".format(args["bucket_name"], versioning_response1["Status"]))
        
    except ClientError as error:
        print(error.response)
        
# aws_s3_enable_disable_versioning(role_service = "sts", service = "s3", bucket_name = "stack-buck1-isaac", versioning_status = "Enabled")
        
#====================================================================================================================================================================

def aws_s3_bucket_encryption(**args):

    try:
        encryption_action = args["encryption_action"]

        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        if encryption_action.lower() == "enable":
            #enabling bucket encryption by calling the 'put_bucket_encryption' method
            encryption_response = s3_client.put_bucket_encryption(
                Bucket = args["bucket_name"],
                ServerSideEncryptionConfiguration = {
                    "Rules": [
                        {
                            "ApplyServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "aws:kms",
                                "KMSMasterKeyID": "9b6a02f0-0fb6-4642-91a3-5c5fb4431ada"
                            },
                            "BucketKeyEnabled": True
                        },
                    ]
                },
                ExpectedBucketOwner = "767398027423"
            )       

            #checking if calling the 'put_bucket_encryption' method was successful
            if encryption_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                print("Encrytion has been enabled.")

        elif encryption_action.lower() == "disable":
            #disabling bucket encryption by calling the 'delete_bucket_encryption' method
            encryption_response = s3_client.delete_bucket_encryption(Bucket = args["bucket_name"])
            if encryption_response["ResponseMetadata"]["HTTPStatusCode"] == 204:
                print("Encryption has been disabled, bucket encryption reverted to default encryption.")

        #checking to verify the bucket encryption enabled
        encryption_response_check = s3_client.get_bucket_encryption(Bucket = args["bucket_name"])
        encryption_algorithm = encryption_response_check["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]

        print("Bucket encryption for '{}' is currently '{}'.".format(args["bucket_name"], encryption_algorithm))
    
    except ClientError as error:
        print(error.response)

# aws_s3_bucket_encryption(role_service = "sts", service = "s3", bucket_name = "stackbuckisaacsep23", encryption_action = "enable")
        
#====================================================================================================================================================================

def aws_s3_enable_server_access_logging(**args):

    try:
        # encryption_action = args["encryption_action"]

        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        s3_client = boto3.client(args["service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #enabling server logging access using the 'put_bucket_logging' method
        bucket_logging_response = s3_client.put_bucket_logging(
            Bucket = args["bucket_name"],
            BucketLoggingStatus = {
                "LoggingEnabled": {
                    "TargetBucket": args["log_bucket"],
                    "TargetGrants": [
                        {
                            "Grantee": {
                                "Type": "AmazonCustomerByEmail",
                                "EmailAddress": "isaacamboson@gmail.com"
                            },
                            "Permission": "FULL_CONTROL"
                        },
                        {
                            "Grantee": {
                                "Type": "Group",
                                "URI": "http://acs.amazonaws.com/groups/global/AllUsers"
                            },
                            "Permission": "READ"
                        }
                    ],
                    "TargetPrefix": args["bucket_name"]
                }
            }
        )

        #checking if the bucket logging was applied to the s3 bucket
        if bucket_logging_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("Bucket Logging has been enabled.")

        #using the 'get_bucket_logging' method to verify the new logging configuration for the s3 bucket
        get_bucket_logging_response = s3_client.get_bucket_logging(Bucket = args["bucket_name"])
        print("Bucket logging has been enabled on the bucket -", get_bucket_logging_response["LoggingEnabled"]["TargetPrefix"])
        print("Logs are being forwarded to the bucket -", get_bucket_logging_response["LoggingEnabled"]["TargetBucket"])

        #updating bucket policy for log_bucket to grant permissions to the logging service principal, using a bucket policy
        with open("server_logging_policy.json") as sv_policy:
            sv_policy_content = sv_policy.read()
            print(sv_policy_content)

        bucket_logging_policy_response = s3_client.put_bucket_policy(
            Bucket = args["log_bucket"],
            Policy = sv_policy_content
            )

        print(bucket_logging_policy_response)
        

    except ClientError as error:
        print(error.response)

# aws_s3_enable_server_access_logging(role_service = "sts", service = "s3", bucket_name = "stackbuckisaacsep23", log_bucket = "stack-buck1-isaac-serverlogs")

#====================================================================================================================================================================
        
def aws_s3_enable_obj_level_logging(**args):

    try:
        #creating an sts client for assuming roles
        sts_client = boto3.client(args["role_service"], 
                            aws_access_key_id=c.aws_access_key_id,
                            aws_secret_access_key=c.aws_secret_access_key)

        assume_role_response = sts_client.assume_role(
            RoleArn = "arn:aws:iam::767398027423:role/Engineer",
            RoleSessionName = "Engineer@Dev"
            )
                
        #using the temporary credentials for our assumed role for assume the Dev_Engineer role
        temp_credentials = assume_role_response["Credentials"]
        ct_client = boto3.client(args["ct_service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"],
                            region_name = "us-east-1"
                            )
        
        s3_client = boto3.client(args["s3_service"],
                            aws_access_key_id = temp_credentials["AccessKeyId"],
                            aws_secret_access_key = temp_credentials["SecretAccessKey"],
                            aws_session_token = temp_credentials["SessionToken"]
                            )
        
        #updating bucket policy for source bucket to grant permissions for cloud trail, using a bucket policy
        with open("cloud_trail.json") as ct_policy:
            ct_policy_content = ct_policy.read()
            # print(ct_policy_content)

        ct_policy_response = s3_client.put_bucket_policy(
            Bucket = args["bucket_name"],
            Policy = ct_policy_content
            )

        # print(ct_policy_response)
        
        #creating the cloud trail
        create_trail_response = ct_client.create_trail(
            Name = args["trail_name"],
            S3BucketName = args["bucket_name"],
            S3KeyPrefix = args["trail_prefix"],
            IncludeGlobalServiceEvents = True,
            IsOrganizationTrail = False,
            EnableLogFileValidation = False,
            IsMultiRegionTrail = True
        )
        print(create_trail_response)

        #put event selectors
        put_event_selectors_response = ct_client.put_event_selectors(
            TrailName = args["trail_name"],
            EventSelectors = [
                {
                    "ReadWriteType": "All",
                    "IncludeManagementEvents": True,
                    "DataResources": [
                        {
                            "Type": "AWS::S3::Object",
                            "Values": [
                                "arn:aws:s3:::stackbuckisaacsep23/arithmetic.sh"
                            ]
                        }
                    ]
                }
            ]
        )

        print(put_event_selectors_response)

        #get event selectors
        get_event_selectors_response = ct_client.get_event_selectors(
            TrailName = args["trail_name"]
        )

        print(get_event_selectors_response)

    except ClientError as error:
        print(error.response)

aws_s3_enable_obj_level_logging(role_service = "sts",
                                s3_service = "s3",
                                ct_service = "cloudtrail",
                                bucket_name = "stackbuckisaacsep23",
                                trail_name = "stackbuckisaacsep23_trail",                                
                                trail_prefix = "stackbuckisaacsep23-pfx"
                                )
















# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "S3ServerAccessLogsPolicy",
#             "Effect": "Allow",
#             "Principal": {
#                 "Service": "logging.s3.amazonaws.com"
#             },
#             "Action": [
#                 "s3:PutObject"
#             ],
#             "Resource": "arn:aws:s3:::args["log_bucket"]/*",
#             "Condition": {
#                 "ArnLike": {
#                     "aws:SourceArn": "arn:aws:s3:::args["bucket_name"]"
#                 },
#                 "StringEquals": {
#                     "aws:SourceAccount": "767398027423"
#                 }
#             }
#         }
#     ]
# }	
						

# with open("server_logging_policy.json") as sv_policy:
#             sv_policy_content = sv_policy.read()
#             print(sv_policy_content)

















