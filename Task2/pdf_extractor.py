import pandas as pd
import pytesseract.pytesseract
import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request as urlreq
from pdf2image import convert_from_path
import os
import cv2
from PIL import Image
import json

'''---------------------1. READING DATA FROM EXCEL FILE-----------------------------------'''

def read_data(filename):
    # Reading Excel File
    data = pd.read_excel(filename, header=None)

    # Converting dataframe to list
    list_of_links = data.iloc[:, 0].values

    return list_of_links


'''---------------------2. FETCHING CONTENTS FROM LINKS AND STORING-----------------------'''

def pdf_download(list_of_links):
    opener = urlreq.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urlreq.install_opener(opener)

    i = 0
    for link in list_of_links:
        if '.pdf' in link:
            urlreq.urlretrieve(link, f"Downloaded_pdfs/pdf{i}.pdf")

        else:
            domain = "https://" + urlparse(link).netloc
            response = req.get(link)
            extracted_html = BeautifulSoup(response.text, 'html.parser')
            links_in_html = extracted_html.find_all('a')
            for sublink in links_in_html:
                if '.pdf' in sublink.get('href', []):
                    urlreq.urlretrieve(domain+sublink.get('href'), f"Downloaded_pdfs/pdf{i}.pdf")
                    break

        print(f"Downloaded PDF {i}")
        i += 1


'''---------------------3. CONVERTING PDFS TO IMAGES--------------------------------------'''

def pdf_to_images(path_to_pdf_directory, path_to_poppler_bin):
    for i in range(48):
        pages = convert_from_path(path_to_pdf_directory+f"\\pdf{i}.pdf", 300,
                                  poppler_path=path_to_poppler_bin)
        j = 0
        new_path = os.path.join("PDF_Images", f"Pdf{i}")
        os.mkdir(new_path)
        for page in pages:
            img_path = new_path + f"\\Pic_{j}.jpg"
            page.save(img_path, "JPEG")
            j += 1
        print(f"PDF {i} Done")


'''---------------------4. PROCESSING IMAGES-------------------------------------------'''

def process_pdf_images(list_of_pdf_links, path_to_pdf_images_dir, path_to_tesseract_exe, path_to_tessdata,
                       language="en", columns=False):
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract_exe
    tessdata_config = f'--tessdata-dir "{path_to_tessdata}" '
    if columns == True:
        tessdata_config += '--psm 3'
    else:
        tessdata_config += '--psm 6'

    json_content = []

    dirs = os.listdir(path_to_pdf_images_dir)
    dirs.sort(key=lambda x: int(x[3:]))

    for (i, dir) in enumerate(dirs):
        sub_dir = path_to_pdf_images_dir + "\\" + dir
        files = os.listdir(sub_dir)
        files.sort(key=lambda x: int(x[4:-4]))

        j, c, f = 0, 0, 0
        for file in files:
            img_path = sub_dir + "\\" + file
            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            tmp_file = f"{f}.png"
            f += 1
            cv2.imwrite(tmp_file, thresh)
            text = pytesseract.image_to_string(Image.open(tmp_file), lang=language, config=tessdata_config)
            os.remove(tmp_file)
            text = text.replace('\n', '')

            content = {}

            if ".pdf" in list_of_pdf_links[i]:
                content["pdf-url"] = list_of_pdf_links[i]
                content["page-url"] = content["pdf-url"]
            else:
                link = list_of_pdf_links[i]
                if "page" in link:
                    base_link = link.split("page")[0]
                else:
                    base_link = link.split("mode")[0]

                content["pdf-url"] = base_link + "mode/2up"
                if j == 0:
                    content["page-url"] = content["pdf-url"]
                    j += 1
                else:
                    content["page-url"] = base_link + f"page/n{j}/mode/2up"
                    c ^= 1
                    if c == 0:
                        j += 2

            content["pdf-content"] = text

            json_content.append(content)

        print(f"PDF {i} processed!")

    return json_content


'''---------------------5. PREPARING JSON FILE--------------------------------------------'''

def save_json_file(filename, json_content):
    with open(filename, "w") as file:
        json.dump(json_content, file, indent=2, ensure_ascii=False)


'''---------------------MAIN FUNCTION-----------------------------------------------------'''

def main():
    # ADD PATH of excel sheet
    filename = ''

    list_of_pdf_links = read_data(filename)

    pdf_download(list_of_links=list_of_pdf_links)

    # ADD PATH to "Downloaded_pdfs"
    path_to_pdf_directory = ""
    
    # ADD PATH to poppler bin folder
    path_to_poppler_bin = ""
    
    pdf_to_images(path_to_pdf_directory=path_to_pdf_directory, path_to_poppler_bin=path_to_poppler_bin)

    # ADD PATH to "PDF_Images"
    path_to_pdf_images_dir = ""
    
    # ADD PATH to "tesseract.exe"
    path_to_tesseract_exe = ""
    
    # ADD PATH to tessdata folder
    path_to_tessdata = ""
    
    # ADD language to be used
    language = ""
    
    json_content = process_pdf_images(list_of_pdf_links = list_of_pdf_links,
                                      path_to_pdf_images_dir=path_to_pdf_images_dir,
                                      path_to_tesseract_exe=path_to_tesseract_exe,
                                      path_to_tessdata=path_to_tessdata,
                                      language=language,
                                      columns=True)
    
    save_json_file(filename="pdf_extract.json", json_content=json_content)


if __name__ == "__main__":
    main()
