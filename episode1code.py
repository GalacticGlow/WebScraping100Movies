#order for 150$
#order details: find every website with the .portal.athenahealth.com address, they differ by their number before the first dot. find all these websites, take the name of the clinic from it and add them to an excel file
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_clinic_name(clinic_id):
    url = f"https://{clinic_id}.portal.athenahealth.com/" #this is called an "f-string", basically anything that's in the curly brackets will be parsed into the string, even if the variable in the brackets isn't a string
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    clinic_name = soup.find_all('h1')[-1].text.strip()
    return clinic_name
#now we try to figure out how many websites of the type we're looking for exist
start = 12690
end = 12710

master_list = []

for clinic_id in range(start, end+1):#adding the id and name of the website to a dictionary, and we add all the dictionaries to a list
    data_dict = {}
    data_dict['clinic_id'] = clinic_id
    data_dict['clinic_name'] = get_clinic_name(clinic_id)
    if data_dict['clinic_name'] != "Payment Confirmation" and data_dict['clinic_name'] != "Sorry, we can't find that practice. Make sure you typed the right address.":
        master_list.append(data_dict)
#now we create a dataframe from our master_list and transform it into a csv file, which will become an Excel file
print(master_list)
df = pd.DataFrame(master_list)
df.to_csv('clinic_data.csv', index=False)
print(df)