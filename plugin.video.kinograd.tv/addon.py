#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, os, json
import xbmcplugin, xbmcgui, xbmcaddon, xbmc

h = int(sys.argv[1])

addon = xbmcaddon.Addon(id='plugin.video.kinograd.tv')
icon = os.path.join( addon.getAddonInfo('path'), "icon.png" )
xbmcplugin.setContent(h, 'movies')

def showMessage(heading, message, times = 5000):
    xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def GET(url):
	try:
		print 'def GET(%s):'%url
		req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		http=response.read()
		response.close()
		return http
	except:
		showMessage('Не могу открыть URL def GET', url)
		return None
	    
def ROOT():
        u = sys.argv[0] + '?mode=genre_film'
        i = xbmcgui.ListItem('Фильмы', iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(h, u, i, True)
        u = sys.argv[0] + '?mode=genre_serial'
        i = xbmcgui.ListItem('Сериалы', iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(h, u, i, True)
        u = sys.argv[0] + '?mode=genre_mult'
        i = xbmcgui.ListItem('Мульты', iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(h, u, i, True)
        u = sys.argv[0] + '?mode=genre_alfavit'
        i = xbmcgui.ListItem('По алфавиту', iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)

def genre_film():
	wurl = 'http://kinograd.tv'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<ul class="sub-menu"><span><div>(.*?)<li class="sub janry-serialov">',re.S).findall(http)
	r2 = re.compile('<a href="(.*?)">(.*?)</a>',re.S).findall(r1[0])
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://kinograd.tv' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)
	
def genre_serial():
	wurl = 'http://kinograd.tv'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<li class="sub janry-serialov">(.*?)<li class="sub janry-multov">',re.S).findall(http)
	r2 = re.compile('<a href="(.*?)">(.*?)</a>',re.S).findall(r1[0])
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://kinograd.tv' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)
        
def genre_mult():
	wurl = 'http://kinograd.tv'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<a href="#">Мульты</a>(.*?)<li><a href="/multfilmy/">',re.S).findall(http)
	r2 = re.compile('<a href="(.*?)">(.*?)</a>',re.S).findall(r1[0])
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://kinograd.tv' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)
		
def genre_alfavit():
	wurl = 'http://kinograd.tv'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<a class="closemb"></a></div><ul class="alfavit">(.*?)<nav><ul><li class="sub janry-filmov">',re.S).findall(http)
	r2 = re.compile('<li><a href="(.*?)" title=".*?">(.*?)</a></li>',re.S).findall(r1[0])
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://kinograd.tv' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)

def OPEN_MOVIES(params):
	http = GET(urllib.unquote_plus(params['url']))#
	ggg = urllib.unquote_plus(params['url'])
	if http == None: return False
	r1 = re.compile('<div id=\'dle-content\'>(.*?)<\/script><script>\(function',re.S).findall(http)
	r2 = re.compile('</a> <a href="([^"]+)" title=".*?">([^<]+)</a></div><div class="modal',re.S).findall(r1[0])
	r3 = re.compile('<img src="(/uploads.*?)" alt="',re.I).findall(r1[0])
	if len(r2) == 0:
		dialog = xbmcgui.Dialog()
		dialog.ok('ВНИМАНИЕ!', 'Нет такой страницы.', 'В этом разделе меньше страниц.')
		return False
	ii = 0
	for href, alt in r2:
			img = 'http://kinograd.tv' + r3[ii]
			ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "utf-8"), iconImage=img, thumbnailImage=img)
			#i.setInfo(type='video', infoLabels={'title': unicode(alt, "cp1251")})
			u  = sys.argv[0] + '?mode=SRAVN'
			u += '&url=%s'%urllib.quote_plus(href)
			u += '&alt=%s'%urllib.quote_plus(alt)
			u += '&img=%s'%urllib.quote_plus(img)
			u += '&ggg=%s'%urllib.quote_plus(ggg)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	try:
		rp2 = re.compile('<div class="nextpg"><span id="page_next"><a href="(http://kinograd.tv.*?/[^/]+/page/([0-9]+)/)">[^<]+</a></span>.*?</div>', re.DOTALL).findall(http)
		for href, nr in rp2:
			u = sys.argv[0] + '?mode=OPEN_MOVIES'
			u += '&url=%s'%urllib.quote_plus(href)
			i = xbmcgui.ListItem('[COLOR yellow]Далее > [/COLOR] %s '%nr, 
                        iconImage='special://home/addons/next.png', 
                        thumbnailImage='special://home/addons/next.png')
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	try:
		rp = re.compile('(http://kinograd.tv.*?/[^/]+/page/)[0-9]+/').findall(href)
		for hr in rp:
			ggg = hr
			u = sys.argv[0] + '?mode=stran'
			u += '&url=%s'%urllib.quote_plus(ggg)
			i = xbmcgui.ListItem('[COLOR ff62ff59]Переход на стр. >[/COLOR]', 
                        iconImage='special://home/addons/next.png', 
                        thumbnailImage='special://home/addons/next.png')
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	xbmcplugin.endOfDirectory(h)

def stran(params):
	http = urllib.unquote_plus(params['url'])
	keyboard = xbmc.Keyboard()
	keyboard.setHeading('Перейти на страницу ...')
	keyboard.doModal()
	if keyboard.isConfirmed():
		query = keyboard.getText()
		url = (http+query+'/')
		OPEN_MOVIES({'url':urllib.quote_plus(url)})
	else:
		return False
  
def SRAVN(params):
	http = urllib.unquote_plus(params['ggg'])
	if http is None:		return False
	if "serial" in http:
		SERII_Sibnet(params)
	else:
		Play_film(params)

def SERII_Sibnet(params):
	http = GET(urllib.unquote_plus(params['url']))
	img = urllib.unquote_plus(params['img'])
	if http == None: return False
	r2 = re.compile('if\(str==\'video_down.*?"keyseek":8,"pl":"([^"]+)"',re.S).findall(http)
	if len(r2) >= 1:
            http = GET(r2[0])
            r2 = re.compile('"comment":"(.*?)","file":"(.*?)"',re.S).findall(http)
	for name, href in r2:
		img = urllib.unquote_plus(params['img'])
		i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=img, thumbnailImage=img)
		u  = sys.argv[0] + '?mode=SRAVN2'
		u += '&url=%s'%urllib.quote_plus(href)
		u += '&name=%s'%urllib.quote_plus(name)
		u += '&img=%s'%urllib.quote_plus(img)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)

