#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, os, json
import xbmcplugin, xbmcgui, xbmcaddon, xbmc

h = int(sys.argv[1])

addon = xbmcaddon.Addon(id='plugin.video.dream-film')
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
	s=s.decode('windows-1251').encode('utf-8')
	return s

def genre():
        u = sys.argv[0] + '?mode=search'
        i = xbmcgui.ListItem('[ ПОИСК ]', iconImage=icon, thumbnailImage=icon)
        xbmcplugin.addDirectoryItem(h, u, i, True)
	wurl = 'http://dream-film.tv/'
	http = GET(wurl)
	if http == None: return False
	r1 = re.compile('<div id="content" class="cont_pad">(.*?)</ul>',re.S).findall(http)
	r2 = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.S).findall(r1[0])
	for href, name in r2:
		i = xbmcgui.ListItem(unicode(name, "windows-1251"), iconImage=icon, thumbnailImage=icon)
		u  = sys.argv[0] + '?mode=OPEN_MOVIES'
		u += '&url=%s'%urllib.quote_plus('http://dream-film.tv/' + href)
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
		url = ('http://dream-film.tv/?do=search&subaction=search&story='+query)
		Blok_search({'url':urllib.quote_plus(url)})
	else:
		return False
	
def Blok_search(params):
	http = GET(urllib.unquote_plus(params['url']))
	r2 = re.compile('<a href="([^"]+)" ><img title=".*?" alt="(.*?)" style=".*?" src="(.*?)"></a>',re.S).findall(http)
	if len(r2) == 0:
		showMessage('ФИЛЬМЫ НЕ НАЙДЕНЫ', '')
		return False
	for href, alt, img in r2:
		i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
		u  = sys.argv[0] + '?mode=FILMS'
		u += '&url=%s'%urllib.quote_plus(href)
		u += '&alt=%s'%urllib.quote_plus(alt)
		u += '&img=%s'%urllib.quote_plus(img)
		xbmcplugin.addDirectoryItem(h, u, i, True)
	xbmcplugin.endOfDirectory(h)
	
def OPEN_MOVIES(params):
	try:
		http = GET(urllib.unquote_plus(params['url'])).replace('alt=""','alt="')
		if http == None: return False
		r1 = re.compile('<div id=\'dle-content\'>(.*?)<div class="small_box2 premiers">',re.S).findall(http)
		r2 = re.compile('<a href="([^"]+)"><img title=".*?" alt="(.*?)"',re.S).findall(r1[0])
		r3 = re.compile('src="http://dream-film.tv/(.+?)"',re.I).findall(r1[0])
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok('ВНИМАНИЕ!', 'Нет такой страницы.', 'В этом разделе меньше страниц.')
	ii = 0
	for href, alt in r2:
			img = 'http://dream-film.tv/' + r3[ii]
			ii = ii + 1
			i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
			u  = sys.argv[0] + '?mode=FILMS'
			u += '&url=%s'%urllib.quote_plus(href)
			u += '&img=%s'%urllib.quote_plus(img)
			u += '&alt=%s'%urllib.quote_plus(alt)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	try:
		
		rp2 = re.compile('<div class="navigation">.*?<a href=".*?">.*?</a>\s+<a href="(http://[^/]+/[^/]+/[^/]+/([0-9]+)/)">[^<]+</a></div></div>', re.DOTALL).findall(http)
		#rp2 = re.compile('<a href="(.*?)">(.*?)</a>').findall(rp)
		for href, nr in rp2:
			u = sys.argv[0] + '?mode=OPEN_MOVIES'
			u += '&url=%s'%urllib.quote_plus(href)
			i = xbmcgui.ListItem('[COLOR yellow]Далее > [/COLOR] %s '%nr)
			xbmcplugin.addDirectoryItem(h, u, i, True)
	except:
		pass
	try:
		#rp = re.findall('(http://dream-film\.tv.*?\?page=)([0-9]+)', page_s)
		rp = re.compile('(http://dream-film\.tv.*?[^0-9]+)').findall(href) # или эта без page_s
		for hr in rp:
			#ggg = str(hr[0])
			ggg = hr # или эта без page_s
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
 
