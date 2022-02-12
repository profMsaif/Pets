import json
from django.core.management.base import BaseCommand
from api import models, utils


def get_pets(has_photo=None):
    if has_photo:
        instances = models.Pets.objects.exclude(photos=None).all()
    elif has_photo is False:
        instances = models.Pets.objects.filter(photos=None).all()
    else:
        instances = models.Pets.objects.all()

    return utils.pets_to_json_stdout(instances)


class Command(BaseCommand):
    help = "retrieve pets"

    def add_arguments(self, parser):
        parser.add_argument(
            "--has_photo",
            help="if None return all if true return pets with photos",
        )

    def handle(self, *args, **options) -> None:
        has_photo = options.get("has_photo")
        if isinstance(has_photo, str):
            if has_photo not in ("true", "false"):
                self.stderr.write(
                    "--has_photo is optional and it except only boolean true/false"
                )
                return
            has_photo = json.loads(has_photo)
        json_response = get_pets(*args, has_photo=has_photo)
        self.stdout.write(json_response)
