#!/usr/bin/env python

MONGO_CONN_STR = "mongodb+srv://..."

ADMIN_COLLECTION = "info" # collection containing credentials and function parameters

ADMIN_DATABASES = ["admin", "local"] # databases to ignore when fetching customers

_WEBHOOK = ""

TIMEZONE = "America/Sao_Paulo" # timezone for restarting and acquiring load_time_block 

OS = 'UBUNTU'
# OS = 'MAC'

SAVE_LOGS = False

LOG_DIR = "logs/"

MAX_LOG_SIZE = 100000000 # 100Mb

MAX_LOG_BACKUPS = 5

# AWS CONFIG
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY_ID = ""
AWS_REGION = "us-east-2"
LOGGING_BUCKET = "raptor-logs"
