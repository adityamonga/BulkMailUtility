# BulkMailUtility
Utility that takes basic information and schedules Emails to be sent to large number of users.

Works with linux machines. Tested on `Ubuntu 20.04.3 LTS` and `Python 3.8.10`

### Installation
1. `cd` to directory of choice
2. `git clone https://github.com/adityamonga/BulkMailUtility.git`


## Usage
Inside the project directory

Setting Up:
1. `cp BulkMailUtility/credentials.env.example BulkMailUtility/credentials.env`
2. Add credentials to `BulkMailUtility/credentials.env`
3. Update `resources/subject.txt`, `resources/body.txt`, `resources/recipients.txt`, `resources/attachments/`

Run:
1. `make pip`
2. `source venv/bin/activate`
3. `python manage.py runscript scripts.main`

To set up cron:`make cron`

Sets up at 1:30 PM by default. Feel free to use `crontab -e` to make changes.
