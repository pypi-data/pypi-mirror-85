from cleo import Command
from parse.parser import parse


class ConvCommand(Command):
    """
    Generate new file from donor file

    transform
        {name? : Which file do we start from?}
        {destination? : And where should the new file be placed?}
        {--p|poetry : If set, a pyproject.toml will be created}
        {--i|pipfile : If set, a pipfile will be created}
        {--r|requirements : If set, a requirements.txt will be created}
    """

    def handle(self):
        opt = 0
        file_name = self.argument("name")

        if self.option("poetry"):
            opt = 1

        elif self.option("pipfile"):
            opt = 2

        elif self.option("requirements"):
            opt = 3

        if file_name:
            pass
        else:
            self.line("A source file has to be provided! Check help for more details")
            exit()

        if opt:
            v = parse(file_name, opt)
            if v == -1:
                self.line("Invalid file name or extension")
                exit()
            elif v == -2:
                self.line("Can't have the same source and destination type")
                exit()
        else:
            self.line(
                "A destination file option has to be provided! Check help for more details"
            )
