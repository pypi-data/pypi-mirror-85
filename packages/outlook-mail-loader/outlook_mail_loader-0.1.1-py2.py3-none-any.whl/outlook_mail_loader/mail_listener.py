"""
Module with class to listen to some outlook folder and dump all letters
to the local directory
"""
# Standard library imports
from __future__ import division
import logging
import datetime
from time import sleep

# Third party imports
from char import char
from tqdm import tqdm
try:
    from IPython.display import clear_output
    bool_jupyter_installed = True
except ImportError:
    bool_jupyter_installed = False

# Local imports
from .class_mail_dumper import MailFolderDumper

LOGGER = logging.getLogger("outlook_mail_loader")

@char
def listen_outlook_mail_folder(
        str_folder_to_get="inbox",
        str_path_dir_where_to_save="mails",
        int_seconds_step_in_dump=60,
):
    """Class to dump some outlook folder with some periodic"""
    list_datetimes_when_letter_saved = []
    mail_loader_obj = MailFolderDumper()
    mail_loader_obj = MailFolderDumper(
        str_folder_to_get, str_path_dir_where_to_save)
    #####
    # Make first dump of the last mails
    int_msgs_saved = mail_loader_obj.dump_new(20)
    list_datetimes_when_letter_saved += \
        [datetime.datetime.now()] * int_msgs_saved
    print_stats_about_dumped_mails(list_datetimes_when_letter_saved)
    #####
    # Create endless cycle of listening
    while True:
        for _ in tqdm(range(int_seconds_step_in_dump), leave=False):
            sleep(1)
        int_msgs_saved = mail_loader_obj.dump_new(999)
        list_datetimes_when_letter_saved += \
            [datetime.datetime.now()] * int_msgs_saved
        print_stats_about_dumped_mails(list_datetimes_when_letter_saved)
    return mail_loader_obj


@char
def print_stats_about_dumped_mails(list_datetimes_when_letter_saved):
    """"""
    # if bool_jupyter_installed:
    #     clear_output(wait=True)
    LOGGER.info("=" * 79)
    LOGGER.info("Print statistic about saved letters:")
    if not list_datetimes_when_letter_saved:
        LOGGER.info("---> Not even 1 new letter has been received yet.")
        return
    LOGGER.info(
        "Overall letters saved: %d", len(list_datetimes_when_letter_saved))
    #####
    # Get sorted list with number of seconds gone since msg saved
    dt_now = datetime.datetime.now()
    list_seconds_gone_since_saved = [
        int((dt_now - dt_msg_saved).total_seconds())
        for dt_msg_saved in list_datetimes_when_letter_saved]
    list_seconds_gone_since_saved.sort()
    #####
    # Try to print nice stats
    int_max_index_used = 0
    int_max_index = len(list_seconds_gone_since_saved)
    #####
    # Minutes
    list_minutes = [3, 10, 30, 60]
    for int_minutes_end in list_minutes:
        for int_cur_index in range(int_max_index_used, int_max_index):
            int_cur_elem = list_seconds_gone_since_saved[int_cur_index]
            if int_cur_elem / 60 <= int_minutes_end:
                int_max_index_used = int_cur_index
        LOGGER.info(
            "---> Letters saved in the last %d minutes: %d",
            int_minutes_end, int_max_index_used + 1)
        if int_cur_index == int_max_index - 1:
            return
    #####
    # Hours
    list_hours = [2, 3, 6, 12, 24, 24*2, 24*3, 24*4]
    for int_hours_end in list_hours:
        for int_cur_index in range(int_max_index_used, int_max_index):
            int_cur_elem = list_seconds_gone_since_saved[int_cur_index]
            if int_cur_elem / 3600 <= int_hours_end:
                int_max_index_used = int_cur_index
        LOGGER.info(
            "---> Letters saved in the last %d hours: %d",
            int_hours_end, int_max_index_used + 1)
        if int_cur_index == int_max_index - 1:
            return

    LOGGER.info(
        "---> Letters saved more than 96 hours ago: %d",
        int_max_index - 1 - int_cur_index)
