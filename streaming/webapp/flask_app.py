from flask import Flask, jsonify, request, render_template
from redis import Redis
import matplotlib.pyplot as plt
import json
from datetime import datetime
import matplotlib.dates
import time

app = Flask(__name__)

python_counts = [0]
java_counts = [0]
csharp_counts = [0]
python_repo_count_per_batch = []
java_repo_count_per_batch = []
csharp_repo_count_per_batch = []
times = []

@app.route('/updateRepoCountData/<time>', methods=['POST'])
def updateRepoCountData(time):
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('repo_count_data', json.dumps(data))
    global times, python_counts, java_counts, csharp_counts, python_repo_count_per_batch, java_repo_count_per_batch, csharp_repo_count_per_batch
    times.append(datetime.fromisoformat(time))
    
    try:
        python_count_index = data['language'].index('Python')
        # yes_index = data['isMultipleOf9'].index('Yes')
        python_repo_count = data['count(repoName)'][python_count_index]
        # isMultipleOf9 = data['count'][yes_index]
    except ValueError:
        python_repo_count = 0
    try:
        # notMultipleOf9 = data['count'][1 - yes_index]
        csharp_count_index = data['language'].index('C#')
        csharp_repo_count = data['count(repoName)'][csharp_count_index]
    except ValueError:
        csharp_repo_count = 0
    try:
        java_count_index = data['language'].index('Java')
        java_repo_count = data['count(repoName)'][java_count_index]
    except ValueError:
        java_repo_count = 0
    
    # labels.append(datetime.now())
    python_counts.append(python_repo_count)
    java_counts.append(java_repo_count)
    csharp_counts.append(csharp_repo_count)
    python_repo_count_per_batch.append(python_counts[-1] - python_counts[-2])
    java_repo_count_per_batch.append(java_counts[-1] - java_counts[-2])
    csharp_repo_count_per_batch.append(csharp_counts[-1] - csharp_counts[-2])
    return jsonify({'msg': 'success'})

