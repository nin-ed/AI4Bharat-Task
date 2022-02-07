# Task 1

## What is it and how does this work?
This directory named as **"Task1"** consists of two files - 
1. **wiki_extractor.py -** Python script to extract wikipedia data
2. **out.json -** Output file of a sample script run mentioned in the section "Sample" below.
3. **requirements.txt -** File containing necessary libraries to be installed to run the above mentioned script.


The whole script is broken down into three sections - 
1. **Wiki Fetch -** It fetches the title of the pages, by taking keyword and number of urls needed, as input and passing it through wikipedia API which in return, returns the list of titles of the pages according our requirements.
2. **Scrapping Data -** The list is passed to this section to further processing. It takes each title one by one, and fetches the content of the data using Beautiful Soup. Because we just need the textual data from the pages, we visit the "paragraph" tags and fetch its contents. Further, the contents are cleaned by removing escape characters and special symbols. After cleaning, we create a list of dictionaries and returned.

    > **Note:** *Here I have taken data of upto 10 sentences because in some pages, first paragraph only consisted of few words*.
3. **Preparing JSON file -** In this section, the list of dictionaries and the desired output file name is passed. It converts the list of dictionaries into a JSON and saves it into the file.


## Sample
A sample script ran to produce the results stored in file **out.json** can be reproduced as follows - 


1. Download the libraries needed described in **requirements.txt** by running following line in command prompt:
      > pip3 install -r requirements.txt
2. Now run the following command:
      > python wiki_extractor.py --keyword={Your query enclosed in double quotes} --num_urls={Integer value of number of urls needed} --output={Name of the output file enclosed in double quotes}
    
      In this mentioned case it would be -
      > python wiki_extractor.py --keyword="Indian historical events" --num_urls=100 --output="out.json"
