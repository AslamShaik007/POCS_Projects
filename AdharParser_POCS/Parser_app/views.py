from django.shortcuts import render
from .models import AdharFile
# Create your views here.
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import os.path
from django.http import HttpResponse
from .utils import name_extract,aadhar_front_ocr,aadhar_back_ocr,remove_duplicates,find_english_words,extract_addresses,get_address, save_base64_image
from .models import AdharFile
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from tempfile import NamedTemporaryFile
import uuid
import os
from rest_framework.parsers import MultiPartParser
from .utils2 import pan_ocr, replace_letters
from datetime import datetime

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ajay.b\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


class ParseAdharView(viewsets.ModelViewSet):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    # permission_classes = [IsAuthenticated]
      
    def create(self, request, *args, **kwargs):
        try:
            file = request.FILES.get("adhar_file")
            if file:
                adhar_obj = AdharFile.objects.create(file = file)
                filename = f"media/{adhar_obj.file.name}"
                text = aadhar_front_ocr(filename)
                addr = aadhar_back_ocr(filename)
                dob_pattern = r'(?:DOB|008): (\d{2}/\d{2}/\d{4})'
                aadhar_pattern = r'(\d{4} \d{4} \d{4})'
                sex_pattern = r'(MALE|FEMALE|Male|Female)'
                name = name_extract(text)
                address = get_address(addr)
                try:
                    if re.search(dob_pattern, text) is None:
                        dob = re.search(r'Year of Birth : (\d{4})',text).group(1)
                    else:
                        dob = re.search(dob_pattern, text).group(1)
                except Exception:
                    dob = None
                try:
                    aadhar = re.search(aadhar_pattern, text).group(1)
                except Exception as e:
                    aadhar = None
                try:
                    sex = re.search(sex_pattern, text).group(1)
                except Exception:
                    sex = None
                data = {
                    "name": name,
                    "dob" : dob,
                    "adhar_number" : aadhar,
                    "gender": sex,
                    "address" : address,
                }
                adhar_obj.delete()
                os.remove(filename)
                return Response(data, status=200)
            else:
                return Response({
                        "status_code": 400,
                        "message": "Adhar File is required"
                    }, status=400)
        except Exception as e:
            return Response({
                "status_code": 400,
                "message": str(e)
            }, status=400)
            
class PanCardParser(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        if not request.FILES.get("pan_image"):
            return Response({
                "status_code" : 400,
                "message": "PAN is required"
            })
        try:
            pan_image = request.FILES.get('pan_image')
            image_data = pan_image.read()
            if isinstance(pan_image, str):
                with open(pan_image, 'rb') as file:
                    image_data = file.read()
            elif isinstance(pan_image, np.ndarray):
                image_data = pan_image.tobytes()

            result = pan_ocr(image_data)

            text = " ".join(text for text in result)

            pan_pattern = re.compile(r'[A-Z]{3}[PCFTGHLABJ]{1}[A-Z]{1}[IOS0-9]{4}[015A-Z]{1}')

            date_pattern = re.compile(r'(\d{2}/\d{2}/\d{4})')
            
            
            pan_num = [pan for pan in result if pan_pattern.search(pan) and len(pan) == 10]
            try:
                pan_num = replace_letters(pan_num[0])
            except:
                pan_num = ""
            try:
                dob_match = date_pattern.search(text)
                dob = dob_match.group(1) if dob_match else None
                dob = datetime.strptime(dob, '%d/%m/%Y').strftime('%Y-%m-%d') if dob else None
            except:
                dob = ""
            try:
                name = [result[i+1] for i in range(len(result)-1) if ("Name" in result[i] or "Mame" in result[i]) and "Father" not in result[i]]
                name = name[0].replace("$","S").upper()
            except:
                name = ""
            try:
                father_name = [result[i+1] for i in range(len(result)-1) if "Father" in result[i] and "Name" in result[i]]
                father_name = father_name[0].replace("$","S").upper()
            except:
                father_name = ""
            pan_card_data = {
                "pan_number": pan_num,
                "date_of_birth": dob,
                "name": name,
                "father_name": father_name
            }
            return Response(
                pan_card_data, status=200
            )
        except Exception as e:
            return Response(
                {
                    "status_code": 400,
                    "message": "Error Scanning Pancard"
                },
                status=400
            )
