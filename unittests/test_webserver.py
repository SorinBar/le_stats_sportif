from time import sleep
import requests
import json
import unittest


class TestWebserver(unittest.TestCase):
    def setUp(self):
        pass

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_get_job_status(self):
        req_data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "state": "Maine"
        }

        res = requests.post("http://127.0.0.1:5000/api/state_mean", json=req_data)
        data = res.json()
        self.assertEqual("job_id" in data, True, "job_id Non existent <1>")
        
        id = int(data["job_id"][7:])

        sleep(1)

        res = requests.get("http://127.0.0.1:5000/api/get_results/job_id_" + str(id))
        data = res.json()
        self.assertEqual("status" in data, True, "status Non existent")
        self.assertEqual(data["status"], "done", "Wrong status")

        res = requests.get("http://127.0.0.1:5000/api/get_results/job_id_" + str(id + 1))
        data = res.json()
        self.assertEqual("status" in data, True, "status Non existent")
        self.assertEqual(data["status"], "error", "Wrong status")
    
    def test_graceful_shutdown(self):
        req_data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "state": "Maine"
        }

        res = requests.get("http://127.0.0.1:5000/api/graceful_shutdown", json={})
        data = res.json()
        self.assertEqual(data, {"status": "shutting down"}, "Wrong response")
        
        res = requests.post("http://127.0.0.1:5000/api/state_mean", json=req_data)
        data = res.json()
        self.assertEqual(data["job_id"], "job_id_-1", "job_id Non existent <1>")
        
        res = requests.get("http://127.0.0.1:5000/api/get_results/job_id_1")
        data = res.json()
        self.assertEqual("status" in data, True, "status Non existent")
        self.assertEqual(data["status"], "done", "Wrong status")

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        print()
    