import requests


URL = "https://careers.calstate.edu/#top"

search_params = {
  "keywords": "",
  "zipcode": "",
  "jobtype": "1",
  "dist": "20",
  "campusList": "null",
  "jobposted": "0",
  "timebase": "4",
  "appttype": "1",
  "bgunit": "R03",
  "disciplineList": "null"
}

    # Add other parameters as needed
response = requests.post(URL, data = search_params)
if response.status_code == 200:
    # Assuming the response contains HTML data
    # You can parse the HTML using a library like BeautifulSoup
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.content, 'html.parser')
    #NumResults = soup.find('div', style="margin: 0px 10px !important; cursor: default;" )
    resultn = soup.find(id="totalRecords")
    print("Num Results:", resultn.text)
    #print("Results ", num.text)
    print(resultn.prettify())
    #print(soup.prettify())
    # Example: Find and print job listings (customize for your webpage structure)
    
else:
    print("Failed to retrieve the webpage. Status Code:", response.status_code)

