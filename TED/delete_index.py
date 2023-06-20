#python 3.7.1
from elasticsearch import Elasticsearch
es=Elasticsearch()
E=es.indices.exists(index="ted")
if E:
  es.indices.delete(index="ted")
