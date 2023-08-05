import requests


class Rasa:
    def __init__(self, onedash_token):
        self.token = onedash_token
        self.last_user_event = None

    def log_data(self, data):
        url = 'https://app.onedash.cc/api/insert/record/rasa'
        headers = {'Authorization': self.token}
        response = requests.post(url=url, headers=headers, json=data)

    @classmethod
    def from_endpoint_config(
            cls, broker_config
    ):
        if broker_config is None:
            return None
        return cls(**broker_config.kwargs)

    def publish(self, event):
        if self.last_user_event is not None:
            if event['event'] == 'action' and event['policy'] == 'policy_3_FallbackPolicy':
                self.last_user_event['is_fallback'] = True
            else:
                self.last_user_event['is_fallback'] = False
            self.log_data(self.last_user_event)
            self.last_user_event = None
        elif event['event'] == 'user':
            self.last_user_event = event
        elif event['event'] == 'bot':
            self.log_data(event)
