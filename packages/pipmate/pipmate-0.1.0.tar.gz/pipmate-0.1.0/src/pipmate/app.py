from commands import ConvCommand
from cleo import Application

application = Application()
application.add(ConvCommand())

if __name__ == "__main__":
    application.run()
