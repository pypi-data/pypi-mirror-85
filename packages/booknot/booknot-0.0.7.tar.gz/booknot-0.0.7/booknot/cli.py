#!/usr/bin/python
# coding=utf-8

from __future__ import print_function

import os

import click
import requests
from bs4 import BeautifulSoup

from booknot.application.init_application import InitApplication
from booknot.application.capture_application import CaptureApplication
from booknot.booknot_storage.local_booknot_storage import LocalBooknotStorage
from booknot.crawler.http_crawler import HttpCrawler


@click.group()
def cli():
    pass


@click.command('init')
def init():
    workdir = os.getcwd()
    booknot_storage = LocalBooknotStorage(workdir)
    init_application = InitApplication(booknot_storage)

    # init booknot root
    init_application.run()


@click.command('capture')
@click.argument('url')
def capture(url):
    workdir = os.getcwd()
    session = requests.Session()
    crawler = HttpCrawler(session)
    capture_application = CaptureApplication(crawler, workdir, url)
    capture_application.run()


cli.add_command(init)
cli.add_command(capture)

if __name__ == '__main__':
    cli()
