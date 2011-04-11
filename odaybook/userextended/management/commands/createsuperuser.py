# -*- coding: utf-8 -*-

"""
Management utility to create superusers.
Честно почти украдено из стандартной библиотеки Django
"""

import getpass
import re
import sys
from optparse import make_option
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from odaybook.userextended.models import Clerk, Superuser

RE_VALID_USERNAME = re.compile('[\w.@+-]+$')

EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

def is_valid_email(value):
    if not EMAIL_RE.search(value):
        raise exceptions.ValidationError(_('Enter a valid e-mail address.'))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username', dest='username', default=None,
            help='Specifies the username for the superuser.'),
        make_option('--email', dest='email', default=None,
            help='Specifies the email address for the superuser.'),
    )
    help = u'Создание технического администратора системы.'

    def handle(self, *args, **options):
        username = options.get('username', None)
        email = options.get('email', None)

        # If not provided, create the user with an unusable password
        password = None

        # Try to determine the current system user's username to use as a default.
        try:
            default_username = getpass.getuser().replace(' ', '').lower()
        except (ImportError, KeyError):
            # KeyError will be raised by os.getpwuid() (called by getuser())
            # if there is no corresponding entry in the /etc/passwd file
            # (a very restricted chroot environment, for example).
            default_username = ''

        # Determine whether the default username is taken, so we don't display
        # it as an option.
        if default_username:
            try:
                Clerk.objects.get(username=default_username)
            except Clerk.DoesNotExist:
                pass
            else:
                default_username = ''

        # Prompt for username/email/password. Enclose this whole thing in a
        # try/except to trap for a keyboard interrupt and exit gracefully.
        try:

            # Get a username
            while 1:
                if not username:
                    input_msg = u'Username'
                    if default_username:
                        input_msg += ' (Leave blank to use %r)' % default_username
                    username = raw_input(input_msg + u': ')
                if default_username and username == '':
                    username = default_username
                if not RE_VALID_USERNAME.match(username):
                    sys.stderr.write("Error: That username is invalid. Use only letters, digits and underscores.\n")
                    username = None
                    continue
                try:
                    Clerk.objects.get(username=username)
                except Clerk.DoesNotExist:
                    break
                else:
                    sys.stderr.write("Error: That username is already taken.\n")
                    username = None

            # Get an email
            while 1:
                if not email:
                    email = raw_input('E-mail address: ')
                try:
                    is_valid_email(email)
                except exceptions.ValidationError:
                    sys.stderr.write("Error: That e-mail address is invalid.\n")
                    email = None
                else:
                    break

            # Get a password
            while 1:
                if not password:
                    password = getpass.getpass()
                    password2 = getpass.getpass('Password (again): ')
                    if password != password2:
                        sys.stderr.write("Error: Your passwords didn't match.\n")
                        password = None
                        continue
                if password.strip() == '':
                    sys.stderr.write("Error: Blank passwords aren't allowed.\n")
                    password = None
                    continue
                break
        except KeyboardInterrupt:
            sys.stderr.write("\nOperation cancelled.\n")
            sys.exit(1)

        clerk = Clerk.objects.create_user(username, email, password)
        clerk.create_role(Superuser)
        self.stdout.write("Superuser created successfully.\n")