def SRAVN2(params):
	http = urllib.unquote_plus(params['url'])
	if http is None:		return False
	if "youtube" in http:
		You_play(params)
	else:
		PLAY(params)
	
def Play_film(params):
	http = GET(urllib.unquote_plus(params['url']))
	img = urllib.unquote_plus(params['img'])
	alt = urllib.unquote_plus(params['alt'])
	if http == None: return False
	r2 = re.compile('file:"(.*?)"',re.S).findall(http)
	for names in r2:
                i = xbmcgui.ListItem(unicode(alt, "utf-8"), iconImage=img, thumbnailImage=img)
                i.setProperty("IsPlayable","true")
                pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                pl.clear()
                pl.add(names, i)
                xbmc.Player().play(pl)

def PLAY(params):
        http = urllib.unquote_plus(params['url'])
        img = urllib.unquote_plus(params['img'])
        name = urllib.unquote_plus(params['name'])
        if http == None: return False
        i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=img, thumbnailImage=img)
        xbmc.Player().play(http, i)
   
def You_play(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	match = re.compile('rel="canonical" href="https?://www.youtube.com/watch\?v=(.*?)">').findall(http)
        you_tube='plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s'%match[0]
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(you_tube)
        xbmc.Player().play(pl)
   
def get_params(paramstring):
	param=[]
	if len(paramstring)>=2:
		params=paramstring
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params=get_params(sys.argv[2])


mode = None

try:
	mode = urllib.unquote_plus(params['mode'])
except:
	ROOT()

if mode == 'OPEN_MOVIES': OPEN_MOVIES(params)
if mode == 'ROOT': ROOT()
if mode == 'SERII_Sibnet': SERII_Sibnet(params)
if mode == 'You_play': You_play(params)
if mode == 'genre_film': genre_film()
if mode == 'genre_serial': genre_serial()
if mode == 'genre_mult': genre_mult()
if mode == 'genre_alfavit': genre_alfavit()
if mode == 'PLAY': PLAY(params)
if mode == 'SRAVN': SRAVN(params)
if mode == 'SRAVN2': SRAVN2(params)
if mode == 'Play_film': Play_film(params)
if mode == 'stran': stran(params)