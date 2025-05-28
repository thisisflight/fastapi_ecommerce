.DEFAULT_GOAL := help

HOST ?= localhost
PORT ?= 9000

run:
	uvicorn app.main:app --reload --host $(HOST) --port $(PORT)

push:
	git push -u origin HEAD
