from selenium import webdriver
import time
import datetime
import jan_enum

# -----ADDED TO RUN BROWSER HEADLESS-----
#LOOK AT: https://blog.testproject.io/2018/02/20/chrome-headless-selenium-python-linux-servers/
from pyvirtualdisplay import Display 

class Cobiss:

    minDays = 100
    isError = False
    error = ''
    status = None
    cobissLink = 'https://plus.si.cobiss.net/opac7/user/login/aai/cobiss'
    subject = "Cobiss API"

    def __init__(self, cardNum, passw):
        self.cardNum = cardNum
        self.passw = passw
        self.loanLink = 'siktrz/'+cardNum[1:7]   #loan_link = "siktrz/104232"

    def checkCobiss(self):
        print('Check Cobiss running...')

        display = Display(visible=0, size=(1024, 768)) 
        display.start() 

        for x in range(3):

            driver = webdriver.Firefox(timeout=60)  #geckodriver -> needs to be in /usr/local/bin

            driver.get(self.cobissLink)

            #wait to script bild whole web page
            time.sleep(2)

            driver.find_element_by_xpath("//div[@class='tableField']/div[1]/div[1]").click()

            #wait to dropdown bild (1000 inputs)
            time.sleep(3)

            driver.find_element_by_xpath("//div[@class='tableField']/div[1]/div[2]/div[1]/div[@data-value='siktrz']").click()

            libMemberID = driver.find_element_by_id("libMemberID")
            password = driver.find_element_by_id("password1")

            libMemberID.send_keys(self.cardNum)
            password.send_keys(self.passw)

            time.sleep(1)

            driver.find_element_by_id("wp-submit1").click()

            #wait to load new page 
            time.sleep(3)

            logInFlag = False
            for x in range(6):
                if driver.current_url == "https://plus.si.cobiss.net/opac7/memberships":
                    logInFlag = True
                    break

                time.sleep(3)

            if not logInFlag:
                print("Error: can not log in!")
                driver.close()
            else:
                break

        if not logInFlag:
            self.isError = True
            self.error = 'Dostop do COBISS ni uspel!'

            driver.close()

            exit()

        driver.get('https://plus.si.cobiss.net/opac7/mylib/'+self.loanLink+'/loan')

        time.sleep(5)

        booksAtHome = driver.find_elements_by_xpath("//tbody [@id='extLoanStuleBody']/tr")

        for book in booksAtHome:
            #check_box = book.find_element_by_xpath(".//td[1]/div/span/input")
            return_date = book.find_element_by_xpath(".//td[2]")
            #title = book.find_element_by_xpath("/td[3]")
            #take_date = book.find_element_by_xpath("/td[6]")

            #print(return_date.text)

            return_date_date = datetime.datetime.strptime(return_date.text, '%d.%m.%Y') + datetime.timedelta(days=1)

            today = datetime.datetime.now()

            delta = return_date_date - today

            # print(delta.days)

            if delta.days < self.minDays:
                self.minDays = delta.days


        if self.minDays < 3:
            print("Book will expire!")
            self.status = jan_enum.EStatusLibrary.EXPIRE_SOON

            # email.sentEmail("jan.cvek@gmail.com", self.subject, "Vrni knjige v knjižnico: kartica Jan! Še "+ str(minDays) +" do poteka!")
        else:
            print('Everything is OK! Days to expire: '+str(self.minDays))
            self.status = jan_enum.EStatusLibrary.OK

        print('Check Cobiss end.')
        driver.close()