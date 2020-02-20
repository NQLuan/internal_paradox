import requests


def lunch_creation():
    url = 'http://35.209.247.237/api/v1/actions/create_next_month/'
    requests.post(url)
