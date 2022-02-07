# Task 2

## What is it?
In this task, we need to extract data from multiple pdf files mentioned in an excel sheet.

This repository contains following files - 
1. **pdf_extractor.py -** Python script to extract pdf data.
2. **pdf_extract.json -** Extracted JSON file
3. **requirements.txt -** File containing the libraries required to run the script

&nbsp;

## How does it work?
The script is divided into 5 sections - 


1. **READING DATA FROM EXCEL FILE**<br/>
      In this section, data from the excel sheet is retrieved with the help of pandas. It returns a list of pdf file links.

2. **FETCHING CONTENTS FROM LINKS AND STORING**<br/>
      In this section, pdf files are retrieved using urlretrieve. For those whose direct links weren't available, in that, I have used Beautiful Soup to search for the pdf file links in the webpage. Once encountered, I use urlretrieve to download that file. All these pdfs will be downloaded into a new directory named as **Downloaded_pdfs**.


3. **CONVERTING PDF PAGES INTO IMAGES**<br/>
      In this section, first you need to pass the path of the **Downloaded_pdfs** folder and path to the poppler bin folder to the function. In this section, a new directory naming **PDF_Images** is created which stores the pictures of each page with respect to pdfs. 


4. **PROCESSING IMAGES**<br/>
      In this section, the function takes six arguments - <br/>
      - **list_of_pdf_links      -** List that was extracted in section 1.<br/>
      - **path_to_pdf_images_dir -** Path to the directory **PDF_Images**.<br/>
      - **path_to_tesseract_exe  -** Path to the tesseract.exe<br/>
      - **path_to_tessdata       -** Path to a directory named as **tessdata**. It is present inside the Tesseract-OCR directory.<br/>
      - **language               -** Language being used in the data or language that you would want the tesseract to operate on.<br/>
      - **columns                -** True/False. It enables/disables the mode to consider the columns used in the PDF.<br/>


      First we iterate on the files. Upon iterating, once we encounter images, we process them. Then, we convert the images to grayscale and apply threshold so that we can see the writings clearly. Then, we pass this to image_to_string of pytesseract with configurations. There are two configurations/ modes on how we can read the data from the images - <br/>
      - **--psm 6** is to read from leftmost to rightmost. It doesn't care about the columns.<br/>
      - **--psm 3** is to read the data when the contents are divided into column paragraphs. It reads data columnwise in this mode.<br/>

      So, here I have used **--psm 3** to read the data column-wise first. The text received is processed again to clean it.

      Now after this, it starts appending **pdf-urls**, **page-urls**, and **page-content** to a dictionary, which is further appended into a list named as **json_content**. The function returns this list of dictionaries.


5. **PREPARING JSON FILE**<br/>
      In this section, the list of dictionaries is stored into a JSON file named as **pdf_extract.json** present in this directory.

&nbsp;

## How to run the code?
1. Download **Tesseract-OCR** and **poppler**, and set TESSDATA_PREFIX in the environment variables to the path to **tessdata** directory present in the folder named as **Tesseract-OCR**.
2. Assign the path to the variables left blank in the code. It will be denoted with comments like *# ADD PATH*.
3. Download the required libraries by running following command in terminal - 
      > pip3 install -r requirements.txt

4. Now run the **main** or simply type the follwing command in the terminal - 
      > python pdf_extractor.py 
