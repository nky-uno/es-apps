import logging
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from retry import retry
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

@retry(tries=3, delay=2, backoff=2)
def get_elastic():
    try:
        # connect to the Elasticsearch cluster
        elastic = Elasticsearch([{'host': 'nky.uno', 'port': 9200}])
        return elastic
    except Exception as ex:
        logging.error(ex)
        raise

@retry(tries=3, delay=2, backoff=2)
def month_list():
    try:
        elastic = get_elastic()

        response = elastic.search(
            index="daily",
            body={
                "size": 0,
                "aggs": {
                    "group_by_month": {
                        "date_histogram": {
                            "field": "date",
                            "interval": "month",
                            "format": "YYYY-MM",
                            "order": {
                                "_key": "desc"
                            }
                        }
                    }
                }
            }
        )
        es_rows = []
        for tag1 in response['aggregations']['group_by_month']['buckets']:
            es_rows.append(tag1['key_as_string'])
        return es_rows
    except Exception as ex:
        logging.error(ex)
        raise

def DateSelect():
    return dcc.Dropdown(id='date-dropdown',options=[{'label': i, 'value': i} for i in month_list()])
