import json
from typing import List
from django.http import HttpResponseBadRequest, HttpRequest
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api import models, serializers, auth, utils


class PetsViewSet(viewsets.ModelViewSet):
    authentication_classes = [auth.ApiKeyAuthentication]
    # no ordering is required
    queryset = models.Pets.objects.all()
    serializer_class = serializers.PetsSerializer

    def list(self, request: HttpRequest, *args, **kwargs):
        # return list of pets
        try:
            # parser offset and limit params set default values
            offset = int(request.query_params.get("offset", 0))
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            return HttpResponseBadRequest(f"bad paginate value")
        # parser has_photo params
        has_photo = request.query_params.get("has_photo","null")
        if has_photo not in ("true","false", "null"):
            return HttpResponseBadRequest(f"bad value: has_photo must be boolean") 
            
        has_photo = json.loads(has_photo)
        match has_photo:
            case True:
                #  get all pets exclude  the one without photos
                queryset = models.Pets.objects\
                    .exclude(photos=None).all().order_by("-created_at")
            case False:
                # get all pets without photos
                queryset = models.Pets.objects.\
                    filter(photos=None).all().order_by("-created_at")
            case _:
                # get all pets
                queryset = models.Pets.objects.all().order_by("-created_at")
        page = self.paginate_queryset(queryset[offset:limit])
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response(utils.pets_list_response(len(serializer.data), serializer.data))
        return Response(utils.pets_list_response(0, []), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            # validate the body
            serializer = serializers.DeletePetsSerializer(data=request.data)
            if not serializer.is_valid():
                return HttpResponseBadRequest("bad request")
            # get the ids
            ids = serializer.validated_data["ids"]
            instances: List[models.Pets] = models.Pets.objects.filter(id__in=ids).all()
            # deleting all related photos
            for instance in instances:
                photos = instance.photos.all()
                for photo in photos:
                    utils.delete_photo(photo.url)
            
            ids_not_found = list(
                set(ids) - set(map(lambda instance: str(instance.id), instances))
            )
            # delete all instances from the datebase
            instances.delete()
            # set error response for the pets that were not found 
            errors = [utils.pet_was_not_found(id) for id in ids_not_found]
            return Response(data=utils.pet_delete_response(deleted=len(instances), errors=errors),
            status=status.HTTP_200_OK)


    @action(
        methods=["POST"],
        detail=True,
        parser_classes=[
            MultiPartParser,
        ],
        serializer_class=serializers.PetsPhotoSerializer,
    )
    def photo(self, request: HttpRequest, pk=None):
        # the photo endpoint
        #responeding to the call on this url
        #METHOD /pets/<uuid:pk>/photo/
        if request.method == "POST":
            # createing new photo object
            # 1. get theparamters uuid and photo file
            uuid = request.parser_context.get("kwargs").get("pk")
            image_file = request.FILES.get("file", None)
            if image_file is None:
                return HttpResponseBadRequest("missing the image file")
            try:
                pet: models.Pets = models.Pets.objects.get(id=uuid)
            except models.Pets.DoesNotExist:
                return HttpResponseBadRequest("Pet with the matching ID was not found.")
            url = utils.save_photo(request.FILES["file"])
            obj: models.PetsPhoto = models.PetsPhoto.objects.create(pet=pet, url=url)
            pet.photos.add(obj)
            return Response({"id": obj.id, "url": obj.url})

