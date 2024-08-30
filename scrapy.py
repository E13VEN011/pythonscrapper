from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
import time

def sendEmail(amazonPrice, chromaPrice):
    sender_email = 'your_email@example.com'
    receiver_email = 'receiver_email@example.com'
    subject = 'Price Update'
    body = f"Chroma Price: ₹{chromaPrice}\n91mobiles Price: ₹{amazonPrice}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, 'your_password')
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def trackPrices():
    chromaProductURL = input("Enter the Chroma URL: ")
    newSiteURL = input("Enter the 91mobiles URL: ")

    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(r'C:\Users\AYUSH\Downloads\chromedriver-win64\chromedriver.exe')  # Path to chromedriver.exe

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # getting chroma prices;)
    try:
        driver.get('https://www.croma.com/oppo-a59-5g-4gb-ram-128gb-starry-black-/p/303139')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'pdp-product-price'))
        )
        chromaPriceElement = driver.find_element(By.ID, 'pdp-product-price')
        chromaProductPrice = float(chromaPriceElement.get_attribute('value').strip().replace(',', '').replace('₹', ''))
        print('Chroma Price:', chromaProductPrice)
    except Exception as e:
        print(f"Error retrieving Chroma price: {e}")
        chromaProductPrice = None

    #getting 91 mob prices;}
    try:
        driver.get('https://www.91mobiles.com/vivo-v30e-price-in-india')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.store_prc'))
        )
        newSitePriceElement = driver.find_element(By.CSS_SELECTOR, 'span.store_prc')
        newSitePriceText = newSitePriceElement.get_attribute('data-price')
        newSiteProductPrice = float(newSitePriceText.strip().replace(',', ''))
        print('91mobiles Price:', newSiteProductPrice)
    except Exception as e:
        print(f"Error retrieving 91mobiles price: {e}")
        newSiteProductPrice = None

    driver.quit()

    if chromaProductPrice is not None and newSiteProductPrice is not None:
        sendEmail(newSiteProductPrice, chromaProductPrice)
    else:
        print("Could not retrieve prices.")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(amazonPrice, chromaPrice):
    message = ''
    if amazonPrice and chromaPrice:
        if amazonPrice > chromaPrice:
            message = f'Chroma price is lower. Price is Rs.{chromaPrice}'
        elif chromaPrice > amazonPrice:
            message = f'Amazon price is lower. Price is Rs.{amazonPrice}'

        if message:
            fromEmail = 'enriquemartin2001@gmail.com'
            toEmail = 'enriquemartin2001@gmail.com'
            password = 'tnhl ouvp ltsz hdeq'

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = fromEmail
            msg['To'] = toEmail
            msg['Subject'] = 'Price Alert'
            msg.attach(MIMEText(message, 'plain'))

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(fromEmail, password)
                    server.send_message(msg)
                print('Email sent successfully')
            except Exception as e:
                print(f'Error sending email: {e}')

while True:
    trackPrices()
    time.sleep(3600)
