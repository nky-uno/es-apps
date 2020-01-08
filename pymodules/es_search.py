from datetime import date
from dateutil import relativedelta
import calendar
import logging
import pandas as pd
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

def next_day(dt_now):
    year = dt_now.split('-')[0]
    month = dt_now.split('-')[1]
    d = date(int(year),int(month),1)
    nextday = d + relativedelta.relativedelta(months=1)
    return nextday.strftime('%Y-%m-%d')
 
def result(dt_now):
    elastic = get_elastic()
    
    response = elastic.search(
        index="daily",
        body={
            "aggs": {
                "range": {
                    "date_range": {
                        "field": "date",
                         "format": "yyyy-MM-dd",
                         "ranges": [
                             { "from": "{}-01".format(dt_now), "to": "{}".format(str(next_day(dt_now))) }
                         ]
                    },
                    "aggs": {
                        "histogram": {
                            "date_histogram": {
                                "field": "date",
                                "interval": "1d",
                                "order": {
                                    "_key": "desc"
                                }
                            },
                            "aggs": {
                                "by_category": {
                                    "terms": {
                                        "field": "category",
                                        "min_doc_count": 0,
                                        "order": {
                                            "_key":"asc"
                                        }
                                    },
                                    "aggs": {
                                        "count_sum": {
                                            "sum": {
                                                "field": "time"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    
    es_rows = []
    for tag1 in response['aggregations']['range']['buckets']:
        for tag2 in tag1['histogram']['buckets']:
            if (tag2['doc_count'] > 0):
                entry = {"date": tag2['key_as_string']}
                for tag3 in tag2['by_category']['buckets']:
                    entry[str(tag3['key'])] = tag3['count_sum']['value']
                es_rows.append(entry)
    
    df = pd.DataFrame(es_rows)
    return df;
