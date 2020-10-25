import psycopg2
import logging
import uuid
import json

logger = logging.getLogger(__name__)

with open('db/config.json', 'r') as f:
    config = json.load(f)

# Create DB connection
def get_conn():
    logger.info('Connecting to DB...')
    conn = psycopg2.connect(database=config['DATABASE'],
                            user=config['DATABASE_USER'],
                            password=config['DATABASE_PASSWORD'],
                            host=config['DATABASE_HOST'],
                            port=config['DATABASE_PORT'])

    cur = conn.cursor()
    logger.info('Connecting to DB stablished')
    return conn, cur

def get_user(user_id):
    conn, cur = get_conn()

    logger.info('getting {} data from database...'.format(user_id))
    cur.execute("SELECT * FROM users.user WHERE id='{}'".format(user_id))
    data = cur.fetchone()

    response = {}
    for i in range(len(data)):
        response[cur.description[i][0]] = data[i]

    cur.close()
    conn.close()

    return response

def post_user(req_data):
    document = req_data['document']
    name = req_data['name']
    email = req_data['email']

    id = str(uuid.uuid4())
    logger.info('Creating record for {}...'.format(id))

    # POST data to database
    conn, cur = get_conn()
    logger.info('posting {} data to database...'.format(id))
    cur.execute("INSERT INTO users.user (id, document, name, email) VALUES ('{}', '{}', '{}', '{}')".format(id, document, name, email))
    conn.commit()
    logger.info('data from {} posted database...'.format(id))

    cur.close()
    conn.close()

    response = {'id': str(id),
                'document': document,
                'name': name,
                'email': email}

    return response

def put_user(req_data, user_id):
    document = req_data['document']
    name = req_data['name']
    email = req_data['email']

    id = user_id
    logger.info('Modifying record for {}...'.format(id))

    # POST data to database
    conn, cur = get_conn()
    logger.info('posting {} data to database...'.format(id))
    cur.execute("INSERT INTO users.user (id, document, name, email) VALUES ('{}', '{}', '{}', '{}')".format(id, document, name, email))
    conn.commit()
    logger.info('data from {} posted database...'.format(id))

    cur.close()
    conn.close()

    response = {'id': str(id),
                'document': document,
                'name': name,
                'email': email}

    return response

def delete_user(user_id):
    conn, cur = get_conn()

    logger.info('Deleting {} data from database...'.format(user_id))
    cur.execute("DELETE FROM users.user WHERE id='{}'".format(user_id))
    conn.commit()
    logger.info('Data from {} deleted from database'.format(user_id))
    cur.close()
    conn.close()

    return None

def check_existing_document(document):
    conn, cur = get_conn()
    cur.execute("SELECT * FROM users.user WHERE document='{}'".format(document))
    data = cur.fetchone()
    if data is None:
        return False
    else:
        return True