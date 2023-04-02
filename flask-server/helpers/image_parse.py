from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from pytesseract import pytesseract
import os
from models import FNCE_Lead_Model


def image_parse(db: SQLAlchemy):
    # Defining paths to tesseract.exe
    # and the image we would be using
    path_to_tesseract = r"/opt/homebrew/bin/tesseract"
    image_folder = os.path.expanduser("~/Documents/Bendito/fnce_leads")
    # img = Image.open(image_path)

    # Providing the tesseract
    # executable location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract

    # check for duplicative data
    fnce_leads_added = []
    for _, _, file_names in os.walk(image_folder):
        # Iterate over each file_name in the folder
        for file_name in file_names:
            if file_name.find("DS_Store") == -1:
                # Opening the image with PIL & storing it in an image object
                img = Image.open(os.path.join(image_folder, file_name))
                # Passing the image object to
                # image_to_string() function
                raw_text = pytesseract.image_to_string(
                    img)
                text_list = [x for x in raw_text.strip().split(
                    "\n") if x != "" and x != "¢" and x != "<"]
                if "Details Qualifications" in text_list:
                    index_of_name = text_list.index(
                        "Details Qualifications") + 1
                    # parsing error where random letters appear in the index after details qualifications
                    if text_list[index_of_name].lower() == text_list[index_of_name] and len(text_list[index_of_name]) < 6:
                        index_of_name = index_of_name + 1
                        name = text_list[index_of_name]
                    # parsing error where name is split into two elements of list
                    elif len(text_list[index_of_name].split(" ")) < 2 and text_list[index_of_name].lower() != text_list[index_of_name] and text_list[index_of_name + 1].lower() != text_list[index_of_name + 1]:
                        name = text_list[index_of_name] + \
                            " " + text_list[index_of_name+1]
                    # typical parsing of name
                    else:
                        name = text_list[index_of_name]
                else:
                    name = text_list[text_list.index("Lead Details") + 1]
                first_name = name.split(" ")[0].lower()
                last_name = name.split(" ")[1].lower()

                new_fnce_lead_dict = {"id": "", "first_name": first_name, "last_name": last_name,
                                      "is_dietitian": False, "is_student": False, "description": ""}
                for word in text_list:
                    if word.lower().find("dietitian") != -1:
                        new_fnce_lead_dict["is_dietitian"] = True
                    elif word.lower().find("student") != -1:
                        new_fnce_lead_dict["is_student"] = True
                    # grab the email from the text list
                    if word.find("@") != -1:
                        # fix incorrect text interpretations
                        if word.find("|") != -1:
                            word = word.replace("|", "l")
                            if word.find("l ") != -1:
                                word = word[2:]
                        new_fnce_lead_dict["id"] = word

                new_fnce_lead_dict["description"] = " ".join(text_list)
                if new_fnce_lead_dict["id"] not in fnce_leads_added:
                    # manual update
                    if name == "Diana Pinto-":
                        first_name = "diana"
                        last_name = "pinto-sanchez"
                        new_fnce_lead_dict["first_name"] = first_name
                        new_fnce_lead_dict["last_name"] = last_name

                    new_fnce_lead = FNCE_Lead_Model(
                        fnce_lead_dict=new_fnce_lead_dict)
                    db.session.add(new_fnce_lead)
                    fnce_leads_added.append(new_fnce_lead_dict["id"])

    db.session.commit()
