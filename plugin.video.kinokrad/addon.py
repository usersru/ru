#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, re, xbmc, xbmcgui, xbmcplugin, os, urllib, urllib2, xbmcaddon

h = int(sys.argv[1])

addon = xbmcaddon.Addon(id='plugin.video.kinokrad')
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
		
def DEC(s):
	s=s.decode('utf-8').encode('windows-1251')
	return s
		
def genre():
	wurl = 'http://kinokrad-net.ru/'
	http = GET(wurl).replace('" class="supergroup','')
	if http == None: return False#<div class="lefttitle" style="padding-top:15px;">
	r1 = re.compile('<li><a href="\/">.+?</a></li>(.*?)<div class="leftbox-comm-ind">',re.S).findall(http)
	r2 = re.compile('<li><a href="([^"]+)">(.*?)</a></li>',re.S).findall(r1[0].replace('<b>','').replace('</b>','').replace('</font>','').replace('<font color="#008aff">','').replace('<font color="#ff0000">',''))
	if len(r2) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'Нет элементов id,name,link,numberOfMovies')
		return False
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "windows-1251"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://kinokrad-net.ru' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	
	xbmcplugin.endOfDirectory(h)

def OPEN_MOVIES(params):
	http = GET(urllib.unquote_plus(params['url']))#.replace('Вперед','')
	if http == None: return False
	r1 = re.compile('<div id=\'dle-content\'>(.*?)<div class="ftrbox"',re.S).findall(http)
	r2 = re.compile('<a href="([^"]+)"><img title=".*?" alt="(.*?)" class="postr" src="(.*?)" height=',re.S).findall(r1[0])
	r4 = re.compile('<div class="shorttext">(.*?)</div>',re.S).findall(http)
	if len(r2) == 0:
		dialog = xbmcgui.Dialog()
		dialog.ok('ВНИМАНИЕ!', 'Нет такой страницы.', 'В этом разделе меньше страниц.')
		return False
	ii = 0
	for href, alt, img in r2:
			text = r4[ii]
			ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
			i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
			u  = sys.argv[0] + '?mode=SRAVN'
			u += '&url=%s'%urllib.quote_plus(href)
			u += '&alt=%s'%urllib.quote_plus(alt)
			u += '&img=%s'%urllib.quote_plus(img)
			u += '&text=%s'%urllib.quote_plus(text)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	try:
		rp = re.compile('<span class="nav_ext">(.*?)\s+<div class="clr"></div>', re.DOTALL).findall(http)[0]
		rp2 = re.compile('<a href="(.*?page/([0-9]+)/)"><span class="navnext">.*?</span></a>').findall(rp)
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
		rp = re.compile('(.*?page/)([0-9]+)/').findall(href)
		for hr in rp:
			ggg = hr[0]
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
		url = (http+query)
		OPEN_MOVIES({'url':urllib.quote_plus(url)})
	else:
		return False

def SRAVN(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http is None:		return False
	rows1 = re.compile('<param name="flashvars" value="comment=.*?&amp;st=.*?txt&amp;pl=(.*?)&amp;poster=').findall(http)
	if len(rows1) >= 1:
		SERII(params)
	else:
		PLAY(params)
	
def SERII(params):
	alt = urllib.unquote_plus(params['alt'])
	img = urllib.unquote_plus(params['img'])
	http = GET(urllib.unquote_plus(params['url']))
	text = urllib.unquote_plus(params['text'])
	r2 = re.compile('<param name="flashvars" value="comment=.*?&amp;st=.*?txt&amp;pl=(.*?)&amp;poster=',re.S).findall(http)
	if len(r2) >= 1:
            http = GET(r2[0]).replace('\n','').replace('"playlist":[','').replace('"comment":"','   ').replace('",',' ').replace('{','')
            r2 = re.compile('   (.*?) "file":"(.*?)"', re.MULTILINE|re.DOTALL).findall(http)
	if len(r2) == 0:
		showMessage('ПОКАЗАТЬ НЕЧЕГО', 'НА САЙТЕ НЕТ ФИЛЬМА')
		return False
	for name, href in r2:
		name = re.sub('<br>.+?[^ ]+','', name)
		i = xbmcgui.ListItem(unicode(name, "utf-8"), iconImage=img, thumbnailImage=img)
		u  = sys.argv[0] + '?mode=PLAY_Serii'
		u += '&img=%s'%urllib.quote_plus(img)
		u += '&url=%s'%urllib.quote_plus(href)
		u += '&alt=%s'%urllib.quote_plus(alt)
		u += '&name=%s'%urllib.quote_plus(name)
		u += '&text=%s'%urllib.quote_plus(text)
		xbmcplugin.addDirectoryItem(h, u, i, True)
        xbmcplugin.endOfDirectory(h)
	
def PLAY(params):
	http = GET(urllib.unquote_plus(params['url']))
	r2 = re.compile('<iframe height="[0-9]+" width="[0-9]+" frameborder="[0-9]+" src="(.*?)" scrolling="no"></iframe>',re.S).findall(http)
	if len(r2) == 0:
		dialog = xbmcgui.Dialog()
		dialog.ok('[COLOR yellow]ВНИМАНИЕ![/COLOR]', ' ', 'НЕТ ТАКОГО ФИЛЬМА.')
		return False
	if len(r2) >= 1:
            http = GET(r2[0])
            r2 = re.compile('m:"video",uid:"videoplayer[0-9]+",file:"(.*?)"',re.S).findall(http)
	for names in r2:
		img = urllib.unquote_plus(params['img'])
		alt = urllib.unquote_plus(params['alt'])
		text = urllib.unquote_plus(params['text'])
		i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
		i.setProperty("IsPlayable","true")
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		pl.add(names, i)
		xbmc.Player().play(pl)
	
def PLAY_Serii(params):
		http = urllib.unquote_plus(params['url'])
		name = urllib.unquote_plus(params['name'])
		text = urllib.unquote_plus(params['text'])
		alt = urllib.unquote_plus(params['alt'])
		img = urllib.unquote_plus(params['img'])
		i = xbmcgui.ListItem(unicode(alt+'   '+DEC(name), "windows-1251"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt+'   '+DEC(name), "windows-1251"), 'plot': unicode(text, "windows-1251")})
		i.setProperty("IsPlayable","true")
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		pl.add(http, i)
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
	genre()

if mode == 'OPEN_MOVIES': OPEN_MOVIES(params)
if mode == 'SERII': SERII(params)
if mode == 'genre': genre()
if mode == 'PLAY': PLAY(params)
if mode == 'PLAY_Serii': PLAY_Serii(params)
if mode == 'SRAVN': SRAVN(params)
if mode == 'stran': stran(params)