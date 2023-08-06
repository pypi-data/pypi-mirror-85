# -*- coding: utf-8 -*-
"""Upload demo."""
from rayvision_api import RayvisionAPI
from rayvision_sync.upload import RayvisionUpload
from rayvision_sync.utils import cutting_upload

api = RayvisionAPI(access_id="xxxxx",
                   access_key="xxxxx",
                   domain="task.renderbus.com",
                   platform="2")

CONFIG_PATH = [
    r"C:\workspace\work\tips.json",
    r"C:\workspace\work\task.json",
    r"C:\workspace\work\asset.json",
    r"C:\workspace\work\upload.json",
]
UPLOAD = RayvisionUpload(api)

# UPLOAD.upload_asset(r"D:\test\test_upload\1586250829\upload.json")
# UPLOAD.upload_config("5165465", CONFIG_PATH)


# cut upload according to the number of resources
upload_pool = cutting_upload(r"D:\test\test_upload\1586250829\upload.json", max_resources_number=800)
# print(upload_pool)


# Multi-thread upload
UPLOAD.multi_thread_upload(upload_pool, thread_num=20)

# Thread pool upload
# UPLOAD.thread_pool_upload(upload_pool, pool_size=20)
#
