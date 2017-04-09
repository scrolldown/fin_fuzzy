from django.shortcuts import render 
# Create your views here
from django.http import HttpResponse
def main_page(request):
	output='''
		<html>
		<head><title>%s</title></head>
		<body>
			<h1>%s</h1>
			<p>%s</p>
		</body>
		</html>
		''' %('Django TEST','Welcome to Django','Hello World!'
		)
	return HttpResponse(output) 
