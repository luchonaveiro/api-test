from flask import Flask, Response, request, jsonify, make_response
import json
import logging
import os
import sys
import db.db_connection as db

# Define logger
logging.basicConfig(stream=sys.stdout,
                    level=logging.getLevelName(os.getenv('LOGLEVEL', 'INFO')),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Define user endpoint
@app.route('/users', defaults={'user_id':''}, methods=['POST'])
@app.route('/users/<path:user_id>', methods=['GET','DELETE','PUT'])
def post_endpoint(user_id):
    if request.method == 'GET':
        # GET data from database
        response = db.get_user(user_id)

        logger.info('Response:')
        logger.info(response)

        resp = Response(json.dumps(response), 
                        status=200, 
                        mimetype='application/json')
        return resp

    
    elif request.method == 'POST':
        req_data = request.get_json()

        if req_data.get('document') is not None and req_data.get('name') is not None and req_data.get('email') is not None: 
            existing_document = db.check_existing_document(req_data['document'])
    
            if existing_document:
                response = {'message': 'Document {} already exists in Database'.format(req_data['document'])}
            
            else:
                response = db.post_user(req_data)
                
                logger.info('Response:')
                logger.info(response)
        else:
            response = {'message': 'Please enter name, document and mail'}

        resp = Response(json.dumps(response),
                        status=200,
                        mimetype='application/json')
        return resp

    
    elif request.method == 'PUT':
        req_data = request.get_json()

        if req_data.get('document') is not None and req_data.get('name') is not None and req_data.get('email') is not None: 
            db.delete_user(user_id)

            response = db.put_user(req_data, user_id)
            
            logger.info('Response:')
            logger.info(response)
        else:
            response = {'message': 'Please enter name, document and mail'}

        resp = Response(json.dumps(response),
                        status=200,
                        mimetype='application/json')
        return resp    


    elif request.method == 'DELETE':
        db.delete_user(user_id)
        
        resp = Response(None,
                        status=200,
                        mimetype='application/json')
        return resp

    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)