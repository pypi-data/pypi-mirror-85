"""Module with 2 classes to contain and process outlook messages"""
# Standard library imports
import os
import logging
import datetime
from collections import OrderedDict
import json
from io import open

# Third party imports
import dateutil.parser

# Local imports

LOGGER = logging.getLogger("outlook_mail_loader")
LOCAL_TIMEZONE = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo


class OutlookLMessageSaver(object):
    """[summary]

    Data:
        self.msg_handler (win32com object for letter): letter handler
        self.datetime_received (datetime): datetime when msg received

    Methods:
        self.save_message(...): Save current message to the asked directory
    """

    def __init__(self, msg_handler,):
        """Initialize object for current letter

        Args:
            msg_handler (outlook msg handler): win32com object for letter
        """
        self.msg_handler = msg_handler
        str_received_time = str(self.msg_handler.ReceivedTime)
        self.datetime_received = dateutil.parser.parse(str_received_time)

    def save_message(
            self,
            str_path_dir_where_to_save,
            is_to_remove_attachments=False,
            is_to_preserve_msg_obj=True,
            is_to_mark_messages_as_read=False
    ):
        """Save this letter to the given directory

        Args:
            str_path_dir_where_to_save (str): Directory where to save letter
            is_to_remove_attachments (bool, optional): \
                Flag if to remove attachments to save disk space
            is_to_preserve_msg_obj (bool, optional): \
                Flag if to preserve outlook .msg object for letter
            is_to_mark_messages_as_read (bool, optional): \
                Flag if to mark as read saved letters
        """
        LOGGER.debug(
            "Saved outlook message to dir: %s", str_path_dir_where_to_save)
        if not os.path.exists(str_path_dir_where_to_save):
            os.makedirs(str_path_dir_where_to_save)
        #####
        # Save all asked items
        if is_to_preserve_msg_obj:
            str_path_msg = os.path.join(
                str_path_dir_where_to_save, "outlook_message.msg")
            self.msg_handler.SaveAs(Path=str_path_msg)
        self._save_letter_metainfo(str_path_dir_where_to_save)
        if not is_to_remove_attachments:
            self._save_attachments(str_path_dir_where_to_save)
        #####
        # Mark as read if necessary
        if is_to_mark_messages_as_read:
            self._mark_as_read()

    def _save_letter_metainfo(self, str_path_dir_where_to_save):
        """Save letter metainfo

        Args:
            str_path_dir_where_to_save (str): Directory where to save letter
        """
        dict_metainfo = self._create_dict_with_metainfo()
        str_path_to_metainfo = os.path.join(
            str_path_dir_where_to_save, "dict_metainfo.json")
        with open(str_path_to_metainfo, 'w', encoding='utf-8') as file_handler:
            json.dump(
                dict_metainfo,
                file_handler,
                ensure_ascii=False,
                indent=4
            )
        str_path_letter_text = os.path.join(
            str_path_dir_where_to_save, "letter.txt")
        with open(str_path_letter_text, "w", encoding='utf-8') as file_handler:
            file_handler.write(dict_metainfo["Body"])

    def _create_dict_with_metainfo(self):
        """Create dict with letter metainfo from outlook message handler obj

        Returns:
            dict: Dictionary with letter metainfo
        """
        dict_metainfo = OrderedDict()
        dict_metainfo["Subject"] = self.msg_handler.Subject
        dict_metainfo["To"] = self.msg_handler.To
        dict_metainfo["CC"] = self.msg_handler.CC
        dict_metainfo["Sender.Name"] = self.msg_handler.Sender.Name
        dict_metainfo["Sender.Address"] = self.msg_handler.Sender.Address
        dict_metainfo["Body"] = self.msg_handler.Body
        dict_metainfo["Size"] = self.msg_handler.Size
        dict_metainfo["CreationTime"] = str(self.msg_handler.CreationTime)
        dict_metainfo["ReceivedTime"] = str(self.msg_handler.ReceivedTime)
        dict_metainfo["SavedLocallyTime"] = \
            str(datetime.datetime.now(LOCAL_TIMEZONE))
        return dict_metainfo

    def _save_attachments(self, str_path_dir_where_to_save):
        """Save attachments for the current letter

        Args:
            str_path_dir_where_to_save (str): Directory where to save letter

        Returns:
            int: Number of attachments saved
        """
        LOGGER.debug("Save attachments for letter")
        attachments_obj = self.msg_handler.Attachments
        str_path_dir_attachments = os.path.join(
            str_path_dir_where_to_save, "ATTACHMENTS")
        os.makedirs(str_path_dir_attachments)
        int_num = 0
        for int_num, attachment_obj in enumerate(attachments_obj):
            str_path_for_new_attachment = \
                os.path.join(str_path_dir_attachments, attachment_obj.filename)
            attachment_obj.SaveAsFile(str_path_for_new_attachment)
        LOGGER.debug("---> Attachments saved: %d", int_num + 1)
        return int_num

    def _mark_as_read(self):
        """Mark current message as read
        """
        self.msg_handler.Unread = False
