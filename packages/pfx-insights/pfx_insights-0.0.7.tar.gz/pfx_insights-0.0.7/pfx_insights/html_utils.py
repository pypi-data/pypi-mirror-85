import string
import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
import unicodedata
import io
from PyPDF2 import PdfFileReader
import gzip
from . import text_utils

class HtmlProcessor:
	def __init__(self,
				user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
				tags_to_retrieve = None,
				command_timeout = 100
			):
		self.user_agent = user_agent
		self.tx_utils = text_utils.TextUtils()
		self.tags_to_retrieve = tags_to_retrieve
		self.command_timeout = command_timeout

	def __is_tag_visible(self, element):
		if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
			return False
		if isinstance(element, Comment):
			return False
		return True

	def text_from_url(self, url_to_parse, fetch_page_links = False):
		try:
			#set request header for the destination to consider this as a valid browser
			req = urllib.request.Request(url_to_parse, data=None, headers={'User-Agent': self.user_agent})
			url = urllib.request.urlopen(req, timeout=self.command_timeout)
			
			content_type = url.getheader("Content-Type").split(';')[0]
			if content_type == "text/html":
				return self.__text_from_html(url, fetch_page_links)
			elif content_type == "application/pdf":
				return self.__text_from_pdf(url)
			else:
				raise Exception(str.format('Unsupported content type in url: {0}', url_to_parse))

		except Exception as e:
			print(e)
			if fetch_page_links == True:
				return "", "", []
			else:
				return "", ""
				
	def __text_from_pdf(self, url, fetch_page_links):
		fileContents = url.read()
		memoryStream = io.BytesIO(fileContents)
		pdfFile = PdfFileReader(memoryStream)
		
		extracted_text = ""
		numPages = pdfFile.getNumPages()
		for i in range(0, numPages - 1):
			pdfPage = pdfFile.getPage(i)
			extracted_text += pdfPage.extractText()

		if fetch_page_links == True:
			return self.tx_utils.encode_text(""), self.tx_utils.encode_text(extracted_text), []
		else:
			return self.tx_utils.encode_text(""), self.tx_utils.encode_text(extracted_text)

	def __text_from_html(self, url, fetch_page_links):
		body = url.read()
		if url.info().get('Content-Encoding') == 'gzip':
			body = gzip.decompress(body)

		return self.process_html(body, fetch_page_links)

	def __clean_whitespace(self, doc):
		cleaned_doc = doc.replace("\t"," ")
		cleaned_doc = cleaned_doc.replace("\r"," ")
		cleaned_doc = cleaned_doc.replace("\n"," ")

		return cleaned_doc

	def __get_link_from_href(self, link):
		if 'href' in link.attrs and link.attrs['href'].startswith("http"):
			return link.attrs['href']

		return ""

	def process_html(self, body, fetch_page_links = False):
		soup = BeautifulSoup(body, 'html.parser')
		
		#strip out script tags since they are noise
		[s.extract() for s in soup('script')]
		[s.extract() for s in soup('noscript')]
		
		extracted_text = ""
		page_urls = {}
		if self.tags_to_retrieve != None and len(self.tags_to_retrieve) > 0:
			list_text = []			
			for tag in self.tags_to_retrieve:
				for link in soup.find_all(tag):
					raw_text = link.get_text(" ")
		
					raw_text = self.__clean_whitespace(raw_text)
					list_text.append(raw_text)
					
					if fetch_page_links == True:
						page_links = link.findAll("a")
						for page_link in page_links:
							link = self.__get_link_from_href(page_link)
							if len(link) > 0 and link not in page_urls:
									page_urls[link] = 1
			
			extracted_text = ' '.join(list_text)
		else:		
			#visible text
			visible_text = soup.findAll(text=True)
			visible_texts = filter(self.__is_tag_visible, visible_text)
			extracted_text = u" ".join(t.strip() for t in visible_texts)
			extracted_text = self.__clean_whitespace(extracted_text)
   
			if fetch_page_links == True:
				page_links = soup.findAll("a")
				for page_link in page_links:
					link = self.__get_link_from_href(page_link)
					if len(link) > 0 and link not in page_urls:
							page_urls[link] = 1

		#page title 
		title = soup.title
		if title == None:
			title = ""
		else:
			title = title.string
		
		if extracted_text == None:
			extracted_text = ""
		else:
			pass

		if fetch_page_links == True:
			return self.tx_utils.encode_text(title), self.tx_utils.encode_text(extracted_text), list(page_urls.keys())
		else:
			return self.tx_utils.encode_text(title), self.tx_utils.encode_text(extracted_text)