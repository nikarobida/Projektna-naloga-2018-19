import re
import orodje

def zajemi():
    for i in range(1,191):
         spletna_stran = 'https://www.rumratings.com/brands'
         stevila = '?page={}'.format(i)
         naslov = spletna_stran + stevila
         ime_datoteke = 'RumsHTML/Stran{:02}.html'.format(i)
         orodje.shrani(naslov, ime_datoteke)

zajemi()

vzorec = re.compile(
    r'''<\/div>'''
    r'''\n'''
    r'''<div class='rum-title'>'''
    r'''\n'''
    r'''(?P<Name>.*?)'''
    r'''\n'''
    r'''<br>'''
    r'''\n'''
    r'''<div class='rum-info'>'''
    r'''\n'''
    r'''(?P<Country>.*?) \|'''
    r''' (?P<Type>.*?) '''
    r'''\| (?P<Ratings>\d+) rating.*?(\| \S(?P<Price_USD>.*?))?'''
    r'''\n'''
    r'''<\/div>'''
    r'''\n'''
    r'''<\/div>'''
    r'''\n'''
    r'''<div class=.*?>'''
    r'''\n'''
    r'''(?P<Rating>.*?)'''
    r'''\n'''
    r'''<\/div>'''
    ,flags=re.DOTALL)

def izloci(imenik):
     rumi = []
     for html_datoteka in orodje.datoteke(imenik):
          for rum in re.finditer(vzorec, orodje.vsebina_datoteke(html_datoteka)):
               rumi.append(pocisti(rum))
     return rumi


def pocisti(rum):
     podatki = rum.groupdict()
     podatki['Name'] = zamenjaj(str(podatki['Name']))
     podatki['Country'] = str(podatki['Country'])
     podatki['Type'] = str(podatki['Type'])
     podatki['Ratings'] = int(podatki['Ratings'])
     podatki['Price_USD'] = spremeni(str(podatki['Price_USD']))
     podatki['Rating'] = float(podatki['Rating'])
     return podatki

def spremeni(niz1):
    niz2 = zamenjaj_vejico(niz1)
    if niz2 == 'None':
        return niz2
    else:
        return float(niz2)

def zamenjaj_vejico(niz):
    niz = niz.replace(',', '')
    return niz

def zamenjaj(niz):
    niz = niz.replace('&#39;',"'")
    return niz

podatki = izloci('RumsHTML/')
orodje.zapisi_tabelo(podatki, ['Name','Country','Type','Ratings','Price_USD','Rating'], 'RumiCSV/podatki.csv')

