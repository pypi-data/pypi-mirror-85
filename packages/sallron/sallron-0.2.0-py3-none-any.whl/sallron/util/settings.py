#!/usr/bin/env python

# GENERAL CONFIG

INTERFACE_NAME = 'interface_name'

TIMEZONE = "America/Sao_Paulo" # timezone for restarting and acquiring load_time_block 

OS = 'UBUNTU'
# OS = 'MAC'

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/123..."

# LOGGER CONFIG

SAVE_LOGS = False

LOG_DIR = "logs/"

LOG_LEVEL='INFO'

MAX_LOG_SIZE = 100000000 # 100Mb

MAX_LOG_BACKUPS = 5

# MONGO CONFIG

MONGO_CONN_STR = "mongodb+srv://..."

ADMIN_COLLECTION = "info" # collection containing credentials and function parameters

ADMIN_DATABASES = ["admin", "local", "temporary-tokens"] # databases to ignore when fetching customers

# AWS CONFIG

AWS_ACCESS_KEY_ID = "ABC..."

AWS_SECRET_ACCESS_KEY_ID = "cD3..."

AWS_REGION = "us-east-2"

LOGGING_BUCKET = "monitor.logging"

# Max Steel Config

MAX_STEEL_URL = "https://5423csd3j.exe..."