# concrete_crack_classification_image, concrete_crack_classification_video, crack_detection_basic_image, crack_detection_basic_video, crack_detection_yolo_v8_image, crack_detection_yolo_v8_video
from celery import shared_task
from api.project.asset.models import AssetResult

@shared_task
def concrete_crack_classification_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
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

  