from models.connection import bucket
import os

# These functions should support multi-threadding


def save_file(path: str, fileName: str) -> int:
    try:
        fullPath = "{}/{}".format(path, fileName)
        blob = bucket.blob(fullPath)
        blob.download_to_filename("temp/{}".format(fileName))
        return 1
    except Exception as e:
        print(e)
        return 0


def delete_local_file(path: str) -> bool:
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
