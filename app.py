from flask import Flask
from flask import render_template
from selenium import webdriver
from flask_apscheduler import APScheduler
import chromedriver_binary
import datetime

app = Flask(__name__)
scheduler = APScheduler()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=chrome_options)

def scrape_mga():
    companies = []
    browser.get('https://mgalicenseeregister.mga.org.mt/Results1.aspx?Licencee=&Class=&Status=&URL=')
    company_name = browser.execute_script('return vArrayCompanyName')
    license_class = browser.execute_script('return vArrayLicenceClass')
    license_number = browser.execute_script('return vArrayLicenceNumber')
    status = browser.execute_script('return vArrayStatus')
    reg_number = browser.execute_script('return vArrayRegNumber')
    counter = browser.execute_script('return counter')
    browser.quit()

    for i in range(int(counter)):
        companies.append([str(company_name[i]), str(license_class[i]), str(
            license_number[i]), str(status[i]), str(reg_number[i])])
    return companies

companies = scrape_mga()
last_update = datetime.datetime.now()

@app.route('/')
def mga():
    if companies:
        return render_template('index.html', companies=companies, last_update=last_update)
    else:
        scrape_mga()
        return render_template('index.html', companies=companies)

if __name__ == '__main__':
    scheduler.add_job(id='Scrape MGA site', func=scrape_mga, trigger='interval', seconds=21600)
    scheduler.start()
    app.run()
