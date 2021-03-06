import boto3.ec2
from configAWSEnv.connection import connect_to_ec2_resources, connect_to_ec2
from configAWSEnv.const import WAKEUP, SHUTDOWN
from configAWSEnv.prints import print_and_exit
from configAWSEnv.parser import parse_args

'''
Main ASW functionality
- Get the list of instance to run on according to the AWS filter
- Get the required action (start or stop the instances)
- Run and verify state after instance status change.
- If fails - return AWS console URL with the list of problematic instances
'''


def list_instances_by_tag_value(action, filters):
    # When passed a tag key, tag value this will return a list of InstanceIds that were found.
    # append instance state
    ec2client = connect_to_ec2()
    if action == WAKEUP:
        filters.append( {'Name': 'instance-state-name', 'Values': ['{}'.format('stopped')]})
    elif action == SHUTDOWN:
        filters.append( {'Name': 'instance-state-name', 'Values': ['{}'.format('running')]})

    response = ec2client.describe_instances(
        Filters=filters
    )

    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])

    return instancelist


def configure_environment(action, environment):
    ec2resourcers = connect_to_ec2_resources()
    if len(environment) == 0:
        print("No instances found in the environment, check your tags and filters")
        return 1
    if action == WAKEUP:
        ec2resourcers.instances.filter(InstanceIds=environment).start()

        # wait till all instances start
        for instance in environment:
            ec2resourcers.Instance(instance).wait_until_running()
    elif action == SHUTDOWN:
        ec2resourcers.instances.filter(InstanceIds=environment).stop()
        # wait till all instances stop
        for instance in environment:
            ec2resourcers.Instance(instance).wait_until_stopped()
    return 0


def validate_env_status(action, filters):
    new_environment = list_instances_by_tag_value(action, filters)
    if len(new_environment) > 0:
        print_and_exit("Failed to {} environment, "
                       "\nsee instances with unknown status in AWS console:\n {}".format(action, create_aws_url(
            new_environment)), 2)
    else:
        print("environment {} successfully".format(action))

    return new_environment


def get_region():
    my_session = boto3.session.Session()
    return my_session.region_name


def create_aws_url(bad_instances):
    # open browser with instances
    base_url = "https://console.aws.amazon.com/ec2/v2/home"
    region_prefix = "?region="
    region = get_region()
    instances_search = "#Instances:search="
    instances_ids = ""
    sort = ";sort=instanceState"
    for bad_instance in bad_instances:
        instances_ids += bad_instance + ","
    url = base_url + region_prefix + region + instances_search + instances_ids + sort
    return url


def main(*args):
    action, filters = parse_args()
    environment = list_instances_by_tag_value(action=action, filters=filters)
    if not len(environment) > 0:
        print_and_exit("No instances found in the environment", 2)
    print("running on AWS region: {}".format(get_region()))
    print("{} called for the following instances: {}".format(action, environment))

    configure_environment(action, environment)
    validate_env_status(action=action, filters=filters)








