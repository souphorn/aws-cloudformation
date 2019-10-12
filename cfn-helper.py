from crhelper import CfnResource
helper = CfnResource(
	json_logging=False,
	log_level='DEBUG', 
	boto_level='CRITICAL'
)


def handler(event, context):
    helper(event, context)
    
    
@helper.create
def create(event, context):
    logger.info("Got Create")
    
    # Items stored in helper.Data will be saved 
    # as outputs in your resource in CloudFormation
    helper.Data.update({"test": "testdata"})
    return "MyResourceId"


@helper.update
def update(event, context):
    logger.info("Got Update")
    return "MyNewResourceId"


@helper.delete
def delete(event, context):
    logger.info("Got Delete")