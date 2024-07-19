from email.message import EmailMessage
import ssl
import smtplib
import configparser
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # ga_csv_file_path = 'path of csv file'
        # gsc_csv_file_path = 'path of csv file'
        # linkedin_csv_file_path = 'path of csv file  # Update with your LinkedIn CSV file path
        twitter_csv_file_path = 'C:\\Users\\tmana\\OneDrive\\Desktop\\analytics\\myproject\\multiple-Email-social-report\\TwExport_wallet_hunter_Posts.csv'  # Example of CSV file path
    
        # ga_data = pd.read_csv(ga_csv_file_path)
        # gsc_data = pd.read_csv(gsc_csv_file_path)
        # linkedin_data = pd.read_csv(linkedin_csv_file_path, encoding='ISO-8859-1')  # Read the LinkedIn CSV file with 'ISO-8859-1' encoding
        twitter_data = pd.read_csv(twitter_csv_file_path, encoding='ISO-8859-1')  # Read the Twitter CSV file with 'ISO-8859-1' encoding
    
        return render_template('index.html', 
                        #    ga_tables=[ga_data.to_html(classes='data')], ga_titles=ga_data.columns.values,
                        #    gsc_tables=[gsc_data.to_html(classes='data')], gsc_titles=gsc_data.columns.values,
                        #    linkedin_tables=[linkedin_data.to_html(classes='data')], linkedin_titles=linkedin_data.columns.values,  # Add a comma here
                           twitter_tables=[twitter_data.to_html(classes='data')], twitter_titles=twitter_data.columns.values)  # Add Twitter data to the template
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return "An error occurred. Please try again later.", 500
    
    
config = configparser.ConfigParser()
config.read('C:\\Users\\tmana\\OneDrive\\Desktop\\analytics\\myproject\\multiple-Email-social-report\\config.ini') # config.ini file path

# Email details
sender_email = 'you@gmail.com'
receiver_email = ['to@gmail.com', 'to@gmail.com'] # you can add as many gmail as you want
password = config['mails']['password']  # Use the 16 digit password from the google account setting

# Get the report
with app.test_client() as c:
    response = c.get('/')
    report = response.get_data(as_text=True)

# Set up the SMTP server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Login to the email server
server.login(sender_email, password)

# Create the email
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = ', '.join(receiver_email)
msg['Subject'] = "Report"
msg.set_content(report, subtype='html')

# Send the email
server.send_message(msg)

# Close the connection to the server
server.quit()