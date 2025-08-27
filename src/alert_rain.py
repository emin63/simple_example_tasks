"""Simple script to alert me if it is going to raining.

Must provide environment variables to configure (see `get_vars`) function.
"""

import logging
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

import requests


def send_email(msg, subject, to_email, from_email, app_passwd):
    """Send an email via Gmail SMTP.
    
    Args:
        msg (str): The message body to send
        subject (str): Email subject line
        to_email (str): Recipient's email address
        from_email (str): Sender's Gmail address
        app_passwd (str): Gmail app password (not regular password)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        email_msg = MIMEMultipart()
        email_msg['From'] = from_email
        email_msg['To'] = to_email
        email_msg['Subject'] = subject
        
        # Attach message body
        email_msg.attach(MIMEText(msg, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable encryption
        server.login(from_email, app_passwd)
        
        # Send email
        text = email_msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logging.exception(f"Error sending email: {e}")
        return False


def get_vars():
    my_vars = {}
    for name, reason in (
            ('FROM_EMAIL', 'Email account sending email.'),
            ('GMAIL_APP_PASSWD', 'The app password for your sending account.'),
            ('TO_EMAIL', 'Email account to send to.'),
            ('LATITUDE', 'The latitude where you want the weather report.'),
            ('LONGITUDE', 'The longitude where you want the weather report.'),
            ('RAIN_ALERT', 'If percent change of rain above this, email sent.'),
            ):
        value = os.environ.get(name, None)
        if not value:
            raise ValueError(f'Must provide env var {name} as {reason}.')
        my_vars[name] = value
    return my_vars


def main():
    timeout = 30
    my_vars = get_vars()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': my_vars['LATITUDE'],
        "longitude": my_vars['LONGITUDE'],
        "current": "temperature_2m,wind_speed_10m,precipitation_probability",
        "forecast_days": 1,
    }
    req = requests.get(url, params=params, timeout=timeout)
    results = req.json()
    current_data = results.get('current', {})
    info = {
        'rain_chance_percent': current_data.get('precipitation_probability'),
        'timestamp': current_data.get('time'),
        'location': f"{my_vars['LATITUDE']}, {my_vars['LONGITUDE']}",
        }
    print(f'Current data:\n{info}')
    if info['rain_chance_percent'] > int(my_vars['RAIN_ALERT']):
        send_email(str(info), f'rain forecast {info["rain_chance_percent"]}%',
                   my_vars['TO_EMAIL'], my_vars['FROM_EMAIL'],
                   my_vars['GMAIL_APP_PASSWD'])

    return info


if __name__ == '__main__':
    main()
