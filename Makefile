PROJECT_PATH=`pwd`/
VIRTUALENV_NAME=venv/
VIRTUALENV_PATH=$(PROJECT_PATH)$(VIRTUALENV_NAME)
PYTHON_BIN=$(VIRTUALENV_PATH)bin/python
PIP_BIN=$(VIRTUALENV_PATH)bin/pip
TMP_CRONFILE = /tmp/cronfile

install_system_virtualenv:
	python3 -m pip install virtualenv

environment: install_system_virtualenv
	python3 -m virtualenv -p python3 $(VIRTUALENV_NAME)

pip: environment
	$(PIP_BIN) install -r requirements.txt

cron:
	# adds to 1:30 p.m by default
	crontab -l > $(TMP_CRONFILE); echo "30 13 * * * cd /root/deployments/BulkMailUtility && source venv/bin/activate && python manage.py runscript scripts.main -v3" >> $(TMP_CRONFILE); crontab $(TMP_CRONFILE); rm $(TMP_CRONFILE)
