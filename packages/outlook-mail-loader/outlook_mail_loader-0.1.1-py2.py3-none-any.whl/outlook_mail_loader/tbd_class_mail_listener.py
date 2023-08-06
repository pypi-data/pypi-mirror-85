"""
Module with class to listen to some outlook folder and dump all letters
to the local directory
"""
# Standard library imports
import logging
import datetime

# Third party imports
from char import char

# Local imports
from .class_mail_dumper import MailFolderDumper

LOGGER = logging.getLogger("outlook_mail_loader")

@char
def listen_outlook_mail_folder():
    """Class to dump some outlook folder with some periodic"""
    mail_loader_obj = MailFolderDumper()
    list_datetimes_when_letter_saved = []
    list_datetimes_when_letter_saved.append(datetime.datetime.now())
    return mail_loader_obj
