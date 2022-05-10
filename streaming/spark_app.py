import socket
import time
import sys
import requests
import re
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import count, avg, col
from pyspark.sql import SQLContext
import pyspark.sql.functions as f

def aggregate_count(new_values, total_sum):
	return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
    if('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SparkSession(spark_context)
    return globals()['sqlContextSingletonInstance']

def send_repo_count_df_to_dashboard(df, time):
    url = f'http://webapp:5000/updateRepoCountData/{time}'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def send_avg_stars_df_to_dashboard(df):
    url = 'http://webapp:5000/updateAvgStarsData'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def send_python_word_counts_df_to_dashboard(df):
    url = 'http://webapp:5000/updatePythonWordCounts'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def send_java_word_counts_df_to_dashboard(df):
    url = 'http://webapp:5000/updateJavaWordCounts'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def send_csharp_word_counts_df_to_dashboard(df):
    url = 'http://webapp:5000/updateCSharpWordCounts'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def process_rdd(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(repoName=w[0][0], language=w[0][1], stars=w[0][2], description=re.sub('[^a-zA-Z ]', '', w[0][3].strip()), count=w[1]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")

        repo_counts_by_lang_df = results_df.groupBy("language").agg(count("repoName"))
        avg_stars_by_lang_df = results_df.groupBy("language").agg(avg("stars"))
        word_counts_df = results_df.withColumn('word', f.explode(f.split(f.col('description'), '\\s+'))) \
        .groupBy('word', 'language') \
        .count() \
        .sort('count', ascending=False)

        print("Total repo count, average stars by language thus far:")
        
        repo_counts_by_lang_df.join(avg_stars_by_lang_df, ["language"]).show()

        print("Top 10 words in descriptions by language thus far:")

        csharp_word_counts = word_counts_df.where(word_counts_df.language=="C#")
        python_word_counts = word_counts_df.where(word_counts_df.language=="Python")
        java_word_counts = word_counts_df.where(word_counts_df.language=="Java")
        csharp_word_counts = csharp_word_counts.where(csharp_word_counts.word!='').limit(10)
        python_word_counts = python_word_counts.where(python_word_counts.word!='').limit(10)
        java_word_counts = java_word_counts.where(java_word_counts.word!='').limit(10)
        
        csharp_word_counts.show()
        python_word_counts.show()
        java_word_counts.show()
        send_repo_count_df_to_dashboard(repo_counts_by_lang_df, time)
        send_avg_stars_df_to_dashboard(avg_stars_by_lang_df)
        send_python_word_counts_df_to_dashboard(python_word_counts)
        send_java_word_counts_df_to_dashboard(java_word_counts)
        send_csharp_word_counts_df_to_dashboard(csharp_word_counts)

    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

    
if __name__ == "__main__":
    DATA_SOURCE_IP = "data-source"
    DATA_SOURCE_PORT = 9999
    sc = SparkContext(appName="githubRepos")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 60)
    ssc.checkpoint("checkpoint_githubRepos")
    data = ssc.socketTextStream(DATA_SOURCE_IP, DATA_SOURCE_PORT)
    repos = data.map(lambda x: x.split("$#(DELIMITER)#$"))
    counts = repos.map(lambda repo: (tuple([repo[0], repo[1], int(repo[2]), repo[3]]), 1)).reduceByKey(lambda a, b: a+b)
    windowed_counts = counts.map(lambda repo: ("Python" if repo[0][1] == "Python" else ("Java" if repo[0][1] == "Java" else "C#"), 1)).reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y: x - y, 60, 60)
    windowed_counts.pprint()
    aggregated_counts = counts.updateStateByKey(aggregate_count)
    aggregated_counts.foreachRDD(process_rdd)
    ssc.start()
    ssc.awaitTermination()