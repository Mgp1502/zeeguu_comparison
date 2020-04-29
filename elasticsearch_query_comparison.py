import os

from elasticsearch import Elasticsearch
import sqlalchemy as database
from sqlalchemy.orm import sessionmaker
from zeeguu_core.elastic.elastic_query_builder import build_elastic_query
from mysql_queries import mysql_fulltext_query, base_mysql_query
from timeit import default_timer as timer
from zeeguu_core.model import Language
import csv
from compare_settings import *


def query_performance(mysql, index, size_of_index, size, content, topics,
                      unwanted_topics, user_topics, unwanted_user_topics):
    language = Language("en", "English")
    language.id = 5

    elastic_query_body = build_elastic_query(size, content, topics, unwanted_topics,
                            user_topics, unwanted_user_topics, language, 100, 0)

    mysql_query_full_text = mysql_fulltext_query(mysql, size, content, topics, unwanted_topics,
                                                 user_topics, unwanted_user_topics, language, 100, 0)

    mysql_query_old = base_mysql_query(mysql, size, content, topics, unwanted_topics,
                                       user_topics, unwanted_user_topics, language, 100, 0)

    elastic_time_lst = []
    elastic_returned_articles = []
    for j in range(20):
        start = timer()
        res = es.search(index=index, body=elastic_query_body)
        elastic_returned_articles.append(len(res['hits'].get('hits')))
        end = timer()
        elastic_time_lst.append(end - start)

    write_results_to_csv(size_of_index + " elastic", average_time_in_ms(elastic_time_lst), size)

    # #MySQL Full Text
    mysql_time_lst = []
    mysql_returned_articles = []
    for i in range(10):
        start = timer()
        result = mysql_query_full_text.all()
        mysql_returned_articles.append(len(result))
        end = timer()
        mysql_time_lst.append(end-start)

    write_results_to_csv(size_of_index + " MySQL Full Text", average_time_in_ms(mysql_time_lst),
                         size)

    # MySQL Base Version
    mysql_time_lst = []
    mysql_returned_articles = []
    for i in range(10):
        start = timer()
        result = mysql_query_old.all()
        mysql_returned_articles.append(len(result))
        end = timer()
        mysql_time_lst.append(end - start)

    write_results_to_csv(size_of_index + " MySQL Base Version", average_time_in_ms(mysql_time_lst),
                         size)


def average_time_in_ms(lst):
    return (sum(lst) / len(lst))*1000


def average(lst):
    return sum(lst) / len(lst)


def write_results_to_csv(index, time, asked_for):
    file_exists = os.path.isfile(title_of_csv)
    path = os.path.join('output', title_of_csv)
    with open(path, 'a', newline='') as csvfile:
        fieldnames = ['Index', "Time in MS", "Asked for articles"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({'Index': index, 'Time in MS': time, 'Asked for articles': asked_for})


def run(sessions, requested_articles):
    for session in sessions:
        for nb_articles in requested_articles:
            query_performance(session[0], session[2], session[1], nb_articles, content, wanted_topics,
                              unwanted_topics, wanted_user_topics, unwanted_user_topics)

    print('Done with difficulty 5')


if __name__ == '__main__':
    es = Elasticsearch([ES_CONN_STRING])
    # here declare the search parameters to use in the comparison.

    #
    content = 'trump'
    wanted_topics = ''
    unwanted_topics = ''
    wanted_user_topics = ''
    unwanted_user_topics = ''

    engine10k = database.create_engine(DB10K)
    Session10k = sessionmaker(bind=engine10k)
    session10k = Session10k()

    engine100k = database.create_engine(DB100K)
    Session100k = sessionmaker(bind=engine100k)
    session100k = Session100k()

    engine1000k = database.create_engine(DB1000K)
    Session1000k = sessionmaker(bind=engine1000k)
    session1000k = Session1000k()

    session_lst = [(session10k, '10k', ES_INDEX10K),
                   (session100k, '100k', ES_INDEX100K),
                   (session1000k, '1000k', ES_INDEX)]

    # name of the CSV to save the results,
    title_of_csv = 'trump_english.csv'

    # add the different mysql sessions to a list, together with what elasticsearch index to use
    session_lst = [(session10k, '10k', ES_INDEX10K),
                   (session100k, '100k', ES_INDEX100K),
                   (session1000k, '1000k', ES_INDEX)]

    requested_articles_lst = [10, 20, 50, 100]
    run(session_lst, requested_articles_lst)

