import os
from requests import post



class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    EMAIL = os.environ.get('EMAIL')

    FROM_TITLE = 'New Feedback Submission'
    FROM_EMAIL = os.environ.get("FROM_EMAIL")

    @classmethod
    def send_email(cls, html):
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException('mailgun_failed_load_api_key')

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException('mailgun_failed_load_domain')

        response = post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=('api', cls.MAILGUN_API_KEY),
            data={
                'from': f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                'to': cls.EMAIL,
                'subject': "Natours Feedback",
                'html': html
            },
        )
        if response.status_code != 200:
            raise MailGunException('An error occurred while sending e-mail.')
        return response
