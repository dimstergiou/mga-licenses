from flask import Flask
from flask import render_template
from selenium import webdriver
import chromedriver_binary

app = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=chrome_options)


@app.route('/')
def mga():
    browser.get('https://mgalicenseeregister.mga.org.mt/Results1.aspx?Licencee=&Class=&Status=&URL=')
    # Parse JS variables
    company_name = browser.execute_script('return vArrayCompanyName')
    license_class = browser.execute_script('return vArrayLicenceClass')
    license_number = browser.execute_script('return vArrayLicenceNumber')
    status = browser.execute_script('return vArrayStatus')
    reg_number = browser.execute_script('return vArrayRegNumber')
    counter = browser.execute_script('return counter')
    browser.quit()

    companies = []
    for i in range(int(counter)):
        companies.append([str(company_name[i]), str(license_class[i]), str(
            license_number[i]), str(status[i]), str(reg_number[i])])

    return render_template('index.html', companies=companies)


if __name__ == '__main__':
    app.run()
