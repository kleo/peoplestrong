import requests
from bs4 import BeautifulSoup
import base64
from base64 import b64decode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import datetime
from fake_useragent import UserAgent
import re
import json
import holidays

ph_holidays = holidays.PH()

if datetime.datetime.today() in ph_holidays:
    # Today is a holiday Labor Day 2023-05-09 12:59 
    print('Today is a holiday', ph_holidays.get(datetime.datetime.today().isoformat()), datetime.datetime.today().strftime('%Y-%m-%d %I:%M'))
else:
    # 2023-5-6 22:12:52
    time_formatted = datetime.datetime.now().strftime("%Y-%-m-%-d %-H:%-M:%-S")

    # set credentials here
    username = 'EFSI021160'
    password = time_formatted + '|' + 'k211194'

    # json8 requires employee specific information

    ua = UserAgent()

    session = requests.session()

    headers1 = {
        'Host': 'entrego.peoplestrong.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    response1 = session.get('https://entrego.peoplestrong.com/altLogin.jsf', headers=headers1)

    # 'kubesg-worklife2~eCbAXX7iW1cA7wsEJQtrcVqD-LUs6G6oJhFSwaC_.alt-worklife2-5c48479b58-k4wls'
    # print(response1.cookies.get('JSESSIONID'))

    soup = BeautifulSoup(response1.text, 'html.parser')
    # -4075476134951471660:-1882564903002077706
    viewstate = soup.find("input", {"name":"javax.faces.ViewState"})['value']

    headers2 = {
        'Host': 'entrego.peoplestrong.com',
        'User-Agent': ua.chrome,
        'Accept': '*/*',
        'Referer': 'https://entrego.peoplestrong.com/altLogin.jsf',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    params2 = {
        'v': '20230417'
    }

    response2 = requests.get('https://entrego.peoplestrong.com/javascript/crypto/crypto.js', params=params2, headers=headers2)

    cryptojs = response2.text
    cryptojs_split = cryptojs.split('\n')
    cryptojs_list = cryptojs_split[3].strip('\t').split('"')

    key64 = cryptojs_list[1]
    pubkey = b64decode(key64)

    rsa_key = RSA.importKey(pubkey)

    cipher = PKCS1_v1_5.new(rsa_key)

    username_encrypted = base64.b64encode(cipher.encrypt(str.encode(username))).decode('utf-8')
    password_encrypted = base64.b64encode(cipher.encrypt(str.encode(password))).decode('utf-8')

    session.cookies.set("dateTime", time_formatted, domain="entrego.peoplestrong.com")

    headers3 = {
        'Host': 'entrego.peoplestrong.com',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://entrego.peoplestrong.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': ua.chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'https://entrego.peoplestrong.com/altLogin.jsf',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    data3 = {
        'loginForm': 'loginForm',
        'loginForm:hideChangePassword': 'true',
        'loginForm:username12': '',
        'loginForm:username': username_encrypted,
        'loginForm:password': password_encrypted,
        'loginForm:loginButton': '',
        'javax.faces.ViewState': viewstate
    }

    response3 = session.post(
        'https://entrego.peoplestrong.com/altLogin.jsf',
        headers=headers3,
        data=data3
    )

    headers4 = {
        'Host': 'onewebapi-dc2.peoplestrong.com',
        'User-Agent': ua.chrome,
        'Content-Type': 'application/json; charset=utf-8',
        'Bundleid': '1',
        'Bundle_name': 'EN',
        'Platform': 'Web',
        'Timezone': 'Asia/Manila',
        'Accept': '*/*',
        'Origin': 'https://entrego.peoplestrong.com',
        'Referer': 'https://entrego.peoplestrong.com/oneweb/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close',
    }

    json4 = {
        'input': {
            'portalType': 'Employee Portal',
            'deviceId': 'oneapp_web_096887d0-d77e-11ed-95f5-69520a905976',
            'companyURL': 'entrego.peoplestrong.com',
            'userNameHash': '',
            'passwordHash': '',
            'keycloakEnabled': True,
            'oktaEnabled': False,
            'authToken': session.cookies.get('AccessToken'),
        },
    }

    response4 = session.post(
        'https://onewebapi-dc2.peoplestrong.com/service/user/api/login/v1',
        headers=headers4,
        json=json4
    )

    # {"responseData":{"userId":"645138","userName":"EFSI021160","email":"kleo.bercero@entrego.com.ph","profileImage":null,"profileName":"Kleo Carl Florentino Bercero","grade":null,"joiningDate":null,"organizationId":"10048","employeeCode":"EFSI021160","roleList":["EMPLOYEE","INTERVIEWER","HIRING_MANAGER"],"authToken":"ODc3N2YwODMtOGM4Ny00YWQ2LTljZjUtY2FiMTQ3MzYxMGY1X0VGU0kwMjExNjBfX19fXzEwMDQ4","refreshToken":null,"keycloakAccessToken":null,"keycloakRefreshToken":null,"isFirstLogin":"true","employeeId":"411144","entityID":"56","jidSuffix":"entrego.peoplestrong.com","jid":"645138@entrego.peoplestrong.com","sessionToken":"ODc3N2YwODMtOGM4Ny00YWQ2LTljZjUtY2FiMTQ3MzYxMGY1X0VGU0kwMjExNjBfX19fXzEwMDQ4","domain":"entrego.peoplestrong.com"},"message":{"code":"EC200","message":"Successfully login.","description":"login data has been fetched successfully."}}

    headers5 = {
        'Host': 'authdc2.peoplestrong.com',
        'User-Agent': ua.chrome,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://entrego.peoplestrong.com',
        'Referer': 'https://entrego.peoplestrong.com/oneweb/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close',
    }

    data5 = {
        'grant_type': 'refresh_token',
        'client_id': '10048',
        'refresh_token': session.cookies.get('RefreshToken'),
    }

    response5 = session.post(
        'https://authdc2.peoplestrong.com/auth/realms/10048/protocol/openid-connect/token',
        headers=headers5,
        data=data5
    )

    openid_token = json.loads(response5.text)
    # print(openid_token['refresh_token'])

    headers6 = {
        'Host': 'entrego.peoplestrong.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.chrome,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'https://entrego.peoplestrong.com/oneweb/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    params6 = {
        'sessionToken': session.cookies.get('SessionToken'),
        'source': 'ONEWEB',
        'menu': 'MyAttendance',
        'accessToken': session.cookies.get('AccessToken'),
        'refreshToken': session.cookies.get('RefreshToken'),
    }

    response6 = session.get(
        'https://entrego.peoplestrong.com/secureSloginDeeplinkKeycloak.jsf',
        params=params6,
        headers=headers6
    )

    soup6 = BeautifulSoup(response6.text, 'html.parser')
    script_tag = soup6.find('script', string=re.compile(r'_Alogin\s*=\s*'))
    javascript_code = script_tag.string
    document_cookie = javascript_code.strip()
    alogin = document_cookie.split('=')
    # print(alogin[2])

    # MyAttendance
    session.cookies.set("_Amenu", "TXlBdHRlbmRhbmNl", domain="entrego.peoplestrong.com")
    session.cookies.set("_Alogin", alogin[2], domain="entrego.peoplestrong.com")

    headers7 = {
        'Host': 'entrego.peoplestrong.com',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': ua.chrome,
        'Origin': 'https://entrego.peoplestrong.com',
        'Referer': 'https://entrego.peoplestrong.com/home.jsf',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    json7 = {
        'paramJson': alogin[2]
    }

    response7 = session.post(
        'https://entrego.peoplestrong.com/service/altone/angular/login/userdetail',
        headers=headers7,
        json=json7
    )

    userdetail = json.loads(response7.text)
    # print(userdetail['authToken'])
    # print(userdetail['zauthToken'])

    session.cookies.set("RefreshToken", openid_token['refresh_token'], domain="entrego.peoplestrong.com")

    headers8 = {
        'Host': 'entrego.peoplestrong.com',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': ua.chrome,
        'Origin': 'https://entrego.peoplestrong.com',
        'Referer': 'https://entrego.peoplestrong.com/home.jsf',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close',
        'User_token': userdetail['authToken']
    }

    json8 = {
        'data': {
            'timeZone': 'Asia/Manila',
            'shiftPremiseID': None,
            'premiseConfigured': False,
            'userMessage': None,
            'userStatus': None,
            'shiftId': 6541,
            'holiday': False,
            'roasterId': 70,
            'roasterSource': 'Organization Roster',
        },
        'dataList': None,
        'dataMap': None,
        'identity': {
            'userId': 645138,
            'employeeId': 411144,
            'employeeIdSecure': 'Y6A66iThqmMTxxJhOb3r6Q==',
            'organizationId': 10048,
            'tenantId': 10035,
            'roleList': [
                10496,
                10501,
                10426,
            ],
            'platform': 'WEB',
            'bundleName': 'EN',
            'excludedMenuList': None,
            'employeeCode': 'EFSI021160',
            'orgUnitId': 78889,
            'photoPath': None,
            'firstName': 'Kleo Carl',
            'userName': 'EFSI021160',
            'leftPhotoURL': 'https://staticdc2.peoplestrong.com/talentpact/server/appdata/system/tenant_10035/org_10048/logo/MicrosoftTeams-image (12).png',
            'jinieEnabled': True,
            'zippiEnabled': True,
            'authToken': userdetail['authToken'],
            'tcFlag': True,
            'tcShowFlag': True,
            'tcAcceptFlag': False,
            'termsAndConditionsModuleConfig': None,
            'tcData': 'TC DATA',
            'tcCheckbox': False,
            'tcCheckLabel': 'TC CHECK BOX LABEL',
            'tcSave': 'SAVE',
            'tcDataViewable': False,
            'tcSaveViewable': False,
            'sectorId': None,
            'hideChangePassword': True,
            'zauthToken': userdetail['zauthToken'],
            'userGroupList': None,
            'groupPolicyList': None,
            'countryID': 411,
            'customLandingPageId': None,
            'countryRoleList': {
                '411': [
                    10496,
                    10501,
                    10426,
                ],
            },
            'entityRoleMap': {
                '56': [
                    10496,
                    10501,
                    10426,
                ],
            },
            'organizationCode': 'Entrego',
            'alumni': None,
            'sysBundleID': 1,
            'entityID': 56,
            'sessionToken': session.cookies.get('SessionToken'),
            'formName': None,
            'worksiteId': 10512,
        },
    }

    response8 = session.post(
        'https://entrego.peoplestrong.com/service/altone/angular/punch-card/punch-in',
        headers=headers8,
        json=json8
    )

    # {"data":{"punchInOutTimeTO":{"punchDate":"2023-05-08","punchInTime":"01:04","punchOutTime":null,"punchInRendered":false,"punchOutRendered":true,"attendanceId":0,"singlePunch":false,"messageForOut":null,"shiftPremiseList":null,"message":null,"inSetUp":null,"outSetUp":null,"shiftId":777,"holiday":false,"roasterId":70,"roasterSource":"Organization Roster","defaultWithThresHoldShift":true}},"message":{"code":"S100","desc":"operation successful","displayMsg":""}}

    # note: second punch in request will punch out time, any subsequent punch outs during the day will update punch out time

    # {"data":{"punchInOutTimeTO":{"punchDate":"2023-05-08","punchInTime":"01:04","punchOutTime":"01:11","punchInRendered":false,"punchOutRendered":true,"attendanceId":0,"singlePunch":false,"messageForOut":null,"shiftPremiseList":null,"message":null,"inSetUp":null,"outSetUp":null,"shiftId":777,"holiday":false,"roasterId":70,"roasterSource":"Organization Roster","defaultWithThresHoldShift":true}},"message":{"code":"S100","desc":"operation successful","displayMsg":""}}

    # print(response8.text)
    punch_dict = json.loads(response8.text)

    if punch_dict['data']['punchInOutTimeTO']['punchOutTime'] is None:
        print('Clocked In on', punch_dict['data']['punchInOutTimeTO']['punchDate'], punch_dict['data']['punchInOutTimeTO']['punchInTime'])
    else:
        print('Clocked Out on', punch_dict['data']['punchInOutTimeTO']['punchDate'], punch_dict['data']['punchInOutTimeTO']['punchOutTime'])

    # Clocked In on 2023-05-08 01:04
    # Clocked Out on 2023-05-08 01:35