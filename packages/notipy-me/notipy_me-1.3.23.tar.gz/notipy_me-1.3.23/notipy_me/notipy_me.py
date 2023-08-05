from contextlib import ContextDecorator
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from datetime import datetime
import socket
import getpass
from typing import List, Dict, Callable, Tuple, Union
import humanize
import time
import pandas as pd
from validators import domain
from environments_utils import is_stdout_enabled
from tabulate import tabulate
from validate_email import validate_email
from humanize import naturaldelta
import sys
import warnings
from traceback import format_tb
from userinput import userinput, set_validator, can_start, clear


class Notipy(ContextDecorator):
    __SINGLE_RUN__ = ".single_run"

    def __init__(
        self,
        setup_single_run: bool = False,
        task_name: str = None
    ):
        """Create a new istance of Notipy."""
        super(Notipy, self).__init__()
        self._enabled = False
        self._task_name = task_name
        if os.path.exists(self.__SINGLE_RUN__) or setup_single_run or can_start("Press CTRL+C to start notipy within {i} seconds..."):
            self._setup(setup_single_run)
        self._report = self._interrupt_txt = self._interrupt_html = None

    def _setup(self, setup_single_run: bool = False):
        self._enabled = True
        clear()
        print("Let's setup your notipy!")
        self._always_use_default = userinput(
            "always_use_default",
            label="Should I always use the defaults?",
            default="yes" if setup_single_run else "no",
            sanitizer="human_bool",
            cache_path=self.__SINGLE_RUN__,
            validator="human_bool",
            auto_clear=True,
            always_use_default=os.path.exists(
                self.__SINGLE_RUN__) or setup_single_run
        )

        delete_password = userinput(
            "delete_password",
            label="Should I delete your password after usage?",
            default="yes",
            sanitizer="human_bool",
            cache_path=self.__SINGLE_RUN__,
            validator="human_bool",
            auto_clear=True,
            always_use_default=not setup_single_run
        )

        self._email = userinput(
            "email",
            validator="email",
            cache_path=".notipy",
            always_use_default=self._always_use_default
        )

        self._password = userinput(
            "password",
            cache_path=self.__SINGLE_RUN__,
            validator="non_empty",
            hidden=True,
            delete_cache=delete_password,
            auto_clear=True,
            always_use_default=os.path.exists(self.__SINGLE_RUN__)
        )
        self._send_start_email = userinput(
            "start_email",
            label="Should I send a start email too?",
            default="yes",
            sanitizer="human_bool",
            cache_path=".notipy",
            validator="human_bool",
            always_use_default=self._always_use_default,
            auto_clear=True
        )
        self._task_name = userinput(
            "task name",
            default=self._task_name,
            validator="non_empty",
            cache=self._task_name is None,
            cache_path=".notipy",
            always_use_default=self._always_use_default,
            auto_clear=True
        )
        self._recipients = userinput(
            "recipients", default=self._email,
            label="Please insert {name}, separated by a comma",
            cache_path=".notipy",
            validator=lambda x: all([
                validate_email(email) for email in x.split(",")
            ]),
            always_use_default=self._always_use_default,
            auto_clear=True
        ).split(",")
        timeouts = {
            "hours": 24,
            "minutes": 30,
            "seconds": 120
        }
        self._report_timeout_unit = userinput(
            "report_timeout_unit",
            label="Please insert {{name}}, choosing from {choices}".format(
                choices=", ".join(timeouts.keys())
            ),
            cache_path=".notipy",
            default="hours",
            validator=set_validator(timeouts.keys()),
            always_use_default=self._always_use_default,
            auto_clear=True
        )
        self._report_timeout = int(userinput(
            "report_timeout",
            label="Please insert {{name}} in {unit}".format(
                unit=self._report_timeout_unit
            ),
            cache_path=".notipy",
            default=timeouts[self._report_timeout_unit],
            validator="positive_integer",
            always_use_default=self._always_use_default,
            auto_clear=True
        ))
        self._port = int(userinput(
            "port",
            default=465,
            validator="positive_integer",
            cache_path=".notipy",
            always_use_default=self._always_use_default,
            auto_clear=True
        ))
        self._smtp_server = userinput(
            "smtp_server",
            default="smtp.{server}".format(server=".".join(
                self._email.split("@")[1].split(".")[-2:])),
            validator="hostname",
            cache_path=".notipy",
            always_use_default=self._always_use_default,
            auto_clear=True
        )

    def _notify(self, subject: str, txt: str, html: str):
        try:
            server_ssl = SMTP_SSL(self._smtp_server, self._port)
            server_ssl.login(self._email, self._password)
            msg = MIMEMultipart('alternative')
            msg["Subject"] = subject
            msg["To"] = ", ".join(self._recipients)
            msg["From"] = self._email
            msg.attach(MIMEText(txt, 'plain'))
            msg.attach(MIMEText(html, 'html'))
            server_ssl.sendmail(msg["From"], self._recipients, msg.as_string())
            server_ssl.close()
        except Exception:
            warnings.warn("Unable to send email with subject '{subject}'!".format(
                subject=subject
            ))
        

    @property
    def _pwd(self):
        return os.path.dirname(os.path.realpath(__file__))

    def _load_model(self, name: str, ext: str):
        with open("{pwd}/models/{name}.{ext}".format(pwd=self._pwd, name=name, ext=ext), "r") as f:
            return f.read()

    def _json(self, name: str, ext: str) -> Dict:
        common = json.loads(self._load_model("common", "json"))
        generic = json.loads(self._load_model(name, "json"))
        extension = json.loads(self._load_model(ext, "json"))
        return {**common, **generic, **extension}

    def _start(self):
        self._notify(  # pylint: disable=no-value-for-parameter
            *self._build_models("start")
        )

    def _completed(self):
        self._notify(  # pylint: disable=no-value-for-parameter
            *self._build_models("completed")
        )

    def _interruption(self):
        self._notify(  # pylint: disable=no-value-for-parameter
            *self._build_models("interruption")
        )

    def _send_report(self):
        self._notify(  # pylint: disable=no-value-for-parameter
            *self._build_models("report")
        )

    def _format_traceback(self, tb, value):
        self._interrupt_txt = "\n".join(format_tb(tb)) + str(value)
        self._interrupt_html = self._interrupt_txt.replace("\n", "<br>")

    def _info(self) -> Dict:
        return {
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "pwd": os.getcwd(),
            "elapsed": humanize.naturaldelta(time.time() - self._start_time),
            "now": datetime.now().date(),
            "interrupt_txt": "" if self._interrupt_txt is None else self._interrupt_txt,
            "interrupt_html": "" if self._interrupt_html is None else self._interrupt_html,
            "report_html": "" if self._report is None else self._report.tail().to_html(),
            "report_txt": "" if self._report is None else tabulate(self._report.tail(), tablefmt="pipe", headers="keys"),
            "email": self._email,
            "task_name": self._task_name
        }

    def _build_models(self, name: str) -> Tuple[str, str, str]:
        info = self._info()
        models = []
        for ext in ("txt", "html"):
            data = self._json(name, ext)
            model = self._load_model("basic", ext)
            for k, v in data.items():
                if isinstance(v, list):
                    if ext == "txt":
                        v = "\n".join(v)
                    if ext == "html":
                        v = "<br>".join(v)
                v = v.format(**info)
                model = model.replace(k, v)
                data[k] = v
            models.append(model)
        return (data["model_subject"], *models)

    def add_report(
        self,
        report: Union[pd.DataFrame, Dict],
        add_elapsed_time: bool = True
    ):
        """Add given report to the Notipy object to send via email.

        Parameters
        --------------------------
        report: Union[pd.DataFrame, Dict],
            The report to be added to Notipy.
        add_elapsed_time: bool = True,
            Wether to add metadata relative to how much time has
            elapsed since either start or last report.
            The metadata are added both for the time in seconds and the time
            in human-readable strings.
        """
        if not self._enabled:
            return
        if isinstance(report, Dict):
            try:
                report = pd.DataFrame(report)
            except ValueError:
                report = pd.DataFrame(report, index=[0])

        if add_elapsed_time:
            delta = time.time() - self._last_report
            report["elapsed_time"] = delta
            report["human_elapsed_time"] = naturaldelta(delta)

        self._last_report = time.time()

        self._report = (report if self._report is None else pd.concat([
            self._report, report
        ])).reset_index(drop=True)
        if time.time() - self._last_sent_report > self._report_timeout*{
            "hours": 60*60,
            "minutes": 60,
            "seconds": 1
        }[self._report_timeout_unit]:
            self._last_sent_report = time.time()
            self._send_report()

    def enter(self):
        if self._enabled:
            self._start_time = time.time()
            self._last_report = time.time()
            self._last_sent_report = time.time()
            if self._send_start_email:
                self._start()
        return self

    def __enter__(self):
        return self.enter()

    def exit(self, exc_type=None, exc_val=None, traceback=None):
        if not self._enabled:
            return
        if exc_type is not None and exc_type is not KeyboardInterrupt:
            self._format_traceback(traceback, exc_val)
            self._interruption()
        elif exc_type is None:
            self._completed()

    def __exit__(self, exc_type, exc_val, traceback):
        self.exit(exc_type, exc_val, traceback)
