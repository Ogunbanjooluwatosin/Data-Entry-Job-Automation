# -----------------------------------------imports----------------------
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import requests

# -----------------------------------------constants----------------------
google_form_link = "https://forms.gle/FSnPnDdQHcvBxRGk6"

zillow_endpoint = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.87400423058532%2C%22east%22%3A-122.17412082080078%2C%22south%22%3A37.67644770129696%2C%22west%22%3A-122.69253817919922%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22mapZoom%22%3A11%7D"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'zguid=23|%24ca6368b9-7b92-4d51-ab67-c2be89065efd; _ga=GA1.2.1460486079.1621047110; _pxvid=7fa13d96-b528-11eb-9860-0242ac120012; _gcl_au=1.1.2025797213.1621047113; __gads=ID=66253ab863481044:T=1621047113:S=ALNI_MZr3mehwm2Wjo7NOrmalVtEcJSXag; __pdst=50987f626deb4767a53b5d8ca2ea406a; _fbp=fb.1.1621047115574.1019382068; _pin_unauth=dWlkPU5EVm1PRGRpTVRBdE5UTTFaUzAwWlRBNExUZzJZall0TWpZMU1HWTBNV0ppWlRkbA; G_ENABLED_IDPS=google; userid=X|3|231a9d744e104379%7C3%7CiEt8bkUx9hWaFeyCeAwN9tHl_T0d0Cq-kynGuEvNYr4%3D; loginmemento=1|c2274ba4a4ad76bbe89263d30695c182e9177b9c40a2691f3054987d66a944be; zjs_user_id=%22X1-ZU158jhpb2klds9_4wzn7%22; zgcus_lbut=; zgcus_aeut=189997416; zgcus_ludi=b44a961b-c7ef-11eb-a48f-96824e7eff50-18999; optimizelyEndUserId=oeu1623111792776r0.8778663892923859; _cs_c=1; WRUIDAWS=3326630244368428; visitor_id701843=248614376; visitor_id701843-hash=4be116fbd77089f953bfb6eaf5996ef92662a6ef7d237d3c49f154ffaf4eaa9295c64fb254b106bdff234e183c94498c01af2aab; __stripe_mid=80125db1-17d1-4fc5-ae37-86b12a68709cf3da6d; g_state={"i_p":1627697570928,"i_l":4}; zjs_anonymous_id=%22ca6368b9-7b92-4d51-ab67-c2be89065efd%22; _gac_UA-21174015-56=1.1626042638.Cj0KCQjwraqHBhDsARIsAKuGZeH8gi095UkXfohW-WWvyLosdmTdL8cfJwgAabYF9hS2XU6JlXqpWLcaAq5SEALw_wcB; _gcl_aw=GCL.1626042640.Cj0KCQjwraqHBhDsARIsAKuGZeH8gi095UkXfohW-WWvyLosdmTdL8cfJwgAabYF9hS2XU6JlXqpWLcaAq5SEALw_wcB; zgsession=1|1edd82e6-372a-4546-bc8b-c2bbadfd29b4; DoubleClickSession=true; fbc=fb.1.1626412984774.IwAR2QM6bzrTskAWN5Sk8UnmPlAxb1HRy1h1GRch888QqXfczHZZWb2vDZfIw; _fbc=fb.1.1626413249162.IwAR2QM6bzrTskAWN5Sk8UnmPlAxb1HRy1h1GRch888QqXfczHZZWb2vDZfIw; _csrf=lV2BBFim7Vy2gFTn--PUt0VA; _gaexp=GAX1.2.w27igyYtRQaAa8XQM3MjDw.18837.2!VDVoDKTnRcyv8f4FAcJ8PA.18915.2!Khnq27RoQmSe5DEusmh5xA.18913.3; _gid=GA1.2.705011419.1630004829; FSsampler=707279376; __CT_Data=gpv=26&ckp=tld&dm=zillow.com&apv_82_www33=26&cpv_82_www33=26&rpv_82_www33=13; OptanonConsent=isIABGlobal=false&datestamp=Fri+Aug+27+2021+12%3A39%3A52+GMT-0600+(Mountain+Daylight+Time)&version=5.11.0&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; _cs_id=41cbdc9c-bb0b-aad9-9521-b1328a65ff77.1623111795.22.1630089665.1630089591.1.1657275795752; utag_main=v_id:01796deff9e3001a59964343177e03079002907100838$_sn:41$_se:2$_ss:0$_st:1630255637884$dc_visit:38$ses_id:1630253822479%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:2%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:7b8796ca-44dd-45c9-97d9-bcb642d04cd1%3Bexp-session; JSESSIONID=6CB8C410E0FE216644E8C3A0D0851618; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEklf443J474nftKzJe5PKLD80sujgHvySB7tGcqZunX3BDDH9VwceMqGMTPC54%2F0q4CH%2BfmwsC6P; KruxPixel=true; _derived_epik=dj0yJnU9ai1PSUp1eHZ2Y3J3d0c2NVU1N3BBOFlHbnRBOGFzT0smbj1vLWRISDFwdUNoblN5MjQ4cTVyN213Jm09MSZ0PUFBQUFBR0VzRjRVJnJtPTEmcnQ9QUFBQUFHRXNGNFU; KruxAddition=true; search=6|1632872450375%7Crect%3D40.241821806991595%252C-103.77545313688668%252C39.18758562803622%252C-106.02765040251168%26disp%3Dmap%26mdm%3Dauto%26type%3Dhouse%252Cmultifamily%252Ctownhouse%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%0911093%09%09%09%09%09%09; _uetsid=d5e0465006a011ecbe3bd1a0f1c47d01; _uetvid=987e1c70c40a11ebaed8859af36f82fb; _px3=ba45c3df5d5d63d4d9780a102253cd60b21ab52b04778344e332e05474011c21:oCvapPXE6jD0rCXhSf4UjtEC2U956148EDyiWwRFOF8z5vwK63/hC8OWsk09O61g1spnZw64iXApZu1wOmKpyA==:1000:68UzJ5+ar5XwNm61bm41bhSHp8Zp1PfQQlL/5tcqdUIJ3RmA106//vvYGewCCwmln6acqbDAVKgqfB8Th05yX0Cw0TBW7dhfNdeNRjp9bxeLvKqZ56yuW+aVoYYp/zj6MNKv9c16vKlP771xSdCgUTvZ0CDmh7Ng55sHugOHt/jj+2Zmp2WLnuYR4rf7SEndqWBbAyQhhG4BKeyrZyEMpA==; AWSALB=3BIj2fUDeYgoAcLKaZdMkcyTzWSof62v91DQuCssJMyknlpZWcRcVnUU5Me29AcnFcjg1k9H2ehS6N0rSwxo4w8lmEvFCy6hgQfKm1HH8oVoWtpICS36NoLMMxmZ; AWSALBCORS=_ga=GA1.2.663432782.1683613852; PHPSESSID=8e8edcaa49b9ca4ba58bdd4a5b0d79b1; _gid=GA1.2.1164358470.1685036000',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': 'Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'upgrade-insecure-requests': '1',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

