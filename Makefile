PROJECT_PATH=`pwd`
VIRTUALENV_NAME=venv/
VIRTUALENV_PATH=$(PROJECT_PATH)$(VIRTUALENV_NAME)
PYTHON_BIN=$(VIRTUALENV_PATH)python
PIP_BIN=$(VIRTUALENV_PATH)pip


install_system_virtualenv:
	python3 -m pip install virtualenv

environment: install_system_virtualenv
	python3 -m virtualenv -p python3 $(VIRTUALENV_NAME)

pip:
	$(PIP_BIN) install -r requirements.txt

