# pylint: disable=line-too-long
import click
import inquirer

from booknot.booknot_storage.booknot_storage import BooknotStorage

class InitApplication:

    def __init__(self, booknot_storage: BooknotStorage):
        self.booknot_storage = booknot_storage

    def run(self):

        if self.booknot_storage.exists():
            raise click.ClickException('.booknot already exists')

        if not self.booknot_storage.is_sphinx_present():
            questions = [
                inquirer.Confirm('init sphinx',
                                 message='This will bootstrap a workspace for sphinx in this directory, do you want to continue ?',
                                 default=False),
            ]

            answers = inquirer.prompt(questions)
            if answers['init sphinx']:
                questions = [
                    inquirer.Text('project',
                                     message='What the name of this booknot',
                                     default='Booknot'),
                    inquirer.Text('author',
                                     message='What the name of the author',
                                     default='me'),
                ]

                answers = inquirer.prompt(questions)
                self.booknot_storage.create_sphinx(answers['project'], answers['author'])

                click.echo(click.style("1. to render the booknot, use : make html", fg='yellow'))
                click.echo(click.style("2. to open the booknot after rendering, use a browser and open _build/html/index.html", fg='yellow'))
                self.booknot_storage.init_store()
                click.echo(click.style("3. to bookmark a page, use : booknot capture https://...", fg='yellow'))
        else:
            self.booknot_storage.init_store()
            click.echo(click.style("1. to bookmark a page, use : booknot capture https://...", fg='yellow'))
