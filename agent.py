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
  
  def execute_tool(self,tool_call):
    try:
      function_name = tool_call.function.name
      function_args = json.loads(tool_call.function.arguments)

      if function_name == "add":
        res = add(function_args["a"],function_args["b"])
      elif function_name == "multiply":
        res = multiply(function_args["a"],function_args["b"])
      else:
        res = json.dumps({
                    "error": f"Unknown tool: {function_name}"
                })
      return res
    except json.JSONDecodeError:
      return json.dumps({
          "error": "Failed to parse tool arguments"
      })
    except Exception as e:
      return json.dumps({
        "error": f"Tool execution failed: {str(e)}"
      })
              

  def process_query(self,user_input):
    self.messages.append({
      "role":"user",
      "content":user_input
    })

    try:
      for _ in range(MAX_ITERATION):
        completion = self.client.chat.completions.create(
          model="gpt-5-nano",
          messages=self.messages,
          tools=tools,
          tool_choice='auto'
        )

        response_message = completion.choices[0].message
        
        self.messages.append(response_message)

        if not response_message.tool_calls:
          return response_message.content
        
        for tool_call in response_message.tool_calls:
          try:
            print(f"Tool call: {tool_call}")
            result = self.execute_tool(tool_call)
            print("Execution success")
          except Exception as e:
            print("Execution failed")
            result = json.dumps({"error":f'Tool execution failed: {str(e)}'})
          
          print(f'Tool Result: {result}')

          self.messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":str(result)
          })
          print(f"Message: {self.messages}")
        
      max_iter_message = {
        "role":"assistant",
        "content": f'Maximum number of tool call. Last response: {response_message.content}'
      }
      self.messages.append(max_iter_message)
      return max_iter_message["content"]

    except Exception as e:
      error_message = f"Error processing query: {str(e)}"
      self.messages.append({
          "role": "assistant",
          "content": error_message
      })
      return error_message
  
  def get_conversation_history(self):
    return self.messages