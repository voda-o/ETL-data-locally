import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

# store the final output data
target_file = "transformed_data.csv" 

# create a function to extract from a csv file
def extract_from_csv(file_to_process): 
    dataframe = pd.read_csv(file_to_process) 
    return dataframe 

# create a function to extract from a json file
def extract_from_json(file_to_process): 
    dataframe = pd.read_json(file_to_process, lines=True) 
    return dataframe 

# create a function to extract from an xml file
def extract_from_xml(file_to_process): 
    dataframe = pd.DataFrame(columns=["name", "height", "weight"]) 
    tree = ET.parse(file_to_process) 
    root = tree.getroot() 
    for person in root: 
        name = person.find("name").text 
        height = float(person.find("height").text) 
        weight = float(person.find("weight").text) 
        dataframe = pd.concat([dataframe, pd.DataFrame([{"name":name, "height":height, "weight":weight}])], ignore_index=True) 
    return dataframe 

# create a function to identify which function to call based on the filetype of the data file
def extract(): 
    # create an empty data frame to hold extracted data 
    extracted_data = pd.DataFrame(columns=['name','height','weight'])
     
    # process all csv files 
    for csvfile in glob.glob("*.csv"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True) 
         
    # process all json files 
    for jsonfile in glob.glob("*.json"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True) 
     
    # process all xml files 
    for xmlfile in glob.glob("*.xml"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True) 
         
    return extracted_data

def transform(data): 
    # convert cm to m and round off to two decimals
    data['height'] = round(data.height / 100, 2)
    
    return data 
    print (data)

# load the transformed data to a csv file
def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file) 

# call the functions
extracted_data = extract() 
transformed_data = transform(extracted_data) 
load_data(target_file,transformed_data) 