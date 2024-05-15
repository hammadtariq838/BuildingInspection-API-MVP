# concrete_crack_classification_image, concrete_crack_classification_video, crack_detection_basic_image, crack_detection_basic_video, crack_detection_yolo_v8_image, crack_detection_yolo_v8_video
import os
import time
import cv2
from celery import shared_task
from django.core.files import File
from api.action.ai import crack_detection_basic, CrackDetectionYOLOv8, ConcreteCrackClassification, before_after
from api.project.asset.models import AssetResult, ChildAsset

def save_image_results(asset_result_id, result):
  asset_result = AssetResult.objects.get(id=asset_result_id)

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



@shared_task
def concrete_crack_classification_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
    
    image = cv2.imread(asset_result.asset.file.path)
    concrete_model = ConcreteCrackClassification()
    result, meta = concrete_model.predict(image)
    
    save_image_results(asset_result_id, result)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def concrete_crack_classification_video(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)

    video = cv2.VideoCapture(asset_result.asset.file.path)

    # get the video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # get video fourcc

    # number of frames in the video
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # jump count for the video floor (num_frames ^ 0.5)
    jump_count = int(num_frames ** 0.3)



    # extract frames from video and run crack detection on each frame and create a new video
    # with the crack detection results
    model = ConcreteCrackClassification()
    frames = []
    i = 0
    while True:
      ret, frame = video.read()
      if not ret:
        break
      i += 1
      if i % jump_count != 0:
        continue

      print(f'Concrete Crack Classification Video : Processing Frame {i}/{num_frames}')
      result, meta = model.predict(frame)
      frames.append(result)

    video.release()

    # create a new video with the crack detection results
    video_path = asset_result.asset.file.path
    video_name = asset_result.asset.file.name

    temp_video_path = video_path.replace('assets', 'temp')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

    for frame in frames:
      out.write(frame)

    out.release()

    result_video_name = video_name.replace('assets/', '')
    # attact time to the result video name
    result_video_name = f'{str(int(time.time()))}_{result_video_name}'
    asset_result.result.save(result_video_name, File(open(temp_video_path, 'rb')))

    os.remove(temp_video_path)

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
def crack_detection_basic_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)

    image = cv2.imread(asset_result.asset.file.path)
    result, ratio = crack_detection_basic(image)
    
    save_image_results(asset_result_id, result)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def crack_detection_basic_video(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
    video = cv2.VideoCapture(asset_result.asset.file.path)

    # get the video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    



    # extract frames from video and run crack detection on each frame and create a new video
    # with the crack detection results
    frames = []
    while True:
      ret, frame = video.read()
      if not ret:
        break
      result, ratio = crack_detection_basic(frame)
      frames.append(result)

    video.release()
    # cv2.destroyAllWindows()

    # create a new video with the crack detection results
    video_path = asset_result.asset.file.path
    video_name = asset_result.asset.file.name
    temp_video_path = video_path.replace('assets', 'temp')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

    for frame in frames:
      out.write(frame)

    out.release()

    result_video_name = video_name.replace('assets/', '')
    # attact time to the result video name
    result_video_name = f'{str(int(time.time()))}_{result_video_name}'
    asset_result.result.save(result_video_name, File(open(temp_video_path, 'rb')))
    os.remove(temp_video_path)
    
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
def crack_detection_yolo_v8_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
    
    image = cv2.imread(asset_result.asset.file.path)
    crack_yolo_v8 = CrackDetectionYOLOv8()
    result, meta = crack_yolo_v8.predict_image(image)
    
    save_image_results(asset_result_id, result)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return
  
@shared_task
def crack_detection_yolo_v8_video(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)

    video = cv2.VideoCapture(asset_result.asset.file.path)

    # get the video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # number of frames in the video
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # jump count for the video floor (num_frames ^ 0.5)
    jump_count = int(num_frames ** 0.3)
    # extract frames from video and run crack detection on each frame and create a new video
    # with the crack detection results
    model = CrackDetectionYOLOv8()
    frames = []
    i = 0
    while True:
      ret, frame = video.read()
      if not ret:
        break
      i += 1
      if i % jump_count != 0:
        continue
      print(f'Crack Detection YOLOv8 Video : Processing Frame {i}/{num_frames}')
      result, meta = model.predict_image(frame)
      frames.append(result)

    video.release()

    # create a new video with the crack detection results
    video_path = asset_result.asset.file.path
    video_name = asset_result.asset.file.name
    temp_video_path = video_path.replace('assets', 'temp')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

    for frame in frames:
      out.write(frame)

    out.release()

    result_video_name = video_name.replace('assets/', '')
    # attact time to the result video name
    result_video_name = f'{str(int(time.time()))}_{result_video_name}'
    asset_result.result.save(result_video_name, File(open(temp_video_path, 'rb')))
    os.remove(temp_video_path)
    
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
def before_after_image(asset_result_id):
  try:
    asset_result = AssetResult.objects.get(id=asset_result_id)
    # get asset
    asset = asset_result.asset
    # get child assets
    child_assets = ChildAsset.objects.filter(parent=asset)
    child_assets = list(child_assets)

    if len(child_assets) != 1:
      raise Exception('Only 1 child asset is allowed for before_after_image task')

    before_image = cv2.imread(asset.file.path)
    after_image = cv2.imread(child_assets[0].file.path)

    before_image, after_image = before_after(before_image, after_image)

    save_image_results(asset_result_id, after_image)
  except Exception as e:
    asset_result.error = str(e)
    asset_result.status = 'failed'
    asset_result.save()
    return