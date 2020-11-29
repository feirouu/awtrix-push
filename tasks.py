import os, configparser

from celery import Celery
from celery.schedules import crontab

from parse import default
from parse import custom


__version__ = "2.0.0"


config = configparser.RawConfigParser()
config.read(os.environ.get("CFG_PATH"))
default_config = dict(config.items("DEFAULT"))

app = Celery("tasks")
app.conf.update(default_config)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("===== Start add tasks =====")
    for section in config.sections():
        section_config = dict(config.items(section))
        if "crontab" in section_config and section_config["crontab"]:
            print(f"Add {section} task(crontab).")
            crontab_info = {}
            if "minute" in section_config:
                crontab_info.update(minute=section_config["minute"])
            if "hour" in section_config:
                crontab_info.update(hour=section_config["hour"])
            if "day_of_week" in section_config:
                crontab_info.update(day_of_week=section_config["day_of_week"])
            if "day_of_month" in section_config:
                crontab_info.update(day_of_month=section_config["day_of_month"])
            if "month_of_year" in section_config:
                crontab_info.update(month_of_year=section_config["month_of_year"])
            sender.add_periodic_task(crontab(**crontab_info),
                                        switch.s(section, section_config),
                                        name=f'RUN {section}')
        elif "seconds" in section_config:
            print(f"Add {section} task.")
            sender.add_periodic_task(float(section_config.get("seconds")),
                                        switch.s(section, section_config),
                                        name=f'RUN {section} every {section_config.get("seconds")} seconds')
    print("===== End add tasks =====")


@app.task
def switch(name, config):
    if "custom" in config and config["custom"]:
        return getattr(custom, name.lower())(config)
    return getattr(default, name.lower())(config)
