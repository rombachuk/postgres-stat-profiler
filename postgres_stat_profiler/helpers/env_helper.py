import os

def fetch_env_allow_empty(envname):

    envresult = os.getenv(envname)
    if not envresult:
       value = os.getcwd()
    else:
       value = os.path.expandvars(envresult)
    return value