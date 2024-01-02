from flask import request, make_response, jsonify

class api_auth:

  def __init__(self,request):
    self.request = request 
    self.requestkey = self._getRequestkey()
    if self.requestkey: 
      self.valid = True
    else:
      self.valid = False

  def getValid(self):
      return self.valid
  
  def getRequestkey(self):
      return self.requestkey

  def _getRequestkey(self):
    try:
      key = self.request.authorization
      if key:
         return key
      return None
    except:
      return None
      