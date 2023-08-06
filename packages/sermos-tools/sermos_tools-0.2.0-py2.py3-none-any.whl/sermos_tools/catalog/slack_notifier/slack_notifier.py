""" A tool for sending notifications to Slack channels.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self):
                TODO: Example

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            TODO: Example

"""
import logging
import json
import os
from typing import List
import requests
import attr
from requests.exceptions import ConnectionError as _ConnectionError, Timeout
from sermos_tools import SermosTool

logger = logging.getLogger(__name__)


@attr.s
class SlackNotifier(SermosTool):
    """ Helper to interact with Slack's API

        TODO: This needs work to be more logical / operate more seamlessly
        for both files and messages.

        Usage::

            notifier = SlackNotifier()  # If Env variables set, nothing else needed
            notifier.send_message('Hello world!')
    """
    channels: List[str] = attr.ib(default=[])

    # Used for 'send_message()'
    slack_webhook_url: str = attr.ib(
        default=os.environ.get('SLACK_WEBHOOK_URL', ''))

    # Used for 'upload_file()'
    slack_upload_url: str = attr.ib(default=os.environ.get(
        'SLACK_UPLOAD_URL', 'https://slack.com/api/files.upload'))
    token: str = attr.ib(default=os.environ.get('SLACK_BOT_TOKEN', ''))

    def __attrs_post_init__(self):
        self._get_channels()

    def _get_channels(self):
        if len(self.channels) == 0:
            for channel in os.environ.get("SLACK_CHANNELS", "").split(","):
                self.channels.append(channel)

    def upload_file(self, file_name: str, file_path: str, file_extension: str):
        """ Upload a file to Slack

            TODO there's a bug somewhere that doesn't allow more than one slack channel,
            it will always post to last one in list.
        """
        my_file = {'file': (file_path, open(file_path, 'rb'), file_extension)}

        payload = {
            "filename": file_name,
            "token": self.token,
            "channels": self.channels,
        }
        try:
            resp = requests.post(self.slack_upload_url,
                                 params=payload,
                                 files=my_file)
        except Exception as e:
            logger.error(f"Failed to upload file ... {e}")
            return
        return resp

    def send_message(self,
                     msg,
                     title=None,
                     title_link=None,
                     pretext=None,
                     mrkdwn=True,
                     color="good"):
        """ Send a message (msg) to Slack.
            msg - Required message text
            title - Optional message title
            title_link - Optional link for message title
            pretext - Optional message pretext,
            mrkdwn - Whether markdown will be applied to message (default True)
            color - Color for edge of message
        """

        message_data = {"text": msg, "mrkdwn": mrkdwn, "color": color}

        if title is not None:
            message_data['title'] = title

        if title is not None and title_link is not None:
            message_data['title_link'] = title_link

        if pretext is not None:
            message_data['pretext'] = pretext

        slack_data = {"attachments": []}
        slack_data['attachments'].append(message_data)

        try:

            resp = requests.post(self.slack_webhook_url,
                                 data=json.dumps(slack_data),
                                 headers={'Content-Type': 'application/json'})

            if resp.status_code >= 300:
                logger.warning("Slack responded with non 200 code"
                               f"({resp.status_code}) "
                               f"with following message: {resp.text}")

        except _ConnectionError:
            logger.warning("Unable to post Slack notification")
            return None
        except Timeout:
            logger.warning("Request timed out while posting Slack "
                           "notification.")
            return None
        except Exception as e:
            logger.error(f"Unknown Exception: {e}")
            return None

        return resp


if __name__ == '__main__':  # pragma: no cover
    notifier = SlackNotifier()
    notifier.send_message('Testing...')

    # import tempfile
    # with tempfile.NamedTemporaryFile() as fp:
    #     fp.write(b'Hello world!')
    #     fp.seek(0)
    #     file_name = 'My Stats File...'
    #     file_path = fp.name
    #     file_extension = 'xlsx'
    #     resp = notifier.upload_file(file_name, file_path, file_extension)
    #     print(resp)
