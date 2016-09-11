import hashlib

import boto3

from cfn_resource import logger, Resource as CfnResource

handler = CfnResource()


@handler.create
def create_rsc_proxy(event, context):
    """
    Return the list of strings injected into the pattern

    :param event:
    :param context:
    :return:
    """
    properties = event['ResourceProperties']

    resource_type = properties.get('Type')
    logger.info("Received property 'Type': " + str(resource_type))
    tag_operation = properties.get('Tags')
    logger.info("Received property 'Tags': " + str(tag_operation))

    # Get the appropriate resource finder
    filter_function = _get_resource_finder(resource_type)
    tag_filters = _build_tag_filters(tag_operation)

    # Request from the AWS API
    resources = filter_function(Filter=tag_filters)

    result = map(lambda resource: resource.id, resources)

    resource_id = _build_resource_id(result)

    logger.info("Generated 'resource_id': " + str(resource_id))
    logger.info("Generated 'result': " + str(result))
    return {
        'Status': 'SUCCESS',
        'Reason': 'Formatted List into string',
        'PhysicalResourceId': resource_id,
        'Data': {
            'Elements': result
        }
    }


@handler.delete
def delete_rsc_proxy(event, context):
    """
    We don't actually create anything, so there's nothing to delete.

    :param event:
    :param context:
    :return:
    """
    return {
        'Status': 'SUCCESS',
        'PhysicalResourceId': event['PhysicalResourceId'],
        'Data': {},
    }


@handler.update
def update_rsc_proxy(event, context):
    """
    Run create again, just make sure we use the same LogicalResourceId

    :param event:
    :param context:
    :return:
    """
    properties = event['ResourceProperties']

    property_list = properties.get('List')
    pattern = properties.get('Pattern')

    # Run the
    resource_id, result = _expand(property_list, pattern)
    return {
        'Status': 'SUCCESS',
        'PhysicalResourceId': resource_id,
        'Data': {
            'Elements': result
        }
    }


def _get_resource_finder(resource):
    return {
        "AWS::EC2::VPC": boto3.resource('ec2').vpcs.filter,
        'AWS::EC2::Subnet': boto3.resource('ec2').subnets.filter
    }[resource]


def _build_tag_filters(tags):
    def tag_expander(tag_pairs):
        key, value = tag_pairs
        return {
            'Name': "tag:{0}".format(key),
            'Values': [value]
        }

    return map(tag_expander, tags.items())


def _build_resource_id(result):
    """
    Using the results, generate a unique hash

    :param result:
    :return:
    """
    result_string = str(result)
    return hashlib.md5(result_string.encode()).hexdigest()
