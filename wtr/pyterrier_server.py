from flask import Flask, jsonify

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"

import pyterrier as pt
if not pt.started():
  pt.init()

app = Flask(__name__)
session = None
bm25 = None

def init():     
    index_ref = pt.IndexRef.of('./wtr/index/data.properties')
    index = pt.IndexFactory.of(index_ref)
    global bm25 
    bm25 = pt.BatchRetrieve(index , wmodel='BM25', num_results=100)

@app.route("/results/<query>", methods=['GET'])
def response(query: str):
    results = bm25.search(query)
    
    return jsonify(
        response=results.to_dict()
    )
    
if __name__ == '__main__':

    init()
    app.run(host='0.0.0.0', port=5000)