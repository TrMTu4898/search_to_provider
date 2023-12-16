import google.generativeai as genai
from fastapi.encoders import jsonable_encoder


class GoogleGenerative:
	def __init__(self):
		self.api_key = "AIzaSyA6N9hV4IMKHr7YUGSDjDW2Chw9sK0eDzo"
		genai.configure(api_key=self.api_key)
		self.model = genai.GenerativeModel('gemini-pro')

	def generative(self, input_mes):
		try:
			response = self.model.generate_content(input_mes)
			return response.text
		except Exception as e:
			return {"status_code": 500, "detail": str(e)}