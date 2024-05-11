import os
from celery import shared_task
from .utils import handle_imageProcessing
from django.conf import settings
# from .models import Asset, Result


# @shared_task
# def task_handler(asset_id):
#     asset = Asset.objects.get(id=asset_id)

#     PROCESS_TYPES = ['otsu', 'edge', 'color', 'separate']

#     print('process types:', PROCESS_TYPES)

#     raw_image_path = asset.asset_image.path
#     print("raw_image_path", raw_image_path)

#     media_root = str(settings.MEDIA_ROOT)  # Convert WindowsPath to string
#     inspection_results_path = os.path.join(media_root, "results")

#     if not os.path.exists(inspection_results_path):
#         os.mkdir(inspection_results_path)

#     processed_image_path = raw_image_path.replace(
#         "assets", "results")
#     print("processed_image_path", processed_image_path)

#     for process_type in PROCESS_TYPES:
#         print('current process type:', process_type)
#         # processed_path (file name) will also append the process type (just before the extension)
#         path, ext = os.path.splitext(processed_image_path)
#         temp = path + "_" + process_type + ext

#         print("processed_image_path", temp)

#         # relative path (from media root)
#         relative_path = temp.replace(media_root, "")

#         # call the process_image function
#         process_image(raw_image_path, temp,
#                       process_type)

#         inspection_result = Result(
#             result_image=relative_path,
#             asset=asset,
#         )

#         inspection_result.save()

#     # asset.status = "processed"
#     # asset.save()

#     return True


# def process_image(raw_image_path, processed_image_path, process_type):
#     ret = handle_imageProcessing(
#         raw_image_path, processed_image_path, process_type)

#     if ret:
#         print("successfully processed!")
#     else:
#         print("process failed!")

#     return ret
