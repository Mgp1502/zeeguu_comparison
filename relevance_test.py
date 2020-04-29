import os

from elasticsearch import Elasticsearch
import sqlalchemy as database
from sqlalchemy.orm import sessionmaker
from zeeguu_core.elastic.elastic_query_builder import build_elastic_query
from comparison.mysqlFullText import mysql_fulltext_query
from timeit import default_timer as timer
from zeeguu_core.model import Language
from compare_settings import *
import csv

es = Elasticsearch([ES_CONN_STRING])


def query_performance(mysql, index, size, content, topics,
                      unwanted_topics, user_topics, unwanted_user_topics):
    language = Language("en", "English")
    language.id = 5
    # build elasticsearch query
    query_body = build_elastic_query(size, content, topics, unwanted_topics,
                            user_topics, unwanted_user_topics, language, 100, 0)
    # build Mysql query
    mysql_query = mysql_fulltext_query(mysql, size, content, topics, unwanted_topics,
                                       user_topics, unwanted_user_topics, language, 100, 0)
    # Elasticsearch
    res = es.search(index=index, body=query_body)
    for result in res['hits']['hits']:
        elastic_title = result['_source']['title']
        elastic_content = result['_source']['content']
        published_time = result['_source']['published_time']
        write_results_to_csv("elastic", elastic_title, elastic_content, published_time)

    # Mysql
    result = mysql_query.all()
    for mysql_result in result:
        mysql_title = mysql_result.title
        mysql_content = mysql_result.content
        published_time = mysql_result.published_time
        write_results_to_csv("mysql_full_text", mysql_title, mysql_content, published_time)



def average_time(lst):
    return (sum(lst) / len(lst))*1000


def average(lst):
    return sum(lst) / len(lst)


def write_results_to_csv(name, title, content, published_time):
    file_exists = os.path.isfile(title_of_csv)
    with open(title_of_csv, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Technology', "Title", 'Content', 'Published Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({'Technology': name, 'Title': title,
                         'Content': content, 'Published Time': published_time})


def run(sessions, requested_articles):
    for session in sessions:
        for nb_articles in requested_articles:
            query_performance(session[0], session[2], session[1], nb_articles, content, wanted_topics,
                              unwanted_topics, wanted_user_topics, unwanted_user_topics)

    print('Done')


if __name__ == '__main__':

    content = "soccer"
    wanted_topics = ''
    unwanted_topics = ''
    wanted_user_topics = ''
    unwanted_user_topics = 'the great depression'

    engine1000k = database.create_engine(DB1000K)
    Session1000k = sessionmaker(bind=engine1000k)
    session1000k = Session1000k()

    title_of_csv = 'Relevance_test.csv'

    session_lst = [(session1000k, '1000k', ES_INDEX)]
    requested_articles_lst = [10]
    run(session_lst, requested_articles_lst)
