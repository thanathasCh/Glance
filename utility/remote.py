import requests
import cv2
from common import api_path
from utility import log
from cv import preprocess


def _validate_status(response):
    if response.status_code == 200:
        return True
    else:
        log.print_error(f'Error Code: {response.status_code}')
        return False


def check_process_queue():
    response = requests.get(api_path.list_unprocessed_videos)

    if not _validate_status(response):
        return None

    # TODO convert to class
    return response

def get_video(url):
    video = []

    vcap = cv2.VideoCapture(url)

    while(1):
        ret, frame = vcap.read()
        if frame is None:
            break

        cv2.imshow('frame', frame)
        video.append(frame)
    
    vcap.release()
    
    return video


def upload_images(image_infos):
    # TODO - upload images to the database with table information
    pass


def get_image(path=''):
    response = requests.get(api_path.TEST_BLOB)

    if not _validate_status(response):
        return None
    
    return preprocess.bytes_to_img(response.content)


def get_images(paths):
    return None