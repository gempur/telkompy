import pycurl
import json
# import numpy
# from pprint import pprint
from io import BytesIO
from urllib.parse import urlencode
from bs4 import  BeautifulSoup

username = 'userlogin_di_mytelkom'
password = 'password' 

#init pycurl
def init_curl():
	c = pycurl.Curl()
	return c

#close pycurl
def close_curl(c):
	c.close()

#login POST. set cookie
def login_post(c,url,data):
	buffer = BytesIO()
	c.setopt(c.URL, url)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.COOKIEJAR, './cookie.txt')
	c.setopt(c.COOKIEFILE, './cookie.txt')
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	body = buffer.getvalue().decode('utf-8')
	return body

#POST 
def post_url(c,url,data):
	buffer = BytesIO()
	c.setopt(c.URL, url)
	c.setopt(c.POSTFIELDS, data)
	c.setopt(c.COOKIEFILE, './cookie.txt')
	c.setopt(c.WRITEDATA, buffer)
	c.perform()

	body = buffer.getvalue().decode('utf-8')
	return body

#GET
def get_url(c,url):
	buffer = BytesIO()
	c.setopt(c.URL, url)
	c.setopt(c.COOKIEJAR, './cookie.txt')
	c.setopt(c.COOKIEFILE, './cookie.txt')
	c.setopt(c.WRITEDATA, buffer)
	c.perform()

	body = buffer.getvalue().decode('utf-8')
	return body

#ambil nomor akun pelanggan
def get_number_pel(c):
	j=[]
	postdata = {'lid':'0'}
	postfields = urlencode(postdata)
	data = post_url(c,'https://my.telkom.co.id/ajax/_ajax4.php?act=getdashboard',postfields)
	data = json.loads(data)
	data = (data['data'])

	soup = BeautifulSoup(data,'html.parser')

	for i in soup.find('div',{'id':'acc_1'}).findAll('p'):
		j.append(i.b.text)

	for i in soup.find('div',{'id':'acc_2'}).findAll('p'):
		j.append(i.b.text)
	
	return j

#fungsi tanggal, bulan dan tahun
def tgl(data):
	bulans=['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','Nopember','Desember']
	a= data.split()
	m = bulans.index(a[1]) + 1
	tgl=[m,int(a[2])]
	return tgl

#cek biaya
def cekbiaya(billdate):
	postdata = {'act':'do',
	'for':'1',
	'src':'',
	'signinusername':username,
	'signinpassword':password}
	postfields = urlencode(postdata)

	c = init_curl()
	login_post(c,'https://my.telkom.co.id/login.php',postfields)
	number_pel = get_number_pel(c)
	#number_pel = [u'054841388', u'054841332', u'0541765275']
	nopel = number_pel
	k=[]
	iter = 0
	for i in nopel:
		url = 'https://my.telkom.co.id/dashboard/billing.php?phone='+ i +'&billdate='+billdate
		res = get_url(c,url)
		soup = BeautifulSoup(res,'html.parser')
		tanggal=tgl(soup.find('div',{'id':'bil-dv1'}).text)
		k.append(iter)
		k[iter]=[]
		k[iter].append(tanggal)
		k[iter].append(i)
		l=[]
		n=[]
		count = 0
		for row in soup.find('table',{'class':'tbl_detail'}).findAll('td'):
			
			if count == 0:
				m=[]
				m.append(row.text)
				count = 1
			else:
				item = row.text
				item = item.replace('.',u'')
				item = item.replace(u'\xa0','0')
				if item.isdigit(): item= int(item)
				else: item=item
				m.append(item)
				count =  0
				n.append(m)
		k[iter].append(n)
		iter=iter+1
	return k

	close_curl(c)

#cetak
def listbiaya(data):
	s=[]
	for i in data:
		for j in i[2]:
			b=[]
			b.append(i[0][1])
			b.append(i[0][0])
			b.append(i[1])
			b.append(j[0])
			b.append(j[1])
			# print(b)
			s.append(b)
	return(s)

print(listbiaya(cekbiaya('201512')))

# a='aaa'
# if a.isdigit(): print int(a)
# else: print a
