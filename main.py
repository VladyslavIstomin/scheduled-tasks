import datetime as dt
import pandas as pd
import random
import smtplib
import os

month_now = dt.datetime.today().month
day_now = dt.datetime.today().day

birthday_data = pd.read_csv('birthdays.csv').to_dict('records')

for birthday in birthday_data:
    if birthday['month'] == month_now and birthday['day'] == day_now:
        birthday_name = birthday['name']
        with open(f'letter_templates/letter_{random.randint(1, 3)}.txt', 'r') as file:
            file = file.read()

        replaced_name = file.replace("[NAME]", birthday_name)
        new_mail = "".join(replaced_name)

        my_email = os.environ.get("MY_EMAIL")
        my_password = os.environ.get("MY_PASSWORD")
        with smtplib.SMTP('smtp.ethereal.email', 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(to_addrs=my_email, msg=f"Subject:Happy Birthday\n\n{new_mail}", from_addr=my_email)
