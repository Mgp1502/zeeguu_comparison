# zeeguu_comparison
Code for comparing text search between MySQL, MySQL-fulltext and Elasticsearch on the Zeeguu Ecosystem (https://github.com/zeeguu-ecosystem)
Used in bachelor project at ITU.

##Install/setup
1. Download and setup https://github.com/zeeguu-ecosystem/Zeeguu-Core:
    + This project references to some of the classes in Zeeguu-Core, so Zeeguu-Core and zeeguu_comparison needs to be located in the same folder.
    also remember to follow the install guide as to how to install elasticsearch. 
2. Download this project and run pip install -r requirements: 
    + Make sure it is the same environment as used for the Zeeguu-Core
3. Get X amount of articles and make databases and indexes of different sizes:
    + The program is designed around having 3 different database and elasticsearch indexes of various sizes: 10K, 100K, and 1000K. 
    This was to test the scalability of the different technologies. 
4. Create a MySQL fulltext index on (title, content) in all of the databases: 
    + ALTER TABLE article
    ADD FULLTEXT(content, title);
    + can take some time on the big databases
5. Open up the compare_settings.py and fill in the settings for your setup.

##Elasticsearch_query_comparison.py
1. Open up elasticsearch_query_comparison.py and in the main function define what search parameters to use.
2. Run python elasticsearch_query_comparison.py to create a CSV in the output folder.
3. Change the path in the elasticsearch_statistical_analyser.py to the newly generated CSV.
4. Run elasticsearch_statistical_analyser.py to get a plot

For a test with simulating, concurrent users, run the concurrent_test.bat script. Be prepared that it 
sometimes makes empty line in the resulting CSV, that needs to be removed for before creating a plot. 

##Elasticsearch_relevance_test.py
1. Open up Elasticsearch_relevance_test.py and in the main function define what search parameters to use.
2. Run it to produce a CSV file containing the results from MySQL fulltext and elasticsearch with the same parameters
    + then it is possible to manually look at what technology found the best results.   





