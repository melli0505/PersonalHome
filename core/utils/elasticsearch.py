
from elasticsearch import Elasticsearch # , RequestsHttpConnection


es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "https"}], http_auth=('elastic', 'elastic'), verify_certs=False)
