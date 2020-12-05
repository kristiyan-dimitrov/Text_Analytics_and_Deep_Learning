import logging

import os
import flask
from flasgger import Swagger # Used for Documentation
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from src.preprocess import preprocess
from src.predict import predict, categories

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Flask application
application = Flask(__name__)

application.config['ALLOWED_EXTENSIONS'] = set(['pdf'])
application.config['CONTENT_TYPES'] = {"pdf": "application/pdf"}
application.config["Access-Control-Allow-Origin"] = "*"

CORS(application)

swagger = Swagger(application)


def clienterror(error):
    resp = jsonify(error)
    resp.status_code = 400
    return resp


def notfound(error):
    resp = jsonify(error)
    resp.status_code = 404
    return resp


@application.route('/v1/multilabel', methods=['POST']) # This defines the endpoint as a URL # It's POST, because its expecting to receive some information
def sentiment_classification():
    """Run multi-label boardgame classification given boardgame description.
        ---
        parameters:
          - name: body
            in: body
            schema:
              id: description
              required:
                - description
              properties:
                description:
                  type: [string]
            description: the required boardgame description for POST method
            required: true
        definitions:
          SentimentResponse:
          Project:
            properties:
              status:
                type: string
              ml-result:
                type: object
        responses:
          40x:
            description: Client error
          200:
            description: Multi-label Boardgame Categorization
            examples:
                          [
{
  "status": "success",
  "sentiment": "1"
},
{
  "status": "error",
  "message": "Exception caught"
},
]
        """
    json_request = request.get_json() # Getting whatever you sent to service
    if not json_request:
        return Response("No json provided.", status=400) # If you sent nothing, we throw error
    description = json_request['description']
    if description is None:
        return Response("No text provided.", status=400)
    else:
        preprocessed_description = preprocess(description)
        predicted_categories = predict(preprocessed_description)
        return flask.jsonify({"status": "success", "predicted_categories": predicted_categories.tolist()}) # Returning an answer to the POST request; the .jsonify part will put HTTP status 200


@application.route('/v1/multilabel/categories', methods=['GET'])
def multilabel_categories():
    """Possible boardgame categories.
        ---
        definitions:
          CategoriestResponse:
          Project:
            properties:
              categories:
                type: object
        responses:
          40x:
            description: Client error
          200:
            description: Sentiment Classification Response
            examples:
                          [
{
  "categories": [1,2,3],
  "sentiment": "1"
}
]
        """
    return flask.jsonify({"categories": list(categories)})


if __name__ == '__main__':
    application.run(debug=True, use_reloader=True)