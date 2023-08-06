from datetime import datetime
from pathlib import Path

import allure
import pymysql as pymysql
import yaml


class MySQLHandler:
    def __init__(self, config: dict):
        self.config = config

    @property
    def db(self):
        return pymysql.connect(
            host=self.config.get("host"),
            port=int(self.config.get("port")),
            database=self.config.get("database"),
            user=self.config.get("user"),
            password=self.config.get("password"),
            charset="utf8",
            autocommit=True,
        )

    @property
    def cursor(self):
        return self.db.cursor()

    def sql(self, sql):
        return self.cursor.execute(sql)

    def yml(self, yml):
        if Path.exists(yml):
            yml = YmlHandler(yml).parameters
        for name, value in yml.items():
            self.sql(sql=value)
        self.cursor.close()
        self.db.close()


yaml.warnings({"YAMLLoadWarning": False})


class YmlHandler:
    def __init__(self, file):
        if Path(file).exists():
            self.file = file
            self.yc = None
        else:
            raise FileNotFoundError

    def __getitem__(self, key: str = None):
        return str(self.yc[key]) if key in self.yc else None

    @property
    def parameters(self):
        with open(str(self.file), "rb") as yf:
            self.yc = yaml.safe_load(yf)
        return dict(self.yc)


class AllureHandler:
    def __init__(self, driver):
        self.driver = driver

    def png(self):
        timing = datetime.now().strftime("%Y%m%d%H%M%S")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            f"Exception at {timing}",
            allure.attachment_type.PNG,
        )
