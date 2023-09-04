
import hashlib

def calculate_file_hash(file):
    hasher = hashlib.md5()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()