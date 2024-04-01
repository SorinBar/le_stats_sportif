import json
import pandas as pd

def save_json(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file)

def read_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def state_mean_service(job_id, webserver, question, state):
    data = webserver.data_ingestor.data
    mean = data[
        (data['Question'] == question) &
        (data['LocationDesc'] == state) &
        (data['YearStart'] >= 2011) &
        (data['YearEnd'] <= 2022)]['Data_Value'].mean()
    
    result = {state: mean}

    save_json('jobs/job_id_' + str(job_id), result)
    
    # return read_json('jobs/job_id_' + str(job_id))

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
