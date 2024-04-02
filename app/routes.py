from flask import request, jsonify
from app import webserver
from app.services import *

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    webserver.logger.info("Echo")
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_results(job_id):
    job_index = int(job_id[7:]) - 1
    webserver.logger.info("get_results: " + str(job_index))

    return jsonify(get_results_service(job_index, webserver))

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify(get_jobs_service(webserver))

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    webserver.logger.info("get_num_jobs")

    return jsonify(get_num_jobs_service(webserver))

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    data = request.json
    webserver.logger.info("states_mean_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400

    job_id = webserver.tasks_runner.submit(
        states_mean_service,
        webserver,
        data["question"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    webserver.logger.info("state_mean_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400
    if "state" not in data:
        return jsonify({"error": "Missing state"}), 400

    job_id = webserver.tasks_runner.submit(
        state_mean_service,
        webserver,
        data["question"],
        data["state"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    webserver.logger.info("best5_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400

    job_id = webserver.tasks_runner.submit(
        best5_service,
        webserver,
        data["question"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json
    webserver.logger.info("worst5_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400

    job_id = webserver.tasks_runner.submit(
        worst5_service,
        webserver,
        data["question"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json
    webserver.logger.info("global_mean_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400

    job_id = webserver.tasks_runner.submit(
        global_mean_service,
        webserver,
        data["question"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.json
    webserver.logger.info("diff_from_mean_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400

    job_id = webserver.tasks_runner.submit(
        diff_from_mean_service,
        webserver,
        data["question"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    webserver.logger.info("state_diff_from_mean_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400
    if "state" not in data:
        return jsonify({"error": "Missing state"}), 400

    job_id = webserver.tasks_runner.submit(
        state_diff_from_mean_service,
        webserver,
        data["question"],
        data["state"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json
    webserver.logger.info("mean_by_category_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400

    job_id = webserver.tasks_runner.submit(
        mean_by_category_service,
        webserver,
        data["question"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.json
    webserver.logger.info("state_mean_by_category_request: " + str(data))

    if "question" not in data:
        return jsonify({"error": "Missing question"}), 400
    if "state" not in data:
        return jsonify({"error": "Missing state"}), 400

    job_id = webserver.tasks_runner.submit(
        state_mean_by_category_service,
        webserver,
        data["question"],
        data["state"])

    return jsonify({"job_id": "job_id_" + str(job_id)})

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    webserver.logger.info("graceful_shutdown")
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "shutting down"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
