import pandas as pd
import requests 
import json

from simiir.search_interfaces import Document
from simiir.search_interfaces.base_interface import BaseSearchInterface

from ifind.search.response import Response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text, ARRAY
from simiir.search_contexts.search_context import SearchContext

Base = declarative_base()

class Table(Base):
    __tablename__ = 'webtables'
    docno = Column(String, primary_key=True)
    table_content = Column(Text)
    textBefore = Column(Text)
    textAfter = Column(Text)
    pageTitle = Column(String)
    title = Column(String)
    entities = Column(Text)
    url = Column(String)
    orientation = Column(String)
    header = Column(String)
    key_col = Column(String)
    relation = Column(ARRAY(String, dimensions=2))
    
    def __repr__(self):
        repr_str = f"docno={self.docno}, table_content={self.table_content}, textBefore={self.textBefore}, textAfter={self.textAfter},"\
        f"pageTitle={self.pageTitle}, title={self.title}, entities={self.entities}, url={self.url}, orientation={self.orientation},"\
        f"header={self.header}, key_col={self.key_col}"
        
        return repr_str
    
    
def fetch_and_parse(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
            return
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
            return
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
            return
        except requests.exceptions.RequestException as err:
            print ("Something went wrong", err)
            return
        try:
            data = json.loads(response.text)
            return data
        except json.JSONDecodeError as e:
            print("Failed to decode:", e)
            return

class PyterrierWebSearchInterface(BaseSearchInterface):
    """

    """
    def __init__(self):
        self._last_response = None
        self._last_query = None
        
        conn_string = 'postgresql://root@postgres:5432/' + "webtables_db"
        engine = create_engine(conn_string)
        Session = sessionmaker(bind=engine)
        self._session = Session()
        self._filter_seen_rel = False
        self._search_context = None
    
    def issue_query(self, query, num_results=100):
        """
        Allows one to issue a query to the underlying search engine. 
        """

        
        url = 'http://172.23.0.4:5000/results/'
        url_request = url + query.terms.decode('UTF-8')
        _results = fetch_and_parse(url_request).get('response_query') 
        results = pd.DataFrame.from_dict(_results)
 
        response = Response(query_terms=query.terms.decode('UTF-8'), query=query)
        
        for result in results.iterrows():
            
            #filter out seen relevant docs
            _docno = result[1].docno
            if self._filter_seen_rel:

                rel_docs = set([str(doc.doc_id)[2:-1] for doc in self._search_context.get_relevant_documents()])
                if _docno in rel_docs:
                    continue

            record = self._session.query(Table).filter_by(docno=_docno).first()

            if record:
                response.add_result(title=' '.join([record.pageTitle,record.title]),
                                    url=record.url,
                                    summary=' '.join([record.textBefore,record.textAfter]),
                                    docid=_docno,
                                    rank=result[1]['rank'] + 1,
                                    score=result[1].score,
                                    content=record.table_content,
                                    whooshid=_docno)
            
        response.result_total = len(results)
        
        self._last_query = query
        self._last_response = response
        
        return response
    
    def get_document(self, document_id):
        """
        Retrieves a Document object for the given document specified by parameter document_id.
        """
        
        record = self._session.query(Table).filter_by(docno=document_id.decode('utf-8')).first()
        title = ' '.join([record.pageTitle, record.title])
        content = record.table_content
        document = Document(id=document_id, title=title, content=content, doc_id=document_id)
        
        return document

    def set_filter(self, filter, search_context : SearchContext):
        self._filter_seen_rel = filter
        self._search_context = search_context