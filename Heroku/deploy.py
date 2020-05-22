import requests
from bs4 import BeautifulSoup
from flask import Flask

list_id = ['CMND1', 'CMND2', 'CMND3', 'CMND4'] #Change Here

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

def SendReportWithID(main_id):
	main_params = {
		'CodeNumber': main_id,
		'IsFill': True,
		'GoOut': '',
		'GoOutNote': '', 
		'IsCough': False,
		'IsFever': False,
		'IsBreathDifficulty': False,
		'IsSoreThroat': False,
		'IsIllness': False,
		'GoHospital': '',
		'IsContactInfected': False,
		'IsContactSuspectInfected': False,
		'IsContactEntried': False,
		'IsContactTravelPlane': False,
		'IsContactInfected14Days': False,
		'IsContactSuspectInfected14Days': False,
		'Submit': ''
	}
	with requests.Session() as s:
		#GET PARAMS
		url = "http://svktx.vnuhcm.edu.vn/Default/LoadStudentInfoDiseaseCovidReport/"
		params = {
			'CodeNumber' : main_id
		}
		r = s.post(url, data = params, headers = headers)
		soup = BeautifulSoup(r.content, 'html.parser')
		main_params['Id'] = soup.find('input', attrs={'name': 'Id'})['value']
		main_params['StudentId'] = soup.find('input', attrs={'name': 'StudentId'})['value']
		main_params['StudentCode'] = soup.find('input', attrs={'name': 'StudentCode'})['value']
		main_params['IdCardNumber'] = soup.find('input', attrs={'name': 'IdCardNumber'})['value']
		main_params['UniversityId'] = soup.find('input', attrs={'name': 'UniversityId'})['value']
		main_params['DormitoryHouseId'] = soup.find('input', attrs={'name': 'DormitoryHouseId'})['value']
		main_params['DormitoryRoomId'] = soup.find('input', attrs={'name': 'DormitoryRoomId'})['value']
		main_params['FullName'] = soup.find('input', attrs={'name': 'FullName'})['value']
		main_params['UniversityName'] = soup.find('input', attrs={'name': 'UniversityName'})['value']
		main_params['DormitoryFullName'] = soup.find('input', attrs={'name': 'DormitoryFullName'})['value']
		#SEND REQUEST
		url_2 = "http://svktx.vnuhcm.edu.vn/Default/DiseaseCovidReport"
		r_2 = s.post(url_2, data = main_params, headers = headers)

app = Flask(__name__)

@app.route('/')
def index():
	for id in list_id:
	    SendReportWithID(id)
	_result = "<title>Daily Report KTX</title>"
	_result += "Status: Cron Success!!<br>" 
	_result += "Source: https://github.com/caohungphu/AutoCovidReportKTX<br>"
	_result += "Author: Cao Hung Phu<br>"
	_result += "Facebook: caohungphuvn<br>"
	_result += "Contact: caohungphuvn@gmail.com"
	return _result