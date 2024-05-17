import re
import easyocr
reader = easyocr.Reader(['en'])

def pan_ocr(image_path):
    result = reader.readtext(image_path, detail = 0,text_threshold=0.8)
    return result


def replace_letters(word):
    if len(word) != 10:
        print("Error: The input word must be exactly ten letters.")
        return
    letters = list(word)
    for i in range(4, 9):
        if letters[i] == 'I':
            letters[i] = '1'
        elif letters[i] == 'O':
            letters[i] = '0'
        elif letters[i] == 'S':
            letters[i] = '5'
        else:
            pass
    if letters[9] == '1':
      letters[9] = 'I'
    elif letters[9] == '0':
      letters[9] = 'O'
    elif letters[9] == '5':
      letters[9] = 'S'
    result = ''.join(letters)
    return result


# result = pan_ocr("C:\\Users\\aslam\\Desktop\\Pan_Parser\\shaik3.jpg")

# text = " ".join(text for text in result)

# # Pattern for PAN
# pan_pattern = re.compile(r'[A-Z]{3}[PCFTGHLABJ]{1}[A-Z]{1}[IO0-9]{4}[A-Z]{1}')

# # Pattern for DOB
# date_pattern = re.compile(r'(\d{2}/\d{2}/\d{4})')

# # Extracting PAN
# pan_num = [pan for pan in result if pan_pattern.search(pan)]
# pan_num = replace_letters(pan_num[0])

# # Extracting DOB
# dob_match = date_pattern.search(text)
# dob = dob_match.group(1) if dob_match else None

# # Extracting Name
# name = [result[i+1] for i in range(len(result)-1) if ("Name" in result[i] or "Mame" in result[i]) and "Father" not in result[i]]
# name = name[0].replace("$","S").upper()

# # Extracting Father's Name
# father_name = [result[i+1] for i in range(len(result)-1) if "Father" in result[i] and "Name" in result[i]]
# father_name = father_name[0].replace("$","S").upper()

# print(f'PAN: {pan_num}')
# print(f'DOB: {dob}')
# print(f'Name: {name}')
# print(f"Father's Name: {father_name}")