response = requests.get(url=zillow_endpoint, headers=headers)
print(response.status_code)

contents = response.text


class DataEntry:
    def __init__(self):
        self.soup = BeautifulSoup(contents, "html.parser")
        chrome_driver_path = Service(executable_path="C:/Development/chromedriver.exe")
        self.driver = webdriver.Chrome(service=chrome_driver_path)
        self.driver.get(url=google_form_link)
        # -----------------------------------------if page crashes----------------------
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

    def data_code(self):
        all_link = self.soup.find_all('a', {"data-test": "property-card-link"})

        new_link = []
        # ----------for all links
        for link in all_link:
            href = link.get('href')
            if "http" not in href:
                new_link.append(f"https://www.zilow.com{href}")
            else:
                new_link.append(href)
        print(new_link)

        # ----------for all addresses

        all_address = self.soup.find_all("address", {"data-test": "property-card-addr"})

        # ----------for all worth

        all_worth = self.soup.find_all("span", {"data-test": "property-card-price"})
        # -----------------------------------------using selenium----------------------

        # ----------inputting address

        for count in range(len(new_link)):
            sleep(5)
            address_entry = self.driver.find_element(by=By.XPATH,
                                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address_entry.send_keys(all_address[count].text)
            address_entry.send_keys(Keys.RETURN)

            sleep(2)

            price_entry = self.driver.find_element(by=By.XPATH,
                                                   value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_entry.send_keys(all_worth[count].text.split()[0])
            price_entry.send_keys(Keys.RETURN)
            sleep(2)

            link_entry = self.driver.find_element(by=By.XPATH,
                                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_entry.send_keys(new_link[count])
            link_entry.send_keys(Keys.RETURN)

            # click on submit button
            submit = self.driver.find_element(by=By.XPATH,
                                              value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
            submit.click()

            # fill another response
            another_response = self.driver.find_element(by=By.XPATH,
                                                        value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            another_response.click()

            sleep(10)
            self.driver.quit()
