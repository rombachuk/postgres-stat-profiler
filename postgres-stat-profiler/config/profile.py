from flask import request

def find_requestuser(request):
 try:
  auth = request.authorization
  if auth:
   return auth.username
  else:
   cookieauth = request.cookies.get("AuthSession")
   if cookieauth is not None:
    cookieauthparts = str(base64.urlsafe_b64decode(str(cookieauth))).split(':')
    if len(cookieauthparts) > 1:
     return cookieauthparts[0]
  return None
 except Exception as e:
  return None