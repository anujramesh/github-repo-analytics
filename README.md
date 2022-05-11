# Real-Time Streaming Analytics of GitHub Repos with Apache Spark, Docker, and Flask

## Introduction
This project performs real-time streaming analytics for public repositories hosted on GitHub. The system runs a stream processing pipeline, where the live data stream to be analyzed is coming from GitHub API. An Apache Spark cluster processes the data stream. A web application receives the output from Spark and visualizes the analysis result.

## Description of the System Architecture
![System Architecture](System_Architecture.png)

This application consists of four components, as illustrated in the diagram above. Firstly, the Data Source Service makes a request to the 
GitHub API to retrieve repository data. The GitHub API sends it the 
repository data in JSON format. The Data Source Service then takes 
only the relevant information from the JSON, streams it over to the 
Apache Spark Cluster via TCP. The Apache Spark Cluster then 
analyzes this data and sends some key statistics over to the Webapp 
Service, which uses these statistics to show graphical visualizations. Finally, 
the user can see these visualized statistics by visiting the webapp 
service through localhost:5000.

## Implementation

### Data Source Service
The data source service is implemented in `data_source.py`. This service listens 
to port 9999, waiting for another service to connect. Once a connection has been established, it 
makes a get request to the GitHub API every 15 seconds. It iterates through the JSON object it 
receives, and gets the repo’s full name, its primary language, its star count, and its description. It 
then takes these values and puts it into a string separated by delimiters and ending with a newline 
character. It encodes the data and sends it over to spark application.

### Data Source Service
The spark application, implemented in `spark_app.py`, gets a stream of data from the data source via 
TCP connection. It performs the following:

1. Creates batches of 60 seconds, where the data is stored. socketTextStream 
separates each element of data based on newline characters.
2. Maps each repo splitting each string by the delimiter, such that each of the repos’ name, 
language, stars, and description can be separately identified. 
3. Maps each repo into a key, value pair, where keys represent a tuple of the repo’s name, language, stars, description, and 
value is 1. 
4. Reduces by key based on if there are repeating (non-unique) repositories. 
5. Updates state by key
6. After it is able to perform map reduce on the repos and update state by key, it then converts the RDD into a 
dataframe in order to compute the following:
   1. Total number of the collected repositories since the start of the streaming application for each of the three programming languages. Each repository counts towards the result only once.
   2. Number of the collected repositories with changes pushed during the last 60 seconds. Each repository counts towards the result only once during a batch interval (60 seconds).
   3. Average number of stars of all the collected repositories since the start of the streaming application for each of the three programming languages. Each repository counts towards the result only once.
   4. Top 10 most frequent words in the description of all the collected repositories since the start of the streaming application for each of the three programming languages. Each repository counts towards the result only once.

7. Prints the analysis results for each batch.

9. Passes these statistics over to the webapp service.


### 3. Web Application
The web application visualizes the analysis results in real-time, which doesn't need to be fancy. A simple dashboard such as shown in the figure below would suffice. You can easily create a web application using web frameworks, such as [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [Django](https://www.djangoproject.com/). Also, a simple [Flask-based dashboard](https://github.com/pacslab/big-data-systems-docker/blob/main/spark/app/nine-multiples/webapp/flask_app.py) is presented in Lab 7. You can modify its source code to implement the web application for this project.

<img src="Webapp.png" alt="Webapp Screenshot" width="500"/>
