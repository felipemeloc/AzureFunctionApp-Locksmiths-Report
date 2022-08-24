# Code


path = 'api\FunctionReportLocksmiths\load_env.py'
```
import os

env_vars = {
'MAIN_PATH' : '',

# Telegram API
'API_KEY' : "",
'SERVER' : '',

# Azure Blob
'BLOB_CONN_STR' : "",
'CONTAINER' : "",
'REPORT_IMAGE' : '',

# Database
'DATABASE' : '',
'USER_NAME' : '',
'DATABASE_PASSWORD' : '',
'TEST_GROUP' : '',
'LOCKSMITHS_GROUP' : ''

}

def load_env():
    for key, val in env_vars.items():
        os.environ[key] : val

load_env()
```