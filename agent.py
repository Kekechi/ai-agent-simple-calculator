from dotenv import load_dotenv
from openai import OpenAI
from tools import tools,add,multiply
import os, json

load_dotenv('.env')
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')

MAX_ITERATION = 5

class Agent:
  def __init__(self):
    self.client = OpenAI(
      api_key=API_KEY,
      base_url=API_URL
    )

    self.messages = []

    self.messages.append({
      "role":"system",
      "content":"""You are a helpful AI assistant with access to simple calculation tools.
      Follow these rules:
      1. When asked to calculate math equations, always use the available tools first
      2. If a tool returns an error, explain the error to the user clearly"""
    })
  

  def process_query(self,user_input):
    self.messages.append({
      "role":"user",
      "content":user_input
    })

    completion = self.client.chat.completions.create(
      model="gpt-5-nano",
      messages=self.messages,
      tools=tools,
      tool_choice='auto'
    )

    response_message = completion.choices[0].message
    print(response_message)
    return response_message

    # try:
    #   for _ in range(MAX_ITERATION):