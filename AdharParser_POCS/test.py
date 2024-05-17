from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\sairavali\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

model_path = "./my_model/xlm-roberta-large-finetuned-conll03-english/"
tokenizer = AutoTokenizer.from_pretrained(model_path,model_max_length=512)
model = AutoModelForTokenClassification.from_pretrained(model_path)
classifier = pipeline("ner", model=model, tokenizer=tokenizer,aggregation_strategy="simple")

def name_extract(text):
    text  = text.replace(".",",")
    words = text.split()
    cleaned_list = remove_duplicates(words)
    english_text = ' '.join(find_english_words(cleaned_list))
    output = classifier(english_text)
    person_entities = [entity for entity in output if entity['entity_group'] == 'PER']
    for entity in person_entities:
        name = entity['word']
        break
    return name.replace("\n","")

def aadhar_front_ocr(image_path):
    img = Image.open(image_path)
    img = np.asarray(img)
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    img = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)    
    text = pytesseract.image_to_string(img,config='-l tel+eng --psm 12')
    return text

def aadhar_back_ocr(image_path):
    img = Image.open(image_path)
    img = np.asarray(img)
    img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    img = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)    
    text = pytesseract.image_to_string(img,config='-l eng --psm 3')
    return text

def remove_duplicates(input_list):
    seen = {}
    result = []
    for item in input_list:
        if item not in seen:
            result.append(item)
            seen[item] = True
    return result

def find_english_words(input_list):
    english_words = []
    for item in input_list:
        english_words += re.findall(r'[a-zA-Z0-9/,:-]+', item)
    return english_words

def extract_addresses(text):
    # Define the regular expression pattern
    text = text.replace("5/0","S/O")
    text = text.replace("9/0","S/O")
    text = text.replace("3/0","S/O")

    address_pattern = r'(S/O|W/O|S/O:|W/O:)(.*?\d{6})'
    
    # Find all occurrences of the address pattern in the text
    addresses = re.findall(address_pattern, text, re.IGNORECASE | re.DOTALL)
    return addresses

def get_address(text):
    text  = text.replace(".",",")
    words = text.split()
    cleaned_list = remove_duplicates(words)
    english_text = ' '.join(find_english_words(cleaned_list))
    addresses = extract_addresses(english_text)
    addresses = [elem for tpl in addresses for elem in tpl]
    cleaned_text = ' '.join(addresses)
    return cleaned_text

filename = r"C:\Users\sairavali\Desktop\Ad_parser\Parser_pro\445_Adhaar_card_Aarti (1).jpg"

text = aadhar_front_ocr(filename)
addr = aadhar_back_ocr(filename)

dob_pattern = r'(?:DOB|008): (\d{2}/\d{2}/\d{4})'
aadhar_pattern = r'(\d{4} \d{4} \d{4})'
sex_pattern = r'(MALE|FEMALE|Male|Female)'
name = name_extract(text)
address = get_address(addr)



if re.search(dob_pattern, text) is None:
    dob = re.search(r'Year of Birth : (\d{4})',text).group(1)
else:
    dob = re.search(dob_pattern, text).group(1)

aadhar = re.search(aadhar_pattern, text).group(1)
sex = re.search(sex_pattern, text).group(1)


print("Name:", name)
print("DOB:", dob)
print("Aadhar Number:", aadhar)
print("Sex:", sex)
print("Address:",address)