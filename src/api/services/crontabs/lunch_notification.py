import requests


def lunch_notification():
    number_of_lunch = requests.get('http://35.209.247.237/api/v1/actions/get_lunch/').text
    url = 'https://hooks.slack.com/services/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'
    data = {'text': 'There is ' + number_of_lunch + ' people having lunch at company today.'}
    requests.post(url, json=data)
