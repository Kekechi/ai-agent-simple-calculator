

tools = [
  {
    "type":"function",
    "function":{
      "name":"add",
      "description":"""Perform addition of two float numbers. 
      Can perform subtraction through addition of negative numbers. 
      Return the sum in float""",
      "parameters":{
        "type":"object",
        "properties":{
          "a":{
            "type":"number",
            "description":"""The first number of the addition"""
          },
          "b":{
            "type":"number",
            "description":"""The second number of the addition"""
          }
        },
        "required":["a","b"],
        "additionalProperties":False
      },
    "strict":True
    },
  },
  {
    "type":"function",
    "function":{
      "name":"multiply",
      "description":""""Perform multiplication of two float numbers. 
      Can perform division using reciptrical of a number. 
      Return the product in float""",
      "parameters":{
        "type":"object",
        "properties":{
          "a":{
            "type":"number",
            "description":"""The first number of the multiplication"""
          },
          "b":{
            "type":"number",
            "description":"""The second number of the multiplication"""
          }
        },
        "required":["a","b"],
        "additionalProperties":False
      },
      "strict":True
    },
  }
]

def add(a,b):
  return a + b

def multiply(a,b):
  return a * b