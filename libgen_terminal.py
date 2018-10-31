from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import urllib.request
import os

#Return soup of the url.
def page_soup(url):
	driver.get(url)
	html = driver.page_source
	s = BeautifulSoup(html,'html.parser')
	return s


search_url = "http://gen.lib.rus.ec/search.php?req="
file_url = 'http://lib1.org/_ads/'
counter = 1
books_dict = {}
book = input("Enter book you want to search:")


#Headless mode for firefox.
options = Options()
options.headless = True
driver = webdriver.Firefox(firefox_options=options)

#Creating search string.
if len(book.split()) > 1:
	for item in book.split():
		search_url += item + "+"
else:
	search_url += book


soup = page_soup(search_url)
table = soup.find(class_="c")
table_body = table.find('tbody')


#Getting all the items.
for item in table_body.find_all('tr')[1:]:
	author = item.find_all('td')[1].text
	publisher = item.find_all('td')[3].text
	year = item.find_all('td')[4].text
	pages = item.find_all('td')[5].text
	language = item.find_all('td')[6].text
	size = item.find_all('td')[7].text
	extension = item.find_all('td')[8].text
	file_name = item.find_all('td')[2].text
	books_dict[counter] = [author,publisher,year,pages,language,size,extension,item.find_all('td')[2].a.get('href')]
	print("[%s] %s (%s)" % (counter,file_name,extension))
	counter += 1

#If it didn't go through the loop it means that it couldn't find any books on the page.
if counter == 1:
	print("Couldn't find any book.")
	driver.close()
	quit()


book = int(input("What book to you want to download?\n?>"))
os.system('clear')

#Extra info regarding the book.
choice = input("Do you want to see more info about the file?[y/n]")
while choice != 'Y' or choice != 'y' or choice != 'n' or choice != 'N':
	if choice == 'Y' or choice == 'y': 
		print("Author:",books_dict[book][0])
		print("Publisher:",books_dict[book][1])
		print("Year:",books_dict[book][2])
		print("Pages:",books_dict[book][3])
		print("Language:",books_dict[book][4])
		print("Size:",books_dict[book][5])
		break
	elif choice == 'N' or choice == 'n':
		break
	else:
		print("Wrong.")
	choice = input("Do you want to see more info about the file?[Y/N]")

		
#Asking whether to continue or not.
choice = input("Continue to download the file?[Y/N]:")
while choice != 'Y' or choice != 'y' or choice != 'N' or choice != 'n':
	if choice == 'N' or choice == 'n':
		print("Quiting...")
		driver.close()
		quit()
	elif choice == 'Y' or choice == 'y':
		break
	else:
		print("Wrong.")
	choice = input(">>>")

#Downloading the file.
print("Downloading the file...")
file_name = books_dict[book][-1]
soup = page_soup(file_url+file_name[19:])
urllib.request.urlretrieve(soup.find(id="info").a.get('href'),soup.find(id="info").h1.text+'.'+books_dict[book][-2])
driver.close()