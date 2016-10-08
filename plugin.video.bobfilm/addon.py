#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, os, json
import xbmcplugin, xbmcgui, xbmcaddon, xbmc

h = int(sys.argv[1])

addon = xbmcaddon.Addon(id='plugin.video.bobfilm')
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
        u = sys.argv[0] + '?mode=search'
        i = xbmcgui.ListItem('[ ПОИСК ]', iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(h, u, i, True)
	wurl = 'http://bobfilm1.net'
	http = GET(wurl).replace('</span></a></a></li>','</span></a></li>').replace('<span class="boldund">','')
	if http == None: return False
	r1 = re.compile('<div class="bl_top">(.*?)</div>',re.S).findall(http.replace('><span class="und"','').replace('</span>',''))
	r2 = re.compile('<li><a href="(.*?)">(.*?)</a></li>',re.S).findall(r1[0])
	del r2[21]
	del r2[20]
	del r2[17]
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "windows-1251"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://bobfilm1.net' + href)
		u += '&name=%s'%urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)

def search(params):
	keyboard = xbmc.Keyboard()
	keyboard.setHeading('Что ищем?')
	keyboard.doModal()
	if keyboard.isConfirmed():
		query = keyboard.getText()
                query = re.sub(r' ','+', query)
                query = re.sub(r'а','%E0', query)
                query = re.sub(r'б','%E1', query)
                query = re.sub(r'в','%E2', query)
                query = re.sub(r'г','%E3', query)
                query = re.sub(r'д','%E4', query)
                query = re.sub(r'е','%E5', query)
                query = re.sub(r'ж','%E6', query)
                query = re.sub(r'з','%E7', query)
                query = re.sub(r'и','%E8', query)
                query = re.sub(r'й','%E9', query)
                query = re.sub(r'к','%EA', query)
                query = re.sub(r'л','%EB', query)
                query = re.sub(r'м','%EC', query)
                query = re.sub(r'н','%ED', query)
                query = re.sub(r'о','%EE', query)
                query = re.sub(r'п','%EF', query)
                query = re.sub(r'р','%F0', query)
                query = re.sub(r'с','%F1', query)
                query = re.sub(r'т','%F2', query)
                query = re.sub(r'у','%F3', query)
                query = re.sub(r'ф','%F4', query)
                query = re.sub(r'х','%F5', query)
                query = re.sub(r'ц','%F6', query)
                query = re.sub(r'ч','%F7', query)
                query = re.sub(r'ш','%F8', query)
                query = re.sub(r'щ','%F9', query)
                query = re.sub(r'ы','%FB', query)
                query = re.sub(r'э','%FD', query)
                query = re.sub(r'ю','%FE', query)
                query = re.sub(r'я','%FF', query)
                query = re.sub(r'ё','%B8', query)
                query = re.sub(r'ь','%FC', query)
                query = re.sub(r'ъ','%FA', query)
		url = ('http://bobfilm1.net/?do=search&subaction=search&story='+query)
		MOVIES_search({'url':urllib.quote_plus(url)})
	else:
		return False
	
def OPEN_MOVIES(params):
	try:
		http = GET(urllib.unquote_plus(params['url'])).replace('\'','"')
		page_s = urllib.unquote_plus(params['url'])
		if http == None: return False
		r2 = re.compile('<div class="sh3"><a href="([^"]+)">.*?</a></div>.*?<img src="(.*?)".*?alt=".*?title="([^"]+)"',re.S).findall(http)
		#r4 = re.compile('<div id="news-id-[0-9]+" style="display:inline;">(.*?)</div>',re.S).findall(http)
		r4 = re.compile('<div class="shortdisc">(.*?)</div>',re.S).findall(http)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok('ВНИМАНИЕ!', 'Нет такой страницы.', 'В этом разделе меньше страниц.')
	ii = 0
	for href, img, alt in r2:
			text = r4[ii]
			img='http://bobfilm1.net'+img
			ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
			i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
			u  = sys.argv[0] + '?mode=SRAVN'
			u += '&url=%s'%urllib.quote_plus(href)
			u += '&img=%s'%urllib.quote_plus(img)
			u += '&alt=%s'%urllib.quote_plus(alt)
			u += '&text=%s'%urllib.quote_plus(text)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	try:
		rp = re.compile('<div class="pagination">(.*?)</div>', re.DOTALL).findall(http)[0]
		rp2 = re.compile('<a href="(.*?)" class="page_btn next_page">(.*?)</a>').findall(rp)
		for href, nr in rp2:
			u = sys.argv[0] + '?mode=OPEN_MOVIES'
			u += '&url=%s'%urllib.quote_plus(href)
			i = xbmcgui.ListItem('[COLOR yellow]Далее >[/COLOR] %s '%nr, iconImage='special://home/addons/next.png', thumbnailImage='special://home/addons/next.png')
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	try:
		rp = re.findall('(http://bobfilm1\.net.*?/page/)([0-9]+)', page_s)
		for hr in rp:
			ggg = str(hr[0])
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
    
