import requests


def leave_notification():
    text = requests.get('http://35.209.247.237/api/v1/actions/get_leave/').text
    url = 'https://hooks.slack.com/services/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'
    data = {'text': text}
    requests.post(url, json=data)