def FILMS(params):
	http = GET(urllib.unquote_plus(params['url']))
        if http == None: return False
	r2 = re.compile('"videoplayer123"\)\.innerHTML=\'<iframe src="([^"]+)" frameborder="',re.S).findall(http)
	r4 = re.compile('<div id="news-id-.*?" style="display.*?">(.*?)</div>',re.S).findall(http)
	if len(r2) >= 1:
		http = GET(r2[0])
		r2 = re.compile('<param value="st=htt.*?&amp;file=(.*?)&uid=videoplayer" name="flashvars"',re.S).findall(http)
	if len(r2) == 0:
		FILMS_Serii(params)
        for hre in r2:
		text = r4[0]
		text = re.sub('<.*>',' ', text)
		img = urllib.unquote_plus(params['img'])
		alt = urllib.unquote_plus(params['alt'])
		i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
		i.setProperty("IsPlayable","true")
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		pl.add(hre, i)
		xbmc.Player().play(pl)
 
def FILMS11(params):
	http = GET(urllib.unquote_plus(params['url']))
	if http == None: return False
	r2 = re.compile('<video style=".*?" src="([^"]+)" type=',re.S).findall(http)
	r4 = re.compile('<div id="news-id-.*?" style="display.*?">(.*?)</div>',re.S).findall(http)
	if len(r2) == 0:
		FILMS_Serii(params)
	for hre in r2:
		text = r4[0]
		text = re.sub('<.*>',' ', text)
		img = urllib.unquote_plus(params['img'])
		alt = urllib.unquote_plus(params['alt'])
		i = xbmcgui.ListItem(unicode(alt, "windows-1251"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
		i.setProperty("IsPlayable","true")
		pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		pl.clear()
		pl.add(hre, i)
		xbmc.Player().play(pl)

# серии
def FILMS_Serii(params):
	http = GET(urllib.unquote_plus(params['url']))
        if http == None: return False
	r2 = re.compile("fl:'(.*?)'",re.S).findall(http)
	r4 = re.compile('<div id="news-id-.*?" style="display.*?">(.*?)</div>',re.S).findall(http)
	if len(r2) >= 1:
		http = GET(r2[0])
		r2 = re.compile('"comment":"([^"]+)","file":"([^"]+)"',re.S).findall(http)
        for name, href in r2:
		img = urllib.unquote_plus(params['img'])
		alt = urllib.unquote_plus(params['alt'])
		text = r4[0]
		text = re.sub('<.*>',' ', text)
		i = xbmcgui.ListItem(unicode(DEC(alt)+'   '+name, "utf-8"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
		u  = sys.argv[0] + '?mode=PLAY'
		u += '&img=%s'%urllib.quote_plus(img)
		u += '&url=%s'%urllib.quote_plus(href)
		u += '&alt=%s'%urllib.quote_plus(alt)
		u += '&name=%s'%urllib.quote_plus(name)
		u += '&text=%s'%urllib.quote_plus(text)
		xbmcplugin.addDirectoryItem(h, u, i, True)
        xbmcplugin.endOfDirectory(h)
		
def PLAY(params):
		http = urllib.unquote_plus(params['url'])
		name = urllib.unquote_plus(params['name'])
		alt = urllib.unquote_plus(params['alt'])
		img = urllib.unquote_plus(params['img'])
		text = urllib.unquote_plus(params['text'])
		i = xbmcgui.ListItem(unicode(DEC(alt)+'   '+name, "utf-8"), iconImage=img, thumbnailImage=img)
		i.setInfo(type='video', infoLabels={'title': unicode(alt, "windows-1251"), 'plot': unicode(text, "windows-1251")})
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
if mode == 'SERII': SERII()
if mode == 'genre': genre()
if mode == 'PLAY': PLAY(params)
if mode == 'FILMS': FILMS(params)
if mode == 'FILMS_Serii': FILMS_Serii(params)
if mode == 'search': search(params)
if mode == 'Blok_search': Blok_search(params)
if mode == 'stran': stran(params)