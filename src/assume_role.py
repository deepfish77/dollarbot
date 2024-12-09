import boto3


def get_credentials(region="us-east-1", role_arn=None):
    if role_arn is None:
        role = "arn:aws:iam::840590911230:role/AdministratorAccess"
    else:
        print("getting role")
        role = role_arn
    sts_client = boto3.client("sts", region_name=region)
    print("sts_client", sts_client)
    assumed_role_object = sts_client.assume_role(
        RoleArn=role, RoleSessionName="AssumeRoleSession"
    )
    print("assumed_role_object", assumed_role_object)
    credentials = assumed_role_object["Credentials"]
    return credentials


def get_aws_resource_assume_role(resource, region="us-east-1", role_arn=None):
    credentials = get_credentials(region, role_arn)
    aws_resource = boto3.resource(
        resource,
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    return aws_resource


def resource(resource, region="us-east-1", role_arn=None):
    credentials = get_credentials(region, role_arn)
    aws_resource = boto3.resource(
        resource,
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    return aws_resource


def get_aws_client_assume_role(client, region="us-east-1", role_arn=None):
    credentials = get_credentials(region, role_arn)
    aws_client = boto3.client(
        client,
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    return aws_client


def client(client, region="us-east-1", role_arn=None):
    # Duplicate method of boto3 to execute both local and lambda
    credentials = get_credentials(region, role_arn)
    aws_client = boto3.client(
        client,
        region_name=region,
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    return aws_client
