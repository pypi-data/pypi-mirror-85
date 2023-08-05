import click
from click_help_colors import HelpColorsCommand

import unittest
from pyunitreport import HTMLTestRunner
import stf.common.config as common_config
import stf.common.filesystem as common_filesystem
import importlib
import os
import sys

sys.path.insert(1, os.getcwd())


@click.command(
    cls=HelpColorsCommand,
    help_headers_color='yellow',
    help_options_color='green',
)
@click.argument('suite')
@click.option('-e', '--environment', 'environment')
@click.option('-b', '--browser', 'browser', required=False, default="chrome", type=click.Choice(['chrome', 'firefox']))
def run(suite, environment, browser):
    click.echo(click.style("Suite: %s" % (suite), fg='blue'))
    click.echo(click.style("Environment: %s" % (environment), fg='blue'))
    click.echo(click.style("Browser: %s" % (browser), fg='blue'))

    module = importlib.import_module(common_filesystem.tests_folder + '.' + suite)
    class_ = getattr(module, 'TestCase')

    tests = unittest.TestLoader().getTestCaseNames(class_)
    test_suite = unittest.TestSuite()

    test_config = common_config.get_config(os.getcwd())

    for test_name in tests:
        click.echo(click.style("Test: %s" % (test_name), fg='red'))
        test_suite.addTest(class_(test_name, test_config, environment, browser))

    try:
        HTMLTestRunner(
            verbosity=2,
            output="./" + suite,
            report_name='report',
            report_title='Acceptance Test Report'
        ).run(test_suite)
    except:
        print('Failure!')


@click.command(
    cls=HelpColorsCommand,
    help_headers_color='yellow',
    help_options_color='green',
)
@click.argument('name')
@click.option('-t', '--type', 'type', required=False, default="simple", type=click.Choice(common_config.suite_types))
def create(name, type):
    if common_filesystem.create_test_folder():
        click.secho('Test folder created successfully', fg='green')
    else:
        click.secho('Test folder already exists. Skipping creation...')

    new_suite_file = common_filesystem.copy_sample_test(name, type)
    click.secho("Test suite created successfully", fg='green')
    click.secho("Please check new file: %s" % new_suite_file, fg='blue')
