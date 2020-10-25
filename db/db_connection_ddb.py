import logging
import uuid
import json
import boto3

logger = logging.getLogger(__name__)

with open('db/config.json', 'r') as f:
    config = json.load(f)

# Create DB connection
ddb = boto3.resource('dynamodb',
                     aws_access_key_id=config['AWS_ACCESS_KEY'],
                     aws_secret_access_key=config['AWS_SECRET_KEY'],
                     aws_session_token=config['AWS_SESSION_TOKEN'],
                     region_name=config['AWS_REGION'])

users_table = ddb.Table('users')

def get_user(user_id):

    logger.info('getting {} data from database...'.format(user_id))
    data = users_table.get_item(
            Key={
                    'id': user_id
                }
            )
    data = data['Item']

    response = {}
    for i in data.keys():
        response[i] = data[i]

    return response

def post_user(req_data):
    document = req_data['document']
    name = req_data['name']
    email = req_data['email']

    id = str(uuid.uuid4())
    logger.info('Creating record for {}...'.format(id))

    # POST data to database
    users_table.put_item(
        Item={
            'id': id,
            'document': str(document),
            'name': str(name),
            'email': str(email)
        }
    )
    logger.info('data from {} posted database...'.format(id))

    response = {'id': str(id),
                'document': document,
                'name': name,
                'email': email}

    return response

def delete_user(user_id):

    logger.info('Deleting {} data from database...'.format(user_id))
    users_table.delete_item(
        Key={
            'id': user_id
        }
    )
    logger.info('Data from {} deleted from database'.format(user_id))

    return None