def Play_kino(params):#фильм готово
	img = urllib.unquote_plus(params['img'])
	alt = urllib.unquote_plus(params['alt'])
	text = urllib.unquote_plus(params['text'])
	http = GET(urllib.unquote_plus(params['url'])).replace('pl=/pl/','pl=http://bobfilm1.net/pl/')
	if http == None: return False
	r2 = re.compile('pl=(.*?txt)" />',re.S).findall(http)
	if len(r2) >= 1:
            http = GET(r2[0])
            r2 = re.compile('"comment":".+?obfilm","file":"([^"]+)"',re.S).findall(http)
	for name in r2:
		i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
		i.setProperty("IsPlayable","true")
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		pl.add(name, i)
		xbmc.Player().play(pl)
    
def SERII(params):#серии готово
	http = GET(urllib.unquote_plus(params['url']))
	r2 = re.compile('pl=(.*?txt)" />',re.S).findall(http.replace('pl=/','pl=http://bobfilm1.net/'))
	if len(r2) >= 1:
            http = GET(r2[0])
            r2 = re.compile('"comment":"([^"]+)","file":"([^"]+)"',re.S).findall(http)
	for name, href in r2:
		img = urllib.unquote_plus(params['img'])
		alt = urllib.unquote_plus(params['alt'])
		text = urllib.unquote_plus(params['text'])
		i = xbmcgui.ListItem(unicode(DEC(name)+'    '+alt, "windows-1251"), iconImage=img, thumbnailImage=img)
		u  = sys.argv[0] + '?mode=PLAY'
		u += '&img=%s'%urllib.quote_plus(img)
		u += '&url=%s'%urllib.quote_plus(href)
		u += '&alt=%s'%urllib.quote_plus(alt)
		u += '&name=%s'%urllib.quote_plus(name)
		u += '&text=%s'%urllib.quote_plus(text)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)

def MOVIES_search(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	r2 = re.compile('<div class="postershort"><a href="(.*?)" ><\!--dle_image_begin:.*?\|--><img src="(.*?)" alt=".*?" title="(.*?)"  /><\!--dle_image_end--></a></div>',re.S).findall(http)
	#r4 = re.compile('<span style="font-size:12pt;"><!--/sizestart-->(.*?)<!--sizeend--></span><!--/sizeend--></div>',re.S).findall(http)
	#ii = 0
	for href, img, alt in r2:
			text = alt
			img = 'http://bobfilm1.net'+img
			#ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
			#i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
			u  = sys.argv[0] + '?mode=SRAVN'
			u += '&url=%s'%urllib.quote_plus(href)
			u += '&img=%s'%urllib.quote_plus(img)
			u += '&alt=%s'%urllib.quote_plus(alt)
			u += '&text=%s'%urllib.quote_plus(text)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	try:
		rp = re.compile('<div class="pagination">(.*?)</div>', re.DOTALL).findall(http)[0]
		rp2 = re.compile('<a href="(.*?)" class="page_btn next_page">(.*?)</a>').findall(rp)
		for href, nr in rp2:
			u = sys.argv[0] + '?mode=MOVIES_search'
			u += '&url=%s'%urllib.quote_plus(href)
			i = xbmcgui.ListItem('[COLOR yellow]Далее >[/COLOR] %s '%nr, iconImage='special://home/addons/next.png', thumbnailImage='special://home/addons/next.png')
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	xbmcplugin.endOfDirectory(h)
	
def SRAVN(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http is None:		return False
	rows1 = re.compile('value="st=.*?(videobob2serial22)\.txt').findall(http)
	if len(rows1) >= 1:
		SERII(params)
	else:
		Play_kino(params)

def PLAY(params):# серии плай сделано
	http = urllib.unquote_plus(params['url'])
	if http == None: return False
	name = urllib.unquote_plus(params['name'])
	text = urllib.unquote_plus(params['text'])
	alt = urllib.unquote_plus(params['alt'])
	img = urllib.unquote_plus(params['img'])
	i = xbmcgui.ListItem(unicode(DEC(name)+'    '+alt, "windows-1251"), iconImage=img, thumbnailImage=img)
	i.setInfo(type='video', infoLabels={'title': unicode(DEC(name)+'    '+alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
	xbmc.Player().play(http, i)

   
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
if mode == 'SRAVN': SRAVN(params)
if mode == 'SRAVN2': SRAVN2(params)
if mode == 'search': search(params)
if mode == 'MOVIES_search': MOVIES_search(params)
if mode == 'Play_kino': Play_kino(params)
if mode == 'PLAY_serii': PLAY_serii(params)
if mode == 'stran': stran(params)