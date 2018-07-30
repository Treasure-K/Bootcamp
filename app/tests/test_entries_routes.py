from app.tests.base_test_case import BaseTestCase
import json

class TestEntriesEndpoints(BaseTestCase):

	def test_add_entry(self):
		json_data = self.add_entry()["json_data"]
		self.assertEqual(json_data["message"], "Entry added successfully")


	# def test_update_entry(self):
	# 	entry = self.get_entry()
	# 	entry_data = self.create_entry()

	# 	response = self.client.post('/entries/'+entry["entry_id"], data=entry_data, headers={'token':self.token}, content_type='application/json')
	# 	json_data = json.loads(response.data.decode('utf-8'))
	# 	self.assertEqual(json_data["message"], "Updated successfully")
