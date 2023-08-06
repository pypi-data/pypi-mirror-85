""" Test Slack tooling
"""
from sermos_tools.catalog.slack_notifier import SlackNotifier


class TestToolsSlackNotifier:
    """ Test SlackNotifier
    """
    def test_slack_notifier_no_env(self):
        """ Test loading PDF object bytes from S3 and generating its hash.
        """
        notifier = SlackNotifier()
        assert notifier.channels == ['']
        assert notifier.slack_webhook_url == ''
        assert notifier.slack_upload_url == 'https://slack.com/api/files.upload'
        assert notifier.token == ''
