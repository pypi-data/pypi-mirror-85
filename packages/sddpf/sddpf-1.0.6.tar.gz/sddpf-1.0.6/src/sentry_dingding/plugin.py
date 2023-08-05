# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'lcfevr'
    author_url = 'https://github.com/lcfevr/sentry-dingding-feelys'
    version = sentry_dingding.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'https://github.com/lcfevr/sentry-dingding-feelys'),
        ('Bug Tracker', 'https://github.com/lcfevr/sentry-dingding-feelys/issues'),
        ('README', 'https://github.com/lcfevr/sentry-dingding-feelys/blob/master/README.md'),
    ]

    slug = 'DingDing'
    title = 'DingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = "New alert from {}".format(event.project.slug)
        event_url = "{0}events/{1}/".format(group.get_absolute_url(), event.id)
        url_arr = event_url.split('/')
        print(url_arr)
        issue_id = url_arr[url_arr.index('issues') + 1]
        print(issue_id)
        issue_data = requests.get(
            "http://web-middle.ruibogyl.work/sentry/findIssueTargetUrl",
            {"id": issue_id},
            headers={}
        ).json()
        print issue_data
        response = requests.get(
            "http://web-middle.ruibogyl.work/sentry/getDingDingAssignee",
            {"url": issue_data["data"]["url"]},
            headers={}
        ).json()
        print response["data"]["phone"]

        requests.get(
            "http://web-middle.ruibogyl.work/sentry/changeIssueAssignee",
            {"name": response["data"]["userName"], "issueId": issue_id, "orgName": "ruibogyl"},
            headers={}
        )

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": "#### {title} \n > {message} \n [点击查看问题]({event_url}) \n @{phone}".format(
                    title=title,
                    message=event.message,
                    event_url=event_url,
                    phone=response["data"]["phone"],
                ),
            },
            "at": {
                "atMobiles": [
                    response["data"]["phone"]
                ],
                "isAtAll": False
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )

