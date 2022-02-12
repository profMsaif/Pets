"""
in this api we are going  to save photos
delete them and perform other operation that 
are not part of the class 
this file is going to separate them
providing convent way to work.
"""
import uuid
import json
import pathlib
from typing import Dict
from pets import settings
from api import exceptions


def pet_was_not_found(pet_id: str) -> Dict[str, str]:
    return {"id": pet_id, "error": "Pet with the matching ID was not found."}


def generate_photo_file_name(extension: str) -> str:
    """return random photo name"""
    return f"{uuid.uuid4()}.{extension}"


def create_photo_url(photo_file_name) -> str:
    return f"{settings.DOMAIN_URL}/{photo_file_name}"


def get_photo_path_from_url(url: str) -> str:
    # address format should be a domain like example.com
    # or ip:port
    # domain format https://address
    # url format https://address/filename.extension
    # get the file name in this format /filename.extension
    filename = url.split(settings.DOMAIN_URL)[-1]
    return f"{settings.MEDIA_ROOT}{filename}"


def save_photo(photo) -> str:
    """take photofile save and return the url of the file"""
    # the photo must have an extension in the filename
    original_file_name = photo.name.split(".")
    if len(original_file_name) != 2:
        return exceptions.FileNameWithoutExtension("bad image file name")
    extension = original_file_name[1]
    photo_file_name = generate_photo_file_name(extension)
    # write photo by chunks
    with open(f"{settings.MEDIA_ROOT}/{photo_file_name}", "wb+") as fb:
        for chunk in photo.chunks():
            fb.write(chunk)
    return create_photo_url(photo_file_name)


def delete_photo(url) -> None:
    """remove a photo by url"""
    photo = get_photo_path_from_url(url)
    try:
        pathlib.Path(photo).unlink()
    except FileNotFoundError:
        # we are deleting a file that has been already deleted
        # this happend if different pets have the same image
        # which shouldn't happen ever
        # log this
        pass


def pets_list_response(count, items):
    return {"count": count, "items": items}


def pet_delete_response(deleted, errors):
    return {"deleted": deleted, "errors": errors}


def pet_upload_photo_response(id, url):
    return {"id": id, "url": url}


def pets_to_json_stdout(objects):
    """to dict"""
    data = [
        {
            "id": str(object.id),
            "name": object.name,
            "type": object.type,
            "age": object.age,
            "photos": [photo.url for photo in object.photos.all()],
            "created_at": str(object.created_at),
        }
        for object in objects
    ]

    return json.dumps({"pets": data})
