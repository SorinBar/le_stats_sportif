import json
from time import sleep
import pandas as pd

### Helpers ###
def save_json(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file)

def read_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def states_mean_array(webserver, question):
    """
    Returns the mean answer of the question for every state
    in ascending order
    """

    data = webserver.data_ingestor.data
    data_values = data[
        (data['Question'] == question) &
        (data['YearStart'] >= 2011) &
        (data['YearEnd'] <= 2022)][['LocationDesc', 'Data_Value']]

    webserver.logger.info("states_mean_array - " + question + " - count: " + str(len(data_values)))

    # Keep the sum of the values and count for each location
    loc_values = {}
    for _, row in data_values.iterrows():
        location = row['LocationDesc']
        value = row['Data_Value']
        if location not in loc_values:
            loc_values[location] = {
                "total_value": value,
                "count": 1
            }
        else:
            loc_values[location]["total_value"] += value
            loc_values[location]["count"] += 1

    # Generate result
    result_array = []
    for location, value in loc_values.items():
        result_array.append((location, value["total_value"] / value["count"]))
    
    result_array.sort(key=lambda x: x[1])

    return result_array

### Services ###
def get_results_service(index, webserver):
    status = webserver.tasks_runner.get_job(index)

    if status == "error":
        return {
            "status": status,
            "reason": "Invalid job_id"
        }
    elif status == "running":
        return {"status": status}
    else:
        return {
            "status": status,
            "data": read_json("jobs/job_id_" + str(index + 1))
        }

def get_jobs_service(webserver):
    jobs_done = webserver.tasks_runner.get_jobs() 

    result = {
        "status": "done",
        "data": []
    }

    for index, job_done in enumerate(jobs_done):
        result["data"].append({
            f"job_id_{index + 1}": "done" if job_done else "running"
        })

    return result

def get_num_jobs_service(webserver):
    jobs_done = webserver.tasks_runner.get_jobs() 

    running_jobs = 0

    for job_done in jobs_done:
        if not job_done:
            running_jobs += 1

    return {
        "running_jobs": running_jobs
    }

def state_mean_service(job_id, webserver, question, state):
    data = webserver.data_ingestor.data
    mean = data[
        (data['Question'] == question) &
        (data['LocationDesc'] == state) &
        (data['YearStart'] >= 2011) &
        (data['YearEnd'] <= 2022)]['Data_Value'].mean()
    
    result = {state: mean}

    webserver.logger.info("state_mean_service:")
    webserver.logger.info(question)
    webserver.logger.info(state)
    webserver.logger.info(result)

    save_json('jobs/job_id_' + str(job_id), result)

def states_mean_service(job_id, webserver, question):
    result_array = states_mean_array(webserver, question)
    result = {}
    for location, mean in result_array:
        result[location] = mean

    webserver.logger.info("states_mean_service:")
    webserver.logger.info(question)
    webserver.logger.info(result)

    save_json('jobs/job_id_' + str(job_id), result)

def best5_service(job_id, webserver, question):
    result_array = states_mean_array(webserver, question)
    result = {}

    if question in webserver.data_ingestor.questions_best_is_min:
        for i in range(5):
            location, mean = result_array[i]
            result[location] = mean
    else:
        length = len(result)
        for i in range(5):
            location, mean = result_array[length - i - 1]
            result[location] = mean
            

    webserver.logger.info("best5_service:")
    webserver.logger.info(question)
    webserver.logger.info(result)

    save_json('jobs/job_id_' + str(job_id), result)

def worst5_service(job_id, webserver, question):
    result_array = states_mean_array(webserver, question)
    result = {}

    if question in webserver.data_ingestor.questions_best_is_max:
        for i in range(5):
            location, mean = result_array[i]
            result[location] = mean
    else:
        length = len(result)
        for i in range(5):
            location, mean = result_array[length - i - 1]
            result[location] = mean
            

    webserver.logger.info("worst5_service:")
    webserver.logger.info(question)
    webserver.logger.info(result)

    save_json('jobs/job_id_' + str(job_id), result)

def global_mean_service(job_id, webserver, question):
    data = webserver.data_ingestor.data
    mean = data[
        (data['Question'] == question) &
        (data['YearStart'] >= 2011) &
        (data['YearEnd'] <= 2022)]['Data_Value'].mean()
    
    result = {"global_mean": mean}

    webserver.logger.info("global_mean:")
    webserver.logger.info(question)
    webserver.logger.info(result)

    save_json('jobs/job_id_' + str(job_id), result)

def diff_from_mean_service(job_id, webserver, question):
    result_array = states_mean_array(webserver, question)
    result = {}
    data = webserver.data_ingestor.data
    global_mean = data[
        (data['Question'] == question) &
        (data['YearStart'] >= 2011) &
        (data['YearEnd'] <= 2022)]['Data_Value'].mean()

    for location, mean in result_array:
        result[location] = global_mean - mean    

    webserver.logger.info("diff_from_mean_service:")
    webserver.logger.info(question)
    webserver.logger.info(result)

    save_json('jobs/job_id_' + str(job_id), result)