
from lxml import etree
import os
import re
from lxml import html
import codecs
import requests
import os

def stormfrontCrawl():
	entryPoints = ["https://www.stormfront.org/forum/f9-","https://www.stormfront.org/forum/f39-","https://www.stormfront.org/forum/f12-"]
	nPages = [24,66,8501]
	pathOut = "/Users/capitanmartu/Desktop/trainEmbed/stormfront/"
	idThread = 0
	src = "stormfront"
	separator = "\n"
	for idx, entryPoint in enumerate(entryPoints):
		print entryPoint
		i=1	
		url = entryPoint + str(i)+"/"

		while i <= nPages[idx]:
			print "crawling page " + str(i) + " " + url
			page = requests.get(url)
			tree = html.fromstring(page.content)
			linkList = tree.xpath("//td[@class='alt1']/div[not(@class)]/a[contains(@id,'thread_title_')]/@href")
			print len(linkList)
			for link in linkList:
				if os.path.isfile(pathOut+str(idThread)+"_"+src):
					print "already crawled, skipping " +str(idThread)
					idThread+=1
				else:
					j=1
					fd = codecs.open(pathOut+str(idThread)+"_"+src,"w",encoding="utf-8")
					urlBase = link[:-1]
					linkPage = requests.get(link)
					treeLink = html.fromstring(linkPage.content)
					maxPages = treeLink.xpath("//td[@class='alt1']/a[contains(@title,'Last Page') and not(@rel)]/@href")

					if not maxPages:
						maxPages = 1
					else:
						maxPages = maxPages[0].split("-")[1].split("/")[0]
					
					while j <= maxPages:
						urlContent = urlBase+"-"+str(j)+"/"
						contentPage = requests.get(urlContent)
						treeContent = html.fromstring(contentPage.content)
						contentList = treeContent.xpath("//div[contains(@id,'post_message')]/text()")
						contentString = separator.join(contentList)
						fd.write(contentString)
						j+=1

					fd.close()
					idThread+=1
					print "written thread "+str(idThread)
			i+=1
			url = entryPoint + str(i)+"/"


def fatpeoplehateCrawl():
	pass

def niggermaniaCrawl():
	#http://niggermania.net/forum/
	#http://niggermania.net/forum/forumdisplay.php?2-Niggerfuxation-and-TNB/page1219

def vanguardnewsnetworkCrawl():
	#http://www.vanguardnewsnetwork.com/page/711/
	pass

def rooshvCrawl():
	urlBase = "http://www.rooshv.com/page/"
	i = 0
	src = "rooshv"
	idArticle = 0
	pathOut = "/Users/capitanmartu/Desktop/trainEmbed/rooshv/"
	while i < 139:
		print "processing page "+str(i)
		url = urlBase + str(i)
		page = requests.get(url)
		tree = html.fromstring(page.content)
		linkList = tree.xpath("//header[@class='entry-header']/h1[@class='entry-title']/a/@href")
		for link in linkList:
			fd = codecs.open(pathOut+str(idArticle)+"_"+src,"w",encoding="utf-8")
			pageArticle = requests.get(link)
			treeArticle = html.fromstring(pageArticle.content)
			text = treeArticle.xpath("//div[@class='entry-content']/p//text()")
			textString = "\n".join(text)
			fd.write(textString)
			fd.close()
			idArticle+=1
			print "written article "+str(idArticle)
		i+=1

def returnofkingsCrawl():
	urlBase = "http://www.returnofkings.com/page/"
	i = 1
	src = "returnofkings"
	idArticle = 0
	pathOut = "/Users/capitanmartu/Desktop/trainEmbed/returnofkings/"
	
	while i <= 186:
		print "processing page "+str(i)
		url = urlBase + str(i)
		page = requests.get(url)
		tree = html.fromstring(page.content)
		linkList = tree.xpath("//div[@class='cb-meta clearfix']/h2[@class='cb-post-title']/a/@href")
		for link in linkList:
			fd = codecs.open(pathOut+str(idArticle)+"_"+src,"w",encoding="utf-8")
			pageArticle = requests.get(link)
			treeArticle = html.fromstring(pageArticle.content)
			text = treeArticle.xpath("//section[@itemprop='articleBody']//p//text()")
			textString = "\n".join(text)
			fd.write(textString)
			fd.close()
			idArticle+=1
			print "written article "+str(idArticle)
		i+=1



#stormfrontCrawl()
#rooshvCrawl()
returnofkingsCrawl()