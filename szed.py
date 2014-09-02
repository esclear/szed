#!/usr/bin/python
import cookielib, urllib, urllib2, sys, datetime, re, os.path, getopt

#### CONFIG SECTION ###############################################################

user   = 'USERNAME'
pwd    = 'PASSWORD'
issues = [
		'Bayernausgabe_komplett',
		#'Bayernausgabe_basis',
		'Deutschlandausgabe_komplett',
		#'Deutschlandausgabe_basis',
		'Stadtausgabe_komplett',
		#'Stadtausgabe_basis',
		#'Stadtausgabe_Muenchen-City',
		#'Stadtausgabe_Muenchen-Nord',
		#'Stadtausgabe_Muenchen-Sued',
		#'Stadtausgabe_Muenchen-West',
		#'Dachau',
		#'Ebersberg',
		#'Erding',
		#'Freising',
		#'Fuerstenfeldbruck',
		#'Starnberg',
		#'Wolfratshausen'
]

###################################################################################
tdate = datetime.datetime.today()
dir = './sz/'

def Usage():
		print "Usage: szed.py -p place -d day"

try:
	options, args = getopt.getopt(sys.argv[1:], 'd:p:', ['place=', 'date='])
except getopt.GetoptError:
	Usage()
	sys.exit(2)

for o, a in options:
	if o in ("-d", "--date"):
		tdate = datetime.datetime.strptime(a, "%Y-%m-%d")
	if o in ("-p", "--place"):
		dir = a

#### PROGRAM ######################################################################
print("SZ-Downloader Version 2.0.0\n(c) 2013 - 2014 by Daniel Albert\n")

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

print("Fetching login form ...")
resp_lform = opener.open('https://id.sueddeutsche.de/login').read()

## get login_ticket_id
login_ticket_pattern = re.compile(r'<input type="hidden" name="login_ticket" id="id_login_ticket" value="([A-Za-z0-9\-]{32})" />')
login_ticket_match   = login_ticket_pattern.search(resp_lform)
login_ticket         = login_ticket_match.group(1)
#print("[DBG]: login_ticket_id=" + login_ticket)

## get anti csrf token
login_acsrft_pattern = re.compile(r'<input type="hidden" name="_csrf" id="id__csrf" value="([^\"]+)" />')
login_acsrft_match   = login_acsrft_pattern.search(resp_lform)
login_acsrft         = login_acsrft_match.group(1)
#print("[DBG]: login_anti-csrf-token=" + login_acsrft)

## Try to login
print("\nLogging in...")
data = urllib.urlencode({
		'login'        :user,
		'password'     :pwd,
		'login_ticket' :login_ticket,
		'_csrf'        :login_acsrft,
		'tracking_id'  :''
	})

resp_login = opener.open('https://id.sueddeutsche.de/login', data)

if "Logout" in resp_login.read():
	print("Login successful!")
else:
	print("Login failed!")
	sys.exit(1)

## Login into epaper
resp_eplogi = opener.open('https://id.sueddeutsche.de/service/ticket?redirect_uri=http://epaper.sueddeutsche.de/digiPaper/servlet/attributeloginservlet&service_id=epaper')

## Get list of issues
resp_index = opener.open('http://epaper.sueddeutsche.de/app/epaper/pdfversion/szglobal_down.php')
indextext = resp_index.read()

if 'value=' + tdate.strftime("%Y%m%d") in indextext:
	print("SZ for that day is available. Starting download!\n")
else:
	print("No up-to-date SZ found.")
	sys.exit(1)

# Get URLs
data = urllib.urlencode({ 'param_date': tdate.strftime("%Y%m%d") })

resp_index = opener.open('http://epaper.sueddeutsche.de/app/epaper/pdfversion/szglobal_down.php', data)

indextext = resp_index.read()

# -> Regex
file_path_pattern = re.compile(r'/app/pdfdownload/([0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12})/([0-9]{8})_([a-zA-Z_]+)_([0-9]{8,})\.pdf')
# http://epaper.sueddeutsche.de/app/pdfdownload/
# ([0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12})
# /
# ([0-9]{8})
# _
# ([a-zA-Z_]+)
# _
# ([0-9]{18})
# \.pdf

file_path_match = file_path_pattern.search(indextext)

file_path_uuid = file_path_match.group(1)
file_path_date = file_path_match.group(2)
file_path_othr = file_path_match.group(4)

#print(
#	"[DBG]: uuid: " + file_path_uuid + "\n" + 
#	"[DBG]: date: " + file_path_date + "\n" + 
#	"[DBG]: othr: " + file_path_othr + "\n"
#	)

fdate = tdate.strftime('%d.%m.%Y')
if not dir == '':
	if not os.path.exists(dir): os.makedirs(dir)


for itype in issues:
	if not os.path.isfile(dir + itype + "_" + fdate + ".pdf"):
		print('Downloading "' + itype + "_" + fdate + ".pdf ...")
		urllib.urlretrieve (
			'http://epaper.sueddeutsche.de/app/pdfdownload/' + file_path_uuid + '/' + 
			file_path_date + '_' + itype + '_' + file_path_othr + '.pdf',
			dir + itype + "_" + fdate + ".pdf")
		print("Finished download")
	else:
		print(itype + "_" + fdate + ".pdf already downloaded, skipping")

print("All jobs finished!")
