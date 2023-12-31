from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
import os
import pyterrier as pt
import pandas as pd
import gc

app = Flask(__name__)
Base = declarative_base() 
session = None
bm25 = None
index = None
last_query = None

class TableQuery(Base):
    __tablename__ = 'tablequery'
    docno = Column(String, primary_key=True)
    querygen = Column(Text)
    
    def __repr__(self):
        repr_str = f"docno={self.docno}, query={self.querygen}"
        return repr_str

class TableQueries(Base):
    __tablename__ = 'doc2queries'
    docno = Column(String, primary_key=True)
    querygen = Column(ARRAY(Text))

    def __repr__(self):
        repr_str = f"docno={self.docno}, query={self.querygen}"
        return repr_str

def init():   
    if not pt.started():
        pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"])

    global bm25
    global session
    global index

    index_ref = pt.IndexRef.of('./index/data.properties')
    index = pt.IndexFactory.of(index_ref)
    bm25 = pt.BatchRetrieve(index , wmodel='BM25', num_results=100)

    engine = create_engine("postgresql://root@postgres:5432/webtables_db")
    Session = sessionmaker(bind=engine)
    session = Session()

@app.route("/doc2query/<docno_request>", methods=['GET'])
def response_d2q(docno_request: str):
    if docno_request:
        docno_request = docno_request.replace("$", "/")
        result = session.get(TableQueries, docno_request)
        if result:
            result = result.querygen
        else:
            return "docno not found"
    else:
        return "no argument given"

    return jsonify(
        response_d2q=result
    )

@app.route("/results/<query>", methods=['GET'])
def response_query(query: str):
    #Sgc.collect()
    results = bm25.search(query)
    global last_query

    last_query = query
    return jsonify(
        response_query=results.to_dict()
    )

@app.route("/results_rm3/<rel_docs>", methods=['GET'])
def response_query_rm3(rel_docs: str):
    
    global last_query

    if rel_docs == "no_rels":
        rel_docs = []
    else:
        rel_docs = set([rel_doc.replace("$", "/") for rel_doc in rel_docs.split(',')])

    # push rel docs to the top

    rel_pusher = pt.apply.doc_score(lambda row: 9000 if row['docno'] in rel_docs else row['score'])
    

    '''
    test_p = bm25 >> rel_pusher
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(test_p.search(last_query))
    '''
    print(last_query)

    rm3_pipe = bm25 >> rel_pusher >> pt.rewrite.RM3(index) >> bm25
    results = rm3_pipe.search(last_query)

    last_query = results['query'][0]

    return jsonify(
        response_query=results.to_dict()
    )

if __name__ == '__main__':

    init()
    app.run(host='0.0.0.0', port=5000)

