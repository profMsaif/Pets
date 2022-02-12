"""
we are expecting 4 method:
POST /pets/                 # create a pet object
    - return 201
POST /pets/<uuid:id>/photo/ # create a photo object
    - upload photo of Pets object
    - body :
        - {file: uploaded_file}
    - return 201

GET /pets/                  # return a list of pets
    the method has three optional params
    has_photos: boolean  -> {true, false}, default None
        - true: return pets with photos
        - false: return pets without photos
        - none: return all pets

    limit: int -> 20
    offset: int -> 0
    - return 200

DELETE /pets/
    - delete pets with corresponding id and it's related photos
    - body:
        - {ids:[]}
    - return 200 

testing for the command get_pets
"""

import uuid
import pathlib
from io import StringIO
from typing import Any, Dict, List
from unittest import TestCase
from unittest.mock import patch

from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api import models, utils

# Create your tests here.
# app directory photo files must be in the same folder
APP_DIRECTORY = pathlib.Path(__file__).resolve().parent


class PetsAPITests(APITestCase):
    base_url = reverse("pets-list")
    cat_photo_for_test = "cat_test.jpg"
    dog_photo_for_test = "dog_test.jpg"

    def assertIsFile(self, path):
        # check if the file exist
        if not pathlib.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def setUp(self) -> None:
        # create pets object
        models.Pets.objects.create(**{"name": "girl", "age": 1, "type": "cat"})

    def test_create_pet(self):
        """
        Ensure we can create pet object using post method
        """
        body_to_post = {"name": "boy", "age": 7, "type": "dog"}

        successfull_response = {
            "id": "433a203f-5480-442b-b599-01060d988d87",
            "name": "boy",
            "age": 7,
            "type": "dog",
            "photos": [],
            "created_at": "2021-05-18T19:10:17",
        }

        response = self.client.post(self.base_url, body_to_post, format="json")
        response_data: Dict[str, Any] = response.json()
        # the status code must be 201 which should be enough
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # the pet still has no photo
        self.assertEqual(len(response_data["photos"]), 0)
        # compare the key
        self.assertSetEqual(set(response_data.keys()), set(successfull_response.keys()))
        # now we must have two objects , one was created during setUp and this one
        self.assertEqual(models.Pets.objects.count(), 2)

    def test_upload_pet_photo(self):
        """
        Ensure we can upload photos for specific pet
        """
        # get the object that was created during the setup
        # we need it's id
        pet: models.Pets = models.Pets.objects.get()
        # upload the cat photo
        with open(APP_DIRECTORY / f"{self.cat_photo_for_test}", "rb") as fb:
            response = self.client.post(
                f"{self.base_url}{pet.id}/photo/", data={"file": fb}
            )
        # status code must be 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        # now check if the pet object has a photo
        self.assertEqual(len(pet.photos.all()), 1)
        self.assertIsFile(utils.get_photo_path_from_url(response_data["url"]))
        # delete the photo as the test database is going to be dropped
        # at the end of the test
        utils.delete_photo(response_data["url"])

    def test_get_pets_list(self):
        input_data = [
            {"name": "boy", "age": 3, "type": "cat"},
            {"name": "girl", "age": 1, "type": "cat"},
            {"name": "boy", "age": 10, "type": "dog"},
            {"name": "girl", "age": 5, "type": "dog"},
            {"name": "boy", "age": 5, "type": "dog"},
        ]

        # create all pets in the input data
        responses = [
            self.client.post(self.base_url, data, format="json").json()
            for data in input_data
        ]
        # add  photos for the firs two cats
        for response in responses[:2]:
            with open(APP_DIRECTORY / f"{self.cat_photo_for_test}", "rb") as fb:
                self.client.post(
                    f"{self.base_url}{response['id']}/photo/", data={"file": fb}
                )
        # add two photos for the same dog (dog number 4)
        with open(APP_DIRECTORY / f"{self.dog_photo_for_test}", "rb") as fb:
            self.client.post(
                f"{self.base_url}{responses[4]['id']}/photo/", data={"file": fb}
            )

        # now we test getting these object via GET /pets/
        # pets with photos
        pets_with_photos = self.client.get(self.base_url, {"has_photo": "true"}).json()
        self.assertEqual(pets_with_photos["count"], 3)
        self.assertTrue(pets_with_photos["items"][0]["photos"])
        del pets_with_photos
        pets_no_photos = self.client.get(self.base_url, {"has_photo": "false"}).json()
        self.assertEqual(pets_no_photos["count"], 3)
        self.assertFalse(pets_no_photos["items"][0]["photos"])
        del pets_no_photos
        pets_all = self.client.get(self.base_url).json()
        self.assertEqual(pets_all["count"], 6)
        del pets_all
        pets_only_two_objects = self.client.get(self.base_url, {"limit": 2}).json()
        self.assertEqual(pets_only_two_objects["count"], 2)
        del pets_only_two_objects
        self.client.delete(
            self.base_url, {"ids": [str(response["id"]) for response in responses]}
        )

    def test_delete_pets(self):
        # add pets that doesn't exist
        ids = [str(uuid.uuid4())]
        # we trying to delete 7 items
        response = self.client.delete(self.base_url, {"ids": ids})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response["deleted"], 0)
        self.assertEqual(len(response["errors"]), 1)


class CommandTestCase(TestCase):
    def setUp(self) -> None:
        input_data = [
            {"name": "boy", "age": 3, "type": "cat"},
            {"name": "girl", "age": 1, "type": "cat"},
            {"name": "boy", "age": 10, "type": "dog"},
            {"name": "girl", "age": 5, "type": "dog"},
            {"name": "boy", "age": 5, "type": "dog"},
        ]
        # create 5 pets
        instances: List[models.Pets] = [
            models.Pets.objects.create(**data) for data in input_data
        ]
        # add photo for the first cat
        url = "https://address/filename.extension"
        photo: List[models.PetsPhoto] = models.PetsPhoto.objects.create(
            pet=instances[0], url=url
        )
        instances[0].photos.add(photo)

    def test_get_pets_command(self):
        import json

        inputs_with_correct_response = {True: 1, False: 4, None: 5}
        for has_photo, count in inputs_with_correct_response.items():
            with patch("sys.stdout", new=StringIO()) as fake_out:
                call_command("get_pets", has_photo=has_photo)
                response = json.loads(fake_out.getvalue())
                self.assertEqual(len(response["pets"]), count)
