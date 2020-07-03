from PIL import Image
import os
import sys
from tree.models import Couple
from django.core.management.base import BaseCommand

raw_img_path = r"../raw_img"
out_img_path = r"tree/static/tree/img/members"

class Command(BaseCommand):
    help = 'Generate tree_structure.json'

    def handle(self, *args, **options):
        global raw_img_path
        for couple in Couple.objects.all():
            if couple.wife_name:
                wife_raw_img = os.path.abspath( os.path.join(os.getcwd(), raw_img_path, f"{''.join(couple.wife_name.lower().split())}.jpg") )
            if couple.husband_name:
                husband_raw_img = os.path.abspath( os.path.join(os.getcwd(), raw_img_path, f"{''.join(couple.husband_name.lower().split())}.jpg") )
            
            # if os.path.exists(os.path.abspath(os.path.join(os.getcwd(), wife_raw_img))):
            if os.path.exists(wife_raw_img):
                self.__process_img(wife_raw_img)
            if os.path.exists(husband_raw_img):
                self.__process_img(husband_raw_img)

    def __process_img(self, inImg):
            def resize_single_img(inImgPath, sizeThreshold=500):
                if type(inImgPath)==str:
                    raw_img = Image.open(inImgPath)
                    if raw_img.height > sizeThreshold or raw_img.width > sizeThreshold:
                        output_size = (sizeThreshold, sizeThreshold)
                        raw_img.thumbnail(output_size)
                        raw_img.save(os.path.join(out_img_path, os.path.split(inImgPath)[1]))

            resize_single_img(inImg)
