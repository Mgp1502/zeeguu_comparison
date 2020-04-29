DB10K = "mysql://root:1234@127.0.0.1/zeeguu10K?charset=utf8"

DB100K = "mysql://root:1234@127.0.0.1/zeeguu100K?charset=utf8"

DB1000K = "mysql://root:1234@127.0.0.1/zeeguu?charset=utf8"

# Example of a elastic connection string: USERNAME:PASSWORD@127.0.0.1:9200
# if working without user and password, '127.0.0.1:9200' will suffice
ES_CONN_STRING = '127.0.0.1:9200'
# what indices to use in elasticsearch for 10K, 100K, and the full database (~1000K)
ES_INDEX10K = 'zeeguu_articles10k'
ES_INDEX100K = 'zeeguu_articles100k'
ES_INDEX = 'zeeguu_articles'
