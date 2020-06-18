import os, configparser, json

import requests
from celery import Celery
from celery.schedules import crontab

import parse


__version__ = "1.1.0"


config = configparser.RawConfigParser()
config.read(os.environ.get("CFG_PATH"))
default_config = dict(config.items("DEFAULT"))

app = Celery("tasks")
app.conf.update(default_config)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("===== Start add tasks =====")
    for section in config.sections():
        print(f"Add {section} task.")
        section_config = dict(config.items(section))
        if "seconds" in section_config:
            sender.add_periodic_task(float(section_config.get("seconds")),
                                        switch.s(section, section_config),
                                        name=f'RUN {section} every {section_config.get("seconds")} seconds')
    print("===== End add tasks =====")


@app.task
def switch(name, data):
    getattr(parse, name.lower())(data)
