import sys
import os.path
import uuid
from glob import glob
from datetime import datetime
import cgi, cgitb

class HttpServer:
	def __init__(self):
		self.sessions={}
		self.types={}
		self.types['.pdf']='application/pdf'
		self.types['.jpg']='image/jpeg'
		self.types['.txt']='text/plain'
		self.types['.html']='text/html'

	def response(self,kode=404,message='Not Found',messagebody='',headers={}):
		tanggal = datetime.now().strftime('%c')
		resp=[]
		resp.append("HTTP/1.0 {} {}\r\n" . format(kode,message))
		resp.append("Date: {}\r\n" . format(tanggal))
		resp.append("Connection: close\r\n")
		resp.append("Server: myserver/1.0\r\n")
		resp.append("Content-Length: {}\r\n" . format(len(messagebody)))
		for kk in headers:
			resp.append("{}:{}\r\n" . format(kk,headers[kk]))
		resp.append("\r\n")
		resp.append("{}" . format(messagebody))
		response_str=''
		for i in resp:
			response_str="{}{}" . format(response_str,i)
		return response_str

	def proses(self,data):
		requests = data.split("\r\n")
		baris = requests[0]
		all_headers = [n for n in requests[1:] if n!='']
		j = baris.split(" ")
		try:
			method=j[0].upper().strip()
			if (method=='GET'):
				object_address = j[1].strip()
				return self.http_get(object_address, all_headers)
			if (method=='POST'):
				line_form = requests[18].split("=")
				isi_form = line_form[1]
				object_address = j[1].strip()
				return self.http_post(object_address, all_headers,isi_form)
			else:
				return self.response(400,'Bad Request','',{})
		except IndexError:
			return self.response(400,'Bad Request','',{})

	def http_get(self,object_address,headers):
		if object_address=='/sending.html':
			object_address = object_address.replace('/', '')
			fp = open(object_address, 'r')
			isi = fp.read()
		else:
			isi = object_address[1:]
		headers={}
		headers['Content-type']= "text/html"
		return self.response(200,'OK',isi,headers)

	def http_post(self,object_address,headers,isi_form):
		head = headers
		headers ={}
		# isi = "kosong"
		k ="\n"
		for atribut in head:
		    k = k+atribut+"\n"
		isi = "a.Header : \n" + k + "\nb.Isi Form : \n\n" + isi_form
		return self.response(200,'OK',isi,headers)