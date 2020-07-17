#!/usr/bin/make -f

SHELL := /bin/bash


icons:
	rm -rf dist/tmp
	mkdir -p dist/tmp
	cd dist/tmp \
		&& git clone git@github.com:clouderp/cerp
	export ICON_ROOT=dist/tmp/cerp/templates/icon \
		&& ./dist/tmp/cerp/scripts/icons

release:
	rm -rf dist/tmp
	mkdir dist/tmp
	cd dist/tmp \
		&& git clone git@github.com:clouderp/cerp
	./dist/tmp/cerp/scripts/release
