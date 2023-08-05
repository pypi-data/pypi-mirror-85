from selenium import webdriver


class Config:
    # global setting
    DRIVER: webdriver
    # enum: headless or usual
    MODE: str
    # large time judgment conditions
    TIMEOUT: int = 6
    # base url
    URL: str
    # desktop size
    WIDTH: int
    HEIGHT: int