@app.route('/updateAvgStarsData', methods=['POST'])
def updateAvgStarsData():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('repo_avg_star_data', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/updatePythonWordCounts', methods=['POST'])
def updatePythonWordCounts():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('python_word_count_data', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/updateJavaWordCounts', methods=['POST'])
def updateJavaWordCounts():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('java_word_count_data', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/updateCSharpWordCounts', methods=['POST'])
def updateCSharpWordCounts():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('csharp_word_count_data', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/', methods=['GET'])
def index():
    global times, python_counts, java_counts, csharp_counts, python_repo_count_per_batch, java_repo_count_per_batch, csharp_repo_count_per_batch
    r = Redis(host='redis', port=6379)

    # Avg star data
    repo_avg_star_data = r.get('repo_avg_star_data')
    try:
        repo_avg_star_data = json.loads(repo_avg_star_data)
    except TypeError:
        return "waiting for data..."
    try:
        python_avg_stars_index = repo_avg_star_data['language'].index('Python')
        python_avg_stars = repo_avg_star_data['avg(stars)'][python_avg_stars_index]
    except ValueError:
        python_avg_stars = 0
    try:
        csharp_avg_stars_index = repo_avg_star_data['language'].index('C#')
        csharp_avg_stars = repo_avg_star_data['avg(stars)'][csharp_avg_stars_index]
    except ValueError:
        csharp_avg_stars = 0
    try:
        java_avg_stars_index = repo_avg_star_data['language'].index('Java')
        java_avg_stars = repo_avg_star_data['avg(stars)'][java_avg_stars_index]
    except ValueError:
        java_avg_stars = 0
    
    
    # x_axis = matplotlib.dates.date2num(labels)
    plt.clf()
    plt.plot(times, python_repo_count_per_batch, color="blue", label="Python")
    plt.plot(times, java_repo_count_per_batch, color="orange", label="Java")
    plt.plot(times, csharp_repo_count_per_batch, color="green", label="C#")
    plt.xticks(ticks=times, labels=times)
    plt.xlabel('Time')
    plt.ylabel('#repositories')
    plt.legend()
    
    plt.savefig('/streaming/webapp/static/images/linechart.png')
    
    # Bar graph 
    plt.clf()
    x = [1, 2, 3]
    height = [python_avg_stars, csharp_avg_stars, java_avg_stars]
    tick_label = ['Python', 'C#', 'Java']
    plt.bar(x, height, tick_label=tick_label, width=0.8, color=['tab:blue', 'tab:orange', 'tab:green'])
    plt.ylabel('Average number of stars')
    plt.xlabel('PL')
    plt.savefig('/streaming/webapp/static/images/bargraph.png')

    python_word_count_data = r.get('python_word_count_data')
    try:
        python_word_count_data = json.loads(python_word_count_data)
    except TypeError:
        return "waiting for data..."
    try:
        python_word1 = python_word_count_data['word'][0]
        python_word2 = python_word_count_data['word'][1]
        python_word3 = python_word_count_data['word'][2]
        python_word4 = python_word_count_data['word'][3]
        python_word5 = python_word_count_data['word'][4]
        python_word6 = python_word_count_data['word'][5]
        python_word7 = python_word_count_data['word'][6]
        python_word8 = python_word_count_data['word'][7]
        python_word9 = python_word_count_data['word'][8]
        python_word10 = python_word_count_data['word'][9]

        python_word_count1 = python_word_count_data['count'][0]
        python_word_count2 = python_word_count_data['count'][1]
        python_word_count3 = python_word_count_data['count'][2]
        python_word_count4 = python_word_count_data['count'][3]
        python_word_count5 = python_word_count_data['count'][4]
        python_word_count6 = python_word_count_data['count'][5]
        python_word_count7 = python_word_count_data['count'][6]
        python_word_count8 = python_word_count_data['count'][7]
        python_word_count9 = python_word_count_data['count'][8]
        python_word_count10 = python_word_count_data['count'][9]
    except:
        python_word1 = ""
        python_word2 = ""
        python_word3 = ""
        python_word4 = ""
        python_word5 = ""
        python_word6 = ""
        python_word7 = ""
        python_word8 = ""
        python_word9 = ""
        python_word10 = ""

        python_word_count1 = 0
        python_word_count2 = 0
        python_word_count3 = 0
        python_word_count4 = 0
        python_word_count5 = 0
        python_word_count6 = 0
        python_word_count7 = 0
        python_word_count8 = 0
        python_word_count9 = 0
        python_word_count10 = 0

    java_word_count_data = r.get('java_word_count_data')
    try:
        java_word_count_data = json.loads(java_word_count_data)
    except TypeError:
        return "waiting for data..."

    try:
        java_word1 = java_word_count_data['word'][0]
        java_word2 = java_word_count_data['word'][1]
        java_word3 = java_word_count_data['word'][2]
        java_word4 = java_word_count_data['word'][3]
        java_word5 = java_word_count_data['word'][4]
        java_word6 = java_word_count_data['word'][5]
        java_word7 = java_word_count_data['word'][6]
        java_word8 = java_word_count_data['word'][7]
        java_word9 = java_word_count_data['word'][8]
        java_word10 = java_word_count_data['word'][9]

        java_word_count1 = java_word_count_data['count'][0]
        java_word_count2 = java_word_count_data['count'][1]
        java_word_count3 = java_word_count_data['count'][2]
        java_word_count4 = java_word_count_data['count'][3]
        java_word_count5 = java_word_count_data['count'][4]
        java_word_count6 = java_word_count_data['count'][5]
        java_word_count7 = java_word_count_data['count'][6]
        java_word_count8 = java_word_count_data['count'][7]
        java_word_count9 = java_word_count_data['count'][8]
        java_word_count10 = java_word_count_data['count'][9]
    except:
        java_word1 = ""
        java_word2 = ""
        java_word3 = ""
        java_word4 = ""
        java_word5 = ""
        java_word6 = ""
        java_word7 = ""
        java_word8 = ""
        java_word9 = ""
        java_word10 = ""

        java_word_count1 = 0
        java_word_count2 = 0
        java_word_count3 = 0
        java_word_count4 = 0
        java_word_count5 = 0
        java_word_count6 = 0
        java_word_count7 = 0
        java_word_count8 = 0
        java_word_count9 = 0
        java_word_count10 = 0

    csharp_word_count_data = r.get('csharp_word_count_data')
    try:
        csharp_word_count_data = json.loads(csharp_word_count_data)
    except TypeError:
        return "waiting for data..."

    try:
        csharp_word1 = csharp_word_count_data['word'][0]
        csharp_word2 = csharp_word_count_data['word'][1]
        csharp_word3 = csharp_word_count_data['word'][2]
        csharp_word4 = csharp_word_count_data['word'][3]
        csharp_word5 = csharp_word_count_data['word'][4]
        csharp_word6 = csharp_word_count_data['word'][5]
        csharp_word7 = csharp_word_count_data['word'][6]
        csharp_word8 = csharp_word_count_data['word'][7]
        csharp_word9 = csharp_word_count_data['word'][8]
        csharp_word10 = csharp_word_count_data['word'][9]

        csharp_word_count1 = csharp_word_count_data['count'][0]
        csharp_word_count2 = csharp_word_count_data['count'][1]
        csharp_word_count3 = csharp_word_count_data['count'][2]
        csharp_word_count4 = csharp_word_count_data['count'][3]
        csharp_word_count5 = csharp_word_count_data['count'][4]
        csharp_word_count6 = csharp_word_count_data['count'][5]
        csharp_word_count7 = csharp_word_count_data['count'][6]
        csharp_word_count8 = csharp_word_count_data['count'][7]
        csharp_word_count9 = csharp_word_count_data['count'][8]
        csharp_word_count10 = csharp_word_count_data['count'][9]
    except:
        csharp_word1 = ""
        csharp_word2 = ""
        csharp_word3 = ""
        csharp_word4 = ""
        csharp_word5 = ""
        csharp_word6 = ""
        csharp_word7 = ""
        csharp_word8 = ""
        csharp_word9 = ""
        csharp_word10 = ""

        csharp_word_count1 = 0
        csharp_word_count2 = 0
        csharp_word_count3 = 0
        csharp_word_count4 = 0
        csharp_word_count5 = 0
        csharp_word_count6 = 0
        csharp_word_count7 = 0
        csharp_word_count8 = 0
        csharp_word_count9 = 0
        csharp_word_count10 = 0

    return render_template('index.html', lineChartUrl='/static/images/linechart.png', 
        barGraphUrl='/static/images/bargraph.png', pythonCount=python_counts[-1], 
        csharpCount=csharp_counts[-1], javaCount=java_counts[-1],
        pythonWord1=python_word1, pythonWordCount1=python_word_count1,
        pythonWord2=python_word2, pythonWordCount2=python_word_count2,
        pythonWord3=python_word3, pythonWordCount3=python_word_count3,
        pythonWord4=python_word4, pythonWordCount4=python_word_count4,
        pythonWord5=python_word5, pythonWordCount5=python_word_count5,
        pythonWord6=python_word6, pythonWordCount6=python_word_count6,
        pythonWord7=python_word7, pythonWordCount7=python_word_count7,
        pythonWord8=python_word8, pythonWordCount8=python_word_count8,
        pythonWord9=python_word9, pythonWordCount9=python_word_count9,
        pythonWord10=python_word10, pythonWordCount10=python_word_count10,
        javaWord1=java_word1, javaWordCount1=java_word_count1,
        javaWord2=java_word2, javaWordCount2=java_word_count2,
        javaWord3=java_word3, javaWordCount3=java_word_count3,
        javaWord4=java_word4, javaWordCount4=java_word_count4,
        javaWord5=java_word5, javaWordCount5=java_word_count5,
        javaWord6=java_word6, javaWordCount6=java_word_count6,
        javaWord7=java_word7, javaWordCount7=java_word_count7,
        javaWord8=java_word8, javaWordCount8=java_word_count8,
        javaWord9=java_word9, javaWordCount9=java_word_count9,
        javaWord10=java_word10, javaWordCount10=java_word_count10,
        csharpWord1=csharp_word1, csharpWordCount1=csharp_word_count1,
        csharpWord2=csharp_word2, csharpWordCount2=csharp_word_count2,
        csharpWord3=csharp_word3, csharpWordCount3=csharp_word_count3,
        csharpWord4=csharp_word4, csharpWordCount4=csharp_word_count4,
        csharpWord5=csharp_word5, csharpWordCount5=csharp_word_count5,
        csharpWord6=csharp_word6, csharpWordCount6=csharp_word_count6,
        csharpWord7=csharp_word7, csharpWordCount7=csharp_word_count7,
        csharpWord8=csharp_word8, csharpWordCount8=csharp_word_count8,
        csharpWord9=csharp_word9, csharpWordCount9=csharp_word_count9,
        csharpWord10=csharp_word10, csharpWordCount10=csharp_word_count10)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
