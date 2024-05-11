# concrete_crack_classification_image, concrete_crack_classification_video, crack_detection_basic_image, crack_detection_basic_video, crack_detection_yolo_v8_image, crack_detection_yolo_v8_video
import os
import time
import cv2
from celery import shared_task
from django.core.files import File
from api.action.ai import crack_detection_basic
from api.project.asset.models import AssetResult

@shared_task
def concrete_crack_classification_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
    image = cv2.imread(asset_result.asset.file.path)
    




  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def concrete_crack_classification_video(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def crack_detection_basic_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)

    # read the image
    image = cv2.imread(asset_result.asset.file.path)
    result, ratio = crack_detection_basic(image)

    image_path = asset_result.asset.file.path
    image_name = asset_result.asset.file.name

    temp_image_path = image_path.replace('assets', 'temp')
    cv2.imwrite(temp_image_path, result)
    result_image_name = image_name.replace('assets/', '')
    # attact time to the result image name
    result_image_name = f'{str(int(time.time()))}_{result_image_name}'
    asset_result.result.save(result_image_name, File(open(temp_image_path, 'rb')))
    os.remove(temp_image_path)

    """
      @Yousuf24100286
      Save the metadata to the database
    """

    asset_result.status = 'completed'
    asset_result.save()
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def crack_detection_basic_video(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def crack_detection_yolo_v8_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
    image = cv2.imread(asset_result.asset.file.path)

    
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def crack_detection_yolo_v8_video(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return

  