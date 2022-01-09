#!/usr/bin/env python3
from flask import Flask
from celery import Celery

celery = Celery('tasks', backend='rpc://', broker='pyamqp://')

@celery.task
def count():
	for i in range(5):
		print(i)

count()