#!//usr/bin/python
## KPSU "Podcast" to actual Podcast generator
## created for http://www.kpsu.org/category/static-and-distance/
##
## by Daniel Agans
##

##### Define config items:
## Main Site URL
mainpage = 'http://www.kpsu.org/category/static-and-distance/'
## Prefix of link to child pages
linkloc = 'http://www.kpsu.org/static-and-distance/'
casteremail = 'joshuarjustice@gmail.com'
castername = 'Joshua Justice'
castimage = 'http://staticdistance.com/wp-content/uploads/2014/07/header_web.jpg'
XMLURL = 'http://hell.if.i.know'
iCategory = 'Music'
iSubCat = 'Alternative'
keywords = 'music, josh, farts, feces'

import urllib2, html5lib, re, datetime, os

Links, Headings, Subtitles, Descriptions, URLs, MP3s, Episode = ([] for i in range(7)) ## init lists

urlobject = urllib2.urlopen(mainpage)    ## "open" the URL
root_response = urlobject.read()         ## place contents to variable root_response
responses = root_response.splitlines( ); ## split into lines for easy consumption
Breaker = '\n        '

for response in responses:   ## iterate for each line of the HTML document
  if 'og:title' in response:                     ## get the title of the podcast
    TitleLine = response.split('content="')
    Title = (TitleLine[1].split(' - KPSU"'))[0]
  if 'og:description' in response:
    DescLine = response.split('content="')
    Description = (DescLine[1].split('" />'))[0]
  if linkloc in response:      ## only worry about lines that actually have links we care about
    LinkLine = response.split('<a href="')   ## cut the link into 2, so list[1] contains link
    Link = LinkLine[1].split('" rel')        ## cut the stuff after the link off, so that list[0] is the link
    urlobject2 = urllib2.urlopen(Link[0])    ## open the URL that we pulled, to traverse that page in the loop
    root2 = urlobject2.read()                ## put the content into a variable for processing
    responses2 = root2.splitlines( );        ## split that into lines for easier processing
    for secondary in responses2:                      ## initiate looping each line
       if 'og:title' in secondary:                    ## og:title is the line with title
         secondary = secondary.split('content="')
         secondary = secondary[1].split(' - KPSU"')
         Headings.append(secondary[0])
       if 'og:description' in secondary:              ## og:description holds the short description
         secondary = secondary.split('content="')
         Descriptions.append(secondary[1])
       if 'og:url' in secondary:                   ## og:url holds the page URL.  Not sure if this is useful yet
         secondary = secondary.split('content="')
         secondary = secondary[1].split('" />')
         URLs.append(secondary[0])
       if 'Click here to download' in secondary:   ## the important one.  The mp3 link
         secondary = secondary.split('href="')
         secondary = secondary[1].split('"a class="count"')
         MP3s.append(secondary[0])

## Pull in the template and then split out the 'item' section so we can loop
XMLTemplate = open('podcast.template', 'r').read()   ## pull the podcast template into string
XMLTemplate = XMLTemplate.split('^-^')

##substitute the values into the template.  This section dealing only with non-episode
XMLTemplate[0] = XMLTemplate[0].replace('%mainpage%', mainpage)
XMLTemplate[0] = XMLTemplate[0].replace('%casteremail%', casteremail)
XMLTemplate[0] = XMLTemplate[0].replace('%castername%', castername)
XMLTemplate[0] = XMLTemplate[0].replace('%castimage%', castimage)
XMLTemplate[0] = XMLTemplate[0].replace('%title%', Title)
XMLTemplate[0] = XMLTemplate[0].replace('%iCategory%', iCategory)
XMLTemplate[0] = XMLTemplate[0].replace('%iSubCat%', iSubCat)
XMLTemplate[0] = XMLTemplate[0].replace('%description%', Description)
XMLTemplate[0] = XMLTemplate[0].replace('%xmlurl%', XMLURL)
XMLTemplate[0] = XMLTemplate[0].replace('%keywords%', keywords)

##iterate for each article and substitute the proper values
i = 0
while i < len(Headings):
  Episode.append(XMLTemplate[1])  ## copy the template to a variable
  Episode[i] = Episode[i].replace('!title!', Headings[i])
  Episode[i] = Episode[i].replace('!description!', Descriptions[i])
  Episode[i] = Episode[i].replace('!mp3url!', MP3s[i])
  Episode[i] = Episode[i] + Breaker
  i+=1

Eps = ''.join(Episode) ## flatten Episode into a single string
XMLGen = XMLTemplate[0] + Breaker + Eps + Breaker + XMLTemplate[2] ## Put the parts back together
print(XMLGen) ## Output

Podcast = open('Podcast.xml', 'w+')

Podcast.close()

