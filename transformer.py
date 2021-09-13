#!/usr/bin/python3                                                                                                      
                                                                                                                        
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                          
from pyspark.streaming.kafka import KafkaUtils                                                                          
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def handle_rdd(rdd):                                                                                                    
    if not rdd.isEmpty():                                                                                               
        global ss                                                                                                       
        df = ss.createDataFrame(rdd, schema=['text', 'words', 'length', 'sentiment'])                                                
        df.show()                                                                                                       
        df.write.saveAsTable(name='default.tweets', format='hive', mode='append')                                       
                                                                                                                        
sc = SparkContext(appName="Something")                                                                                     
ssc = StreamingContext(sc, 5)                                                                                           
                                                                                                                        
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
                                                                                                                        
ss.sparkContext.setLogLevel('WARN')                                                                                     
                                                                                                                        
ks = KafkaUtils.createDirectStream(ssc, ['tweets'], {'metadata.broker.list': 'localhost:9092'})                       

sid = SentimentIntensityAnalyzer()
                                                                                                                 
lines = ks.map(lambda x: x[1])                                                                                          
                                                                                                                        
transform = lines.map(lambda tweet: (tweet, int(len(tweet.split())), int(len(tweet)), sid.polarity_scores(tweet)))                                  

transform.foreachRDD(handle_rdd)                                                                                        
                                                                                                                        
ssc.start()                                                                                                             
ssc.awaitTermination()

# CREATE TABLE tweets (text STRING, words INT, length INT, text STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\\|' STORED AS TEXTFILE;