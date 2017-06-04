#!/usr/bin/python

from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re

def No_of_products(value):
	
		# Counting number of products in each page
		Elements = value.find('div',{'id' : 'searchResultsContainer'})
		
		count=0
		
		E = Elements('div',{'class' : re.compile('.*grid.*')})
		
		for i in E:
			count+=1
		
		return count/3.0

if len(sys.argv) == 2:

	# WebDriver is a PhantomJS browser object
	WebDriver = webdriver.PhantomJS()

	# Based on the Query keyword given in the command line arguments!, open the Web page to find all it's products
	WebDriver.get("http://shopping.com/products?KW="+sys.argv[1])

	# Get the source code of the page and create a BeautifulSoup parser object with it
	Value = BeautifulSoup(WebDriver.page_source,"html.parser")

	# Count the number of products present in the that page
	Count_per_page = No_of_products(Value)

	# The pagination concept of moving to next pages!
	Value1 = Value.find('div',{'class','paginationNew'})
	
	Page_count = 1
	
	#Getting Total number of Pages using PaginationNew 
	for t in Value1.find_all('a'):
		if t.text.replace(" ","").isdigit():
			Page_count = t.text.replace(" ","")

	# Check the number of items in the last page
	WebDriver.get("http://www.shopping.com/products~PG-"+str(Page_count)+"?KW="+sys.argv[1])
	
	Value = BeautifulSoup(WebDriver.page_source,"html.parser")
	
	Last_page_items = No_of_products(Value)

	# Therefore, Total #of products= (Products per page * No of pages -1) + (Products on last page)
	print "Total Number of Products =>", (int((int(Page_count) - 1))*int(Count_per_page)) + int(Last_page_items)
	
	WebDriver.quit()

else:

	WebDriver = webdriver.PhantomJS()
	
	# Check the number of products in the current page
	WebDriver.get("http://www.shopping.com/products~PG-"+sys.argv[2]+"?KW="+sys.argv[1])
	
	Value = BeautifulSoup(WebDriver.page_source,"html.parser")
	
	Last_page_items = No_of_products(Value)
	
	print "Total Number of Products in Page",sys.argv[2],"=>",int(Last_page_items)
	
	WebDriver.quit()
