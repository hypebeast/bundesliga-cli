.PHONY: clean

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  production  Clean and do a release"
	@echo "  release     package and upload a release"
	@echo "  sdist       package"

production: clean release

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt --use-mirrors

clean:
	rm -rf build \
	rm -rf dist \
	rm -rf *.egg-info \
	find . -name '*.pyc' -exec rm -f {} \
	find . -name '*.pyo' -exec rm -f {} \
	find . -name '*~' -exec rm -f {}

lint:
	flake8 bundesliga > violations.flake8.txt

release: register
	python setup.py sdist upload

register:
	python setup.py register

sdist:
	python setup.py sdist
