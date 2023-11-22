from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS

from api import get_taxonomy, lowest_price #added to top of file
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/getalltaxonomies', methods=['GET'])
def getalltaxonomies():
    return jsonify((get_taxonomy()))

@app.route('/api/getitemsbytaxonomie', methods=['POST'])
def api_get_users():
    taxonomies = request.get_json() # [12, 1223, 32241]
    return jsonify(lowest_price(taxonomies))

if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run() #run app