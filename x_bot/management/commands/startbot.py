from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts the telegram bot'

    def handle(self, *args, **options):
        from x_bot.initializer import app
        app.run()
