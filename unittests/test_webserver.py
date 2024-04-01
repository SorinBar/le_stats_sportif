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
        # 1
        res = requests.post("http://127.0.0.1:5000/api/state_mean", json=req_data)
        data = res.json()
        self.assertEqual("job_id" in data, True, "job_id Non existent <1>")
        self.assertEqual(data["job_id"], "job_id_1", "Wrong job_id")
        
        # 2
        res = requests.post("http://127.0.0.1:5000/api/state_mean", json=req_data)
        data = res.json()
        self.assertEqual("job_id" in data, True, "job_id Non existent <2>")
        self.assertEqual(data["job_id"], "job_id_2", "Wrong job_id")

        # 3
        res = requests.post("http://127.0.0.1:5000/api/state_mean", json=req_data)
        data = res.json()
        self.assertEqual("job_id" in data, True, "job_id Non existent <3>")
        self.assertEqual(data["job_id"], "job_id_3", "Wrong job_id")

        res = requests.get("http://127.0.0.1:5000/api/get_results/job_id_1")
        data = res.json()
        self.assertEqual("status" in data, True, "status Non existent")
        self.assertEqual(data["status"], "done", "Wrong status <1>")

        res = requests.get("http://127.0.0.1:5000/api/get_results/job_id_4")
        data = res.json()
        self.assertEqual("status" in data, True, "status Non existent")
        self.assertEqual(data["status"], "error", "Wrong status <4>")


        # # Stress test
        # for i in range(1000):
        #     res = requests.post("http://127.0.0.1:5000/api/state_mean", json=req_data)

        # self.assertEqual(True, False, "stop")
    
        
        # res = requests.get("http://127.0.0.1:5000/api/get_results/job_id_1000")
        # data = res.json()
        # self.assertEqual("status" in data, True, "status Non existent")
        # self.assertEqual(data["status"], "running", "Wrong status <100>")





if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        print()
    