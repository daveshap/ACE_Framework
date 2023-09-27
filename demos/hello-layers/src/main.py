import os
import time

ace_resource_name = os.getenv('ACE_RESOURCE_NAME')
print(f"Starting ACE resource: {ace_resource_name}", flush=True)
while True:
    time.sleep(1000)
