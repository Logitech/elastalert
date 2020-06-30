import requests

from requests.exceptions import RequestException

from elastalert.alerts import Alerter, BasicMatchString
from elastalert.util import elastalert_logger

class SlackCustomAlert(Alerter):
    # By setting required_options to a set of strings
    # You can ensure that the rule config file specifies all
    # of the options. Otherwise, ElastAlert will throw an exception
    # when trying to load the rule.
    required_options = set(['slack_webhook_url'])

    def __init__(self, rule):
        super(SlackCustomAlert, self).__init__(rule)
        self.slack_webhook_url = self.rule['slack_webhook_url']
        self.slack_title = self.rule.get('slack_title', '')

    # Alert is called
    def alert(self, matches):

        # Matches is a list of match dictionaries.
        # It contains more than one match when the alert has
        # the aggregation option set
        for match in matches:
            elastalert_logger.info("Received match %s" % (match))
            # post to slack
            headers = {'content-type': 'application/json'}
            payload ={
               "blocks":[
                  {
                     "type":"section",
                     "text":{
                        "type":"mrkdwn",
                        "text":"*{slack_title}*".format(slack_title = self.slack_title)
                     }
                  },
                  {
                     "type":"section",
                     "fields":[
                        {
                           "type":"mrkdwn",
                           "text":"*Application:*\n{instance-tag}".format(instance-tag = match['instance-tag'])
                        },
                        {
                           "type":"mrkdwn",
                           "text":"*Time in IST:*\n{timestamp-ist}".format(timestamp-ist = match['@timestamp-ist']
                        },
                        {
                           "type":"mrkdwn",
                           "text":"*Time in CST:*\n{timestamp-cst}".format(timestamp-cst = match['@timestamp-cst']
                        },
                        {
                           "type":"mrkdwn",
                           "text":"*Time in UTC00Z:*\n{timestamp}".format(timestamp = match['@timestamp']
                        }
                     ]
                  },
                  {
                     "type":"actions",
                     "elements":[
                        {
                           "type":"button",
                           "text":{
                              "type":"plain_text",
                              "emoji":true,
                              "text":"Send Incident Response"
                           },
                           "style":"primary",
                           "value":"click_me_123"
                        }
                     ]
                  }
               ]
            }
            try:
                response = requests.post(
                    self.slack_webhook_url, data=json.dumps(payload),
                    headers=headers)
                response.raise_for_status()
            except RequestException as e:
                raise EAException("Error posting to slack: %s" % e)

        elastalert_logger.info("Alert '%s' sent to Slack" % self.rule['name'])


    def get_info(self):
        return {'type': 'slack'}
