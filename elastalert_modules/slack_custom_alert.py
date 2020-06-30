from elastalert.alerts import Alerter, BasicMatchString
from elastalert.util import elastalert_logger

class SlackCustomAlert(Alerter):
    # By setting required_options to a set of strings
    # You can ensure that the rule config file specifies all
    # of the options. Otherwise, ElastAlert will throw an exception
    # when trying to load the rule.
    required_options = set(['slack_webhook_url'])

    # Alert is called
    def alert(self, matches):

        # Matches is a list of match dictionaries.
        # It contains more than one match when the alert has
        # the aggregation option set
        for match in matches:
            elastalert_logger.info("Received match %s" % (match))

    def get_info(self):
        return {'type': 'Slack Alerter',
                'channel': 'test'}
