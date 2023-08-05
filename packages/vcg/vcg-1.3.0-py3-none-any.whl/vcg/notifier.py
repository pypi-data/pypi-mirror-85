# -*- coding: utf-8 -*-
# @Time    : 2019/3/29 16:25
# @Author  : Yinglin Zheng
# @Email   : zhengyinglin@stu.xmu.edu.cn
# @FileName: notifier.py
# @Software: PyCharm
# @Affiliation: VCG@XMU

import socket
import sys
import traceback
from typing import List
from contextlib import contextmanager
import zmail
from zmail.structures import CaseInsensitiveDict

default_server = {"email": "robot@hypercube.top", "password": "gW05I9SYhPrH"}


class Notifier:
    def __init__(self, recipients: List[str] or str, server=None):
        if server is None:
            server = default_server
        self.server = zmail.server(server["email"], server["password"])
        self.recipients = recipients
        self.program_name = sys.argv[0]
        self.computer_name = socket.gethostname()
        self.basic = "Program {} on computer {}".format(
            self.program_name, self.computer_name
        )
        self.end = "\n\nWish you a good day.\nVisual Computing and Graphics Group, Xiamen University, China"

    @staticmethod
    def _organize_extra(extra: str) -> str:
        if extra != "":
            return "\nExtra Info:\n" + extra
        else:
            return ""

    def on_finished(self, extra: str = "") -> bool:
        extras = self._organize_extra(extra)
        return self.server.send_mail(
            self.recipients,
            {
                "subject": "Finish Notification from " + self.computer_name,
                "content_text": "Hi,\n" + self.basic + " finished" + extras + self.end,
                "from": "VCG@XMU <robot@hypercube.top>",
            },
        )

    def on_error(self, extra="") -> bool:
        tb = traceback.format_exc()
        extras = self._organize_extra(extra)

        return self.server.send_mail(
            self.recipients,
            {
                "subject": "Exception Notification from " + self.computer_name,
                "content_text": "Hi, something wrong with "
                + self.basic
                + "\nThe error info are as follow:\n"
                + str(tb)
                + extras
                + self.end,
                "from": "VCG@XMU <robot@hypercube.top>",
            },
        )

    def send_mail(
        self,
        recipients: List[str] or str,
        mail: dict or CaseInsensitiveDict,
        cc=None,
        timeout=None,
        auto_add_from=True,
        auto_add_to=True,
    ) -> bool:
        return self.server.send_mail(
            recipients, mail, cc, timeout, auto_add_from, auto_add_to
        )

    def send(self, content):
        self.server.send_mail(
            self.recipients,
            {
                "subject": "Notification from " + self.computer_name,
                "content_text": str(content) + self.end,
                "from": "VCG@XMU <robot@hypercube.top>",
            },
        )


@contextmanager
def notify(recipients: List[str] or str, debug=False, server=None):
    if server is None:
        server = default_server
    notifier = Notifier(recipients, server=server)
    try:
        yield
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        if not debug:
            notifier.on_error()
        raise e
    else:
        if not debug:
            notifier.on_finished()


if __name__ == "__main__":
    with notify("admin@hypercube.top", debug=True):
        raise NotImplementedError
