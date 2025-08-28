"""Simple script to alert me if weather rainy, too hot, or too cold.

Must provide environment variables to configure (see `get_vars`) function.
"""

import logging
import os

import requests

from ox_task.core.comm_utils import send_email

def get_vars():
    "Get required variables from environment (or complain if missing)."
    my_vars = {}
    for name, reason, default in (
            ('FROM_EMAIL', 'Email account sending email.', ''),
            ('GMAIL_APP_PASSWD', 'App password for your sending account.', ''),
            ('TO_EMAIL', 'Email account to send to.', ''),
            ('LATITUDE', 'The latitude where you want the weather report.',
             '32.361145'),   # Boston latitude
            ('LONGITUDE', 'The longitude where you want the weather report.',
             '-71.057083'),  # Boston longitude
            ('RAIN_ALERT', 'If % change of rain above this, email sent.', '40'),
            ('HOT_ALERT', 'If temperature above this, email sent', '90'),
            ('COLD_ALERT', 'If temperature below this, email sent', '30'),
            ('TEMPERATURE_UNIT', 'Either fahrenheit or celsius', 'fahrenheit')
            ):
        value = os.environ.get(name, default)
        if not value and not default:
            logging.error('missing value for %s; env list is %s', name,
                          list(sorted(os.environ)))
            raise ValueError(f'Must provide env var {name} as {reason}.')
        my_vars[name] = value
    return my_vars


def main():
    """Main function to run to get weather and alert user if necessary.
    """
    timeout = 30
    my_vars = get_vars()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'temperature_unit': my_vars['TEMPERATURE_UNIT'],
        'latitude': my_vars['LATITUDE'], "longitude": my_vars['LONGITUDE'],
        "current": "temperature_2m,wind_speed_10m,precipitation_probability",
        "forecast_days": 1,
    }
    req = requests.get(url, params=params, timeout=timeout)
    results = req.json()
    current_data = results.get('current', {})
    info = {
        'temperature_2m': current_data.get('temperature_2m'),
        'rain_chance_percent': current_data.get('precipitation_probability'),
        'timestamp': current_data.get('time'),
        'location': f"{my_vars['LATITUDE']}, {my_vars['LONGITUDE']}",
        }

    subject = []
    if info['rain_chance_percent'] > float(my_vars['RAIN_ALERT']):
        subject.append(f'rain forecast :{info["rain_chance_percent"]}%')
    if info['temperature_2m'] > float(my_vars['HOT_ALERT']):
        subject.append(f'hot: {info["temperature_2m"]}')
    if info['temperature_2m'] < float(my_vars['COLD_ALERT']):
        subject.append(f'cold: {info["temperature_2m"]}')        

    if subject:
        subject = '; '.join(subject)
        print(f'alert: {subject}')
        send_email(str(info), subject, my_vars['TO_EMAIL'],
                   my_vars['FROM_EMAIL'], my_vars['GMAIL_APP_PASSWD'])

    print(f'Current data:\n{info}')
    return info


if __name__ == '__main__':
    main()
