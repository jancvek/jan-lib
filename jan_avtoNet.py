import urllib.request
from bs4 import BeautifulSoup

class Offer():
    def __init__(self, id, title, prvaReq, km, motor, menjalnik,cena):
        self.id = id
        self.title = title
        self.prvaReq = prvaReq
        self.km = km
        self.motor = motor
        self.menjalnik = menjalnik
        self.cena = cena

class AvtoNet():
    _baseSearchUrl = "https://www.avto.net/Ads/results.asp"
    _detailUrl = "https://www.avto.net/Ads/details.asp"
    _newestUrl = "https://www.avto.net/Ads/results_100.asp?oglasrubrika=1&prodajalec=2"
    _znamka = None
    _model = None
    _cenaMin = None
    _cenaMax = None
    _letnikMin = "0"
    _letnikMax = "2090"
    _bencin = "0"
    _oblika = "0"
    _kmMin = None
    _kmMax = None
    _kwMin = None
    _kwMax = None
    _stran = None
    _response = None

    _znamkaText = "znamka"
    _modelText = "model"
    _cenaMinText = "cenaMin"
    _cenaMaxText = "cenaMax"
    _letnikMinText = "letnikMin"
    _letnikMaxText = "letnikMax"
    _bencinText = "bencin"
    _oblikaText = "oblika"
    _kmMinText = "kmMin"
    _kmMaxText = "kmMax"
    _kwMinText = "kwMin"
    _kwMaxText = "kwMax"
    _stranText = "stran"    

    _offers = []

    #bencin:
    #vse možnosti -> 0
    #bencin -> 201
    #diesel -> 202
    #plin -> 203
    #hibrid -> 205

    #oblika:
    #vse možnosti -> 0
    #limuzina -> 11
    #kombilimuzina -> 12
    #karavan -> 13
    #enoprostorec -> 14

 
    def setSearch(self,znamka,model,cenaMin,cenaMax,letnikMin,letnikMax,bencin,oblika,kmMin,kmMax,kwMin,kwMax):

        if not znamka == "":
            self._znamka = znamka

        if not model == "":
            self._model = model

        if not cenaMin == "":
            self._cenaMin = cenaMin

        if not cenaMax == "":
            self._cenaMax = cenaMax

        if not letnikMin == "":
            self._letnikMin = letnikMin

        if not letnikMax == "":
            self._letnikMax = letnikMax

        if not bencin == "":
            self._bencin = bencin

        if not oblika == "":
            self._oblika = oblika

        if not kmMin == "":
            self._kmMin = kmMin

        if not kmMax == "":
            self._kmMax = kmMax

        if not kwMin == "":
            self._kwMin = kwMin

        if not kwMax == "":
            self._kwMax = kwMax
        return

    def runSearch(self):
        searchUrl = self._baseSearchUrl

        if self._znamka:
            searchUrl = searchUrl+"?"+self._znamkaText+"="+self._znamka

        if self._model:
            searchUrl = searchUrl+"&"+self._modelText+"="+self._model

        if self._cenaMin:
            searchUrl = searchUrl+"&"+self._cenaMinText+"="+self._cenaMin

        if self._cenaMax:
            searchUrl = searchUrl+"&"+self._cenaMaxText+"="+self._cenaMax

        if self._letnikMin:
            searchUrl = searchUrl+"&"+self._letnikMinText+"="+self._letnikMin

        if self._letnikMax:
            searchUrl = searchUrl+"&"+self._letnikMaxText+"="+self._letnikMax

        if self._bencin:
            searchUrl = searchUrl+"&"+self._bencinText+"="+self._bencin

        if self._oblika:
            searchUrl = searchUrl+"&"+self._oblikaText+"="+self._oblika

        if self._kmMin:
            searchUrl = searchUrl+"&"+self._kmMinText+"="+self._kmMin

        if self._kmMax:
            searchUrl = searchUrl+"&"+self._kmMaxText+"="+self._kmMax

        if self._kwMin:
            searchUrl = searchUrl+"&"+self._kwMinText+"="+self._kwMin

        if self._kwMax:
            searchUrl = searchUrl+"&"+self._kwMaxText+"="+self._kwMax

        if self._stran:
            searchUrl = searchUrl+"&"+self._stranText+"="+self._stran

        searchUrl = searchUrl+'&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000100120&EQ8=1010000001&EQ9=100000000&KAT=1010000000&stran='

        print(searchUrl)

        response = urllib.request.urlopen(searchUrl)
        html = response.read()

        self._response = html

        return

    def runSearchByUrl(self, url):
        response = urllib.request.urlopen(url)
        html = response.read()

        self._response = html

    def getOffers(self):
        soup = BeautifulSoup(self._response,'html.parser')

        offers = soup.find_all(class_="ResultsAd")

        i = 0
        for x in offers:
            i+=1
            y = x.find(class_="ResultsAdDataTop")
            a = y.find('a')
            href = a.attrs['href']
            id = self.getIdFromHref(href)
            
            span = a.find('span')
            title = span.text

            ul = y.find('ul')
            li = ul.find_all('li')

            prvaReq = ''
            km = ''
            motor = ''
            menjalnik = ''
            cena = ''

            for data in li:
                text = data.text
                if 'Letnik' in text:
                    prvaReq = text
                elif text[0].isdigit():
                    km = text
                elif 'motor' in text:
                    motor = text
                elif 'menjalnik' in text:
                    menjelnik = text
                else:
                    continue
            
            if x.find(class_="ResultsAdPriceRegular"):
                priceDiv = x.find(class_="ResultsAdPriceRegular")
            elif x.find(class_="ResultsAdPriceAkcijaCena"):
                priceDiv = x.find(class_="ResultsAdPriceAkcijaCena")
            else:
                print("Error! Ne najde cene!")
            
            cena = priceDiv.text

            self._offers.append(Offer(id,title,prvaReq,km,motor,menjalnik,cena))        
            print(id+' '+title+' '+prvaReq+' '+km+' '+motor+' '+menjalnik+' '+cena)

    def getIdFromHref(self,href):
        start = href.find('id=')
        id = href[start+3:start+11]

        return id

    def getCarDetails(self,id):
        detailUrl = self._detailUrl+"?id="+id
        response = urllib.request.urlopen(detailUrl)
        html = response.read()

        soup = BeautifulSoup(html,'html.parser')
        details = soup.find_all(class_="OglasData")

        for x in details:
            name = x.find(class_="OglasDataLeft")
            value = x.find(class_="OglasDataRight")

            #if

            #print(name.text+" - "+value.text)
        
    #def seveDetails(self,name,value):
        #"1.registracija:"
        #"Letnik:"
        #"Starost:"
        #"Tehnični pregled:"
        #"Prevoženi km:"
        #"Gorivo:"
        #"Motor:"
        #"Menjalnik:"
        #"Oblika:"
        #"Barva:"
        #"Notranjost:"
        #"Kraj ogleda:"

        #""

    def getNewestCars(self):
        response = urllib.request.urlopen(self._newestUrl)
        html = response.read()

        self._response = html

        self.getOffers()

        for offer in self._offers:
            print(offer.title)

        return

if __name__ == '__main__':
    avto = AvtoNet()
    avto.runSearchByUrl('https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=8000&cenaMax=12000&letnikMin=2015&letnikMax=2090&bencin=202&starost2=999&oblika=13&ccmMin=1800&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=200000&kwMin=0&kwMax=999&motortakt=&motorvalji=&lokacija=0&sirina=&dolzina=&dolzinaMIN=&dolzinaMAX=&nosilnostMIN=&nosilnostMAX=&lezisc=&presek=&premer=&col=&vijakov=&EToznaka=&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000100020&EQ8=1010000001&EQ9=100000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=&paketgarancije=0&broker=&prikazkategorije=&kategorija=&zaloga=10&arhiv=&presort=&tipsort=&stran=')