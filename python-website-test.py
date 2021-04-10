from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from botocore.exceptions import ClientError
import boto3
import time
import datetime
import os

dt = str(datetime.datetime.now())
bizid = 'devopstechteamtestbiz'+dt
emailid = 'testbiz@test.com'
instahandle = '@bizfaketestinstagram'+dt
loginimg = 'biz_login_'+dt+'.png'
signupimg = 'biz_signup_page_'+dt+'.png'
subimg = 'biz_submit_confirmation_'+dt+'.png'
images = [loginimg, signupimg, subimg]

driver = webdriver.Chrome()
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get ('https://mavenslists.com')

time.sleep(3)

def biz_login():
    biz_login = driver.find_element_by_xpath('//*[@id="comp-ka1kgnkj"]/a')
    driver.save_screenshot(loginimg)
    biz_login.click()
    time.sleep(3)

def biz_signup():
    biz_name = driver.find_element_by_xpath('//*[@id="input_comp-ka1kxfwz"]')
    biz_name.click()
    biz_name.send_keys(bizid)

    biz_email = driver.find_element_by_xpath('//*[@id="input_comp-ka1kxfx61"]')
    biz_email.click()  
    biz_email.clear()
    biz_email.send_keys(emailid)

    biz_insta = driver.find_element_by_xpath('//*[@id="input_comp-ka4clx6h"]')
    biz_insta.click()
    biz_insta.clear()
    biz_insta.send_keys(instahandle)
    time.sleep(1)
    driver.save_screenshot(signupimg)

def submit():
    time.sleep(3)
    sub_button = driver.find_element_by_xpath('//*[@id="comp-ka1kxfxc1"]/button')
    time.sleep(2)
    driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
    sub_button.click()
    time.sleep(1)
    driver.save_screenshot(subimg)
    driver.close()

def upload_files():
    #loop to add list of screenshots to s3
    for x in images:
        print("uploading files to s3 bucket")
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(x, 'bucketname, 'artifacts/business/'+x)

def remove_files():
    #artifact cleanup
    for i in images:
        os.remove(i)

def send_email():
    #send email
    # This address must be verified with Amazon SES.
    SENDER = "Emanuel Burgess <emanuel@somecompany.app>"

    #configuration set in use
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Maven's list automated website testing for" +dt

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Your website automated testing results (business signup)\r\n"
                 "Pleae see attachments"
                )
            
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Maven's list automated website testing for business signup was successful</h1>
    <p>This email is to confirm that your maven's list website business sign up function was successfully tested. You can search by todays date at the link below
    <a href='https://s3.console.aws.amazon.com/s3/buckets/insertbucketname/artifacts/business/?region=us-east-1&tab=overview'>view testing data here</a>
    </p>
    </body>
    </html>
            """            

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Pemail contents
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    "user@gmail.com", "emanuel@somecompany.app", "lajarrid@somecompany.app"
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName="Mavenslistconfig",
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



biz_login()
biz_signup()
submit()
upload_files()
remove_files()
send_email()