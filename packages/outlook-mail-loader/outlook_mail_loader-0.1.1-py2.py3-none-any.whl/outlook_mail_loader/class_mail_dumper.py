"""
Module with main class of this python package
to dump outlook mail to local folder
"""
# Standard library imports
import os
import logging

# Third party imports
import win32com.client
from char import char
from local_simple_database import LocalSimpleDatabase

# Local imports
from .exceptions import OutlookMailLoaderError
from .class_outlook_message import OutlookLMessageSaver
from . import recursive

LOGGER = logging.getLogger("outlook_mail_loader")


class MailFolderDumper(object):
    """Object which handles all outlook mail dump to local folder

    Data:
        self.str_folder_to_get (str): Folder name which to dump
        self.str_path_dir_where_to_save (str): Path where to dump

    Methods:
        self.dump_new(...): Dump new letters to set local directory
        self.print_stats_about_initialized_folders(...):\
            Print hierarchy for initialized outlook mail folder
        self.print_full_folders_hierarchy_from_root(...):\
            Print full hierarchy from root outlook mail folder

    Raises:
        OutlookMailLoaderError: Main Exception of this python package

    """

    @char
    def __init__(
            self,
            str_folder_to_get="inbox",
            str_path_dir_where_to_save="mails",
    ):
        """Init object

        Args:
            str_folder_to_get (str, optional): Folder name to get
            str_path_dir_where_to_save (str, optional): Path where to save
        """
        self.str_folder_to_get = str_folder_to_get
        self._outlook_obj = win32com.client.Dispatch("Outlook.Application")\
            .GetNamespace("MAPI")
        self._outlook_root_folder_handler = self._outlook_obj.Folders.Item(1)
        if self.str_folder_to_get == "root":
            self._outlook_folder_handler = \
                self._outlook_root_folder_handler.Folders(1)
        elif self.str_folder_to_get == "inbox":
            self._outlook_folder_handler = self._outlook_obj.GetDefaultFolder(6)
        else:
            self._outlook_folder_handler = self._get_folder_outlook_handler()

        # As folder handler initialized then create folder where to save mails
        self.str_path_dir_where_to_save = os.path.abspath(
            os.path.join(str_path_dir_where_to_save, str_folder_to_get))
        if not os.path.isdir(self.str_path_dir_where_to_save):
            os.makedirs(self.str_path_dir_where_to_save)
            LOGGER.debug(
                "Created a directory to save all letters: %s",
                self.str_path_dir_where_to_save
            )
        self._local_database = \
            LocalSimpleDatabase(self.str_path_dir_where_to_save)
        logging.info("Mail loader object initialized")

    def dump_new(
            self,
            int_max_last_letters_to_dump=10,
            is_to_mark_messages_as_read=False,
            is_to_remove_attachments=False,
            is_to_preserve_msg_obj=False,
    ):
        """Dump new letters to set local directory

        Args:
            int_max_last_letters_to_dump (int, optional): Max new mails to load
            is_to_mark_messages_as_read (bool, optional): \
                Flag if to mark as read saved letters
            is_to_remove_attachments (bool, optional): \
                Flag if to remove attachments to save disk space
            is_to_preserve_msg_obj (bool, optional): \
                Flag if to preserve outlook .msg object for letter

        Returns:
            int: Number of letters saved
        """
        list_last_messages = list(
            self._get_list_last_not_saved_messages(int_max_last_letters_to_dump))
        for message_obj in list_last_messages:
            # Create path where to save new LETTER
            str_new_mail_dir = os.path.join(
                self.str_path_dir_where_to_save,
                "LETTER_%d" % (self._local_database["int_last_letter_num"] + 1)
            )
            message_obj.save_message(
                str_new_mail_dir,
                is_to_remove_attachments=is_to_remove_attachments,
                is_to_preserve_msg_obj=is_to_preserve_msg_obj,
                is_to_mark_messages_as_read=is_to_mark_messages_as_read
            )

            self._local_database["int_last_letter_num"] += 1
        #####
        # Save Received time for last letter
        if list_last_messages:
            self._local_database["datetime_last_letter_receive_time"] = \
                list_last_messages[-1].datetime_received
        LOGGER.debug("Were dumped new messages: %d", len(list_last_messages))
        return len(list_last_messages)

    def print_stats_about_initialized_folders(self):
        """Print hierarchy for initialized outlook mail folder
        """
        LOGGER.info("Statistics about initialized dirs.")
        recursive.print_hierarchy(
            self._outlook_folder_handler, int_depth_level=1)

    def print_full_folders_hierarchy_from_root(self):
        """Print full hierarchy from root outlook mail folder
        """
        recursive.print_hierarchy(
            self._outlook_root_folder_handler, int_depth_level=1)

    def _get_folder_outlook_handler(self):
        """Get outlook folder handler for folder with asked name

        Raises:
            OutlookMailLoaderError:  Main Exception of this python package
        """
        outlook_folder_handler = recursive.look_for_asked_mail_folders(
            self._outlook_root_folder_handler,
            self.str_folder_to_get,
        )
        if outlook_folder_handler:
            return outlook_folder_handler
        LOGGER.warning(
            "Unable to find outlook folder with name: %s",
            self.str_folder_to_get
        )
        raise OutlookMailLoaderError(
            "Unable to find outlook folder: %s" % self.str_folder_to_get)

    def _get_list_last_not_saved_messages(self, int_max_mails_to_get=10):
        """Get last not saved messages in the order oldest -> newest

        Args:
            int_max_mails_to_get (int, optional): Max last mails to get

        Returns:
            list: [outlook_message_obj_1, outlook_message_obj_2, ...]
        """
        LOGGER.debug(
            "Get last %d unsaved letters for folder: %s",
            int_max_mails_to_get,
            self.str_folder_to_get
        )
        list_last_messages = []
        messages = self._outlook_folder_handler.Items
        messages.Sort("[ReceivedTime]", True)
        for outlook_message_obj in messages:
            if len(list_last_messages) >= int_max_mails_to_get:
                LOGGER.info(
                    "For folder: %s Got max number of emails: %d",
                    self.str_folder_to_get,
                    int_max_mails_to_get,
                )
                break
            message_obj = OutlookLMessageSaver(outlook_message_obj)
            dt_received = message_obj.datetime_received
            if dt_received <= \
            self._local_database["datetime_last_letter_receive_time"]:
                break
            list_last_messages.append(message_obj)
        LOGGER.debug("---> Were Got %d last letters", len(list_last_messages))
        return reversed(list_last_messages)
