import os
import json
from shutil import rmtree, copyfileobj
from airtable import Airtable
from urllib.parse import urlparse
import requests
from pathlib import Path
import logging

"""
 █████╗ ██╗██████╗ ████████╗ █████╗ ██████╗ ██╗     ███████╗
██╔══██╗██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝
███████║██║██████╔╝   ██║   ███████║██████╔╝██║     █████╗  
██╔══██║██║██╔══██╗   ██║   ██╔══██║██╔══██╗██║     ██╔══╝  
██║  ██║██║██║  ██║   ██║   ██║  ██║██████╔╝███████╗███████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝

 ██████╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
██╔════╝██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝ 
██║     ███████║██║     ███████║██║██╔██╗ ██║██║  ███╗
██║     ██╔══██║██║     ██╔══██║██║██║╚██╗██║██║   ██║
╚██████╗██║  ██║╚██████╗██║  ██║██║██║ ╚████║╚██████╔╝
 ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
Author: Ross Mountjoy and Thomas Huxley                                             
"""

# Set up the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def remove_empty_folders(path, remove_root=True):
    'Function to remove empty folders'
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        logger.info("Removing empty folder:", path)
        os.rmdir(path)


def get_record_attachments(record):
    attachments = []
    if "fields" in record:
        fields = record["fields"]
        for key in fields.keys():
            field = fields[key]
            if isinstance(field, list) and isinstance(field[0], dict):
                if "url" in field[0]:
                    attachments.append({"key": key, "field": field})
    return attachments


class Base:
    def __init__(self, base_id, api_key, json_folder=None):
        self.base_id = base_id
        self.api_key = api_key
        self.cache_url_base = None
        self.existing_table = None

        # get json folder path
        if json_folder is None:
            curr_folder = os.path.dirname(__file__)
            main_json_folder = os.path.join(curr_folder, "json")
        else:
            main_json_folder = os.path.abspath(json_folder)
        if not os.path.isdir(main_json_folder):
            os.mkdir(main_json_folder)
        self.json_folder = os.path.join(main_json_folder, self.base_id)
        if not os.path.isdir(self.json_folder):
            os.mkdir(self.json_folder)

    def load_current_table(self, table_name):
        cache_exists = False
        try:
            path = os.path.join(self.json_folder, f"{table_name}.json")
            logger.info(f"Load current table: {path}")
            with open(
                    path, "r"
            ) as json_file:
                self.existing_table = json.load(json_file)["list"]
                cache_exists = True
        except EnvironmentError:
            logger.error("oops")

        return cache_exists

    def attachment_exists(self, attachment_url):
        attachment_url_parsed = urlparse(attachment_url)
        path = self.json_folder + attachment_url_parsed.path
        if os.path.isfile(path):
            logger.info('File exists :' + attachment_url_parsed.path)
            return True
        return False

    def save_attachment(self, url):
        parsed_url = urlparse(url)
        pathname = self.json_folder + parsed_url.path
        new_filename = self.cache_url_base + '/' + self.base_id + parsed_url.path

        if self.attachment_exists(url):
            return new_filename

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            os.makedirs(os.path.dirname(pathname), exist_ok=True)
            with open(pathname, 'wb') as f:
                copyfileobj(r.raw, f)

            logger.info('Image sucessfully Downloaded: ', parsed_url.path)
            return new_filename
        else:
            logger.info('Image Couldn\'t be retreived')
            return False

    def delete_attachment(self, attachment):
        parsed_url = urlparse(attachment["url"].replace(self.cache_url_base + '/' + self.base_id, ''))
        pathname = self.json_folder + parsed_url.path
        try:
            logger.info("Delete: ", pathname)
            os.remove(pathname)
        except EnvironmentError:
            logger.error('No file found: ', pathname)

        if "thumbnails" in attachment:
            thumbnail_sizes = ["small", "large", "full"]
            for size in thumbnail_sizes:
                if size in attachment["thumbnails"]:
                    url = attachment["thumbnails"][size]["url"]
                    parsed_url = urlparse(url.replace(self.cache_url_base + '/' + self.base_id, ''))
                    pathname = self.json_folder + parsed_url.path
                    try:
                        logger.info("Delete: ", pathname)
                        os.remove(pathname)
                    except EnvironmentError:
                        logger.error('No file found: ', pathname)
        return

    def delete_old_attachments(self, new_attachments, record_id):
        if self.existing_table is None:
            logger.info('no cached json')
            return
        rec_list = [rec for rec in self.existing_table if rec["id"] == record_id]
        if len(rec_list):
            rec = rec_list[0]
        else:
            return
        if rec:
            current_record = rec
        else:
            return

        if "fields" not in current_record:
            return

        current_attachments = get_record_attachments(current_record)

        for c_attachment_field in current_attachments:
            matching_field = next((n_attachment['field'] for n_attachment in
                                   new_attachments if c_attachment_field["key"] ==
                                   n_attachment["key"]), None)
            if matching_field:
                for c_attachment in c_attachment_field["field"]:
                    attachment_exists = False
                    for n_attachment in matching_field:
                        if c_attachment["id"] == n_attachment["id"]:
                            attachment_exists = True
                    if not attachment_exists:
                        self.delete_attachment(c_attachment)
            else:
                # key no longer exists, so delete all attachments
                for c_attachment in c_attachment_field["field"]:
                    self.delete_attachment(c_attachment)

        # Remove all empty folders
        remove_empty_folders(self.json_folder, False)
        return

    def cache_attachment(self, field):
        original_url = field["url"]
        new_attachment_url = self.save_attachment(original_url)
        if new_attachment_url:
            field["url"] = new_attachment_url

        if "thumbnails" in field:
            thumbnail_sizes = ["small", "large", "full"]
            for size in thumbnail_sizes:
                if size in field["thumbnails"]:
                    url = field["thumbnails"][size]["url"]
                    new_attachment_url = self.save_attachment(url)
                    if new_attachment_url:
                        field["thumbnails"][size]["url"] = new_attachment_url

        return field

    def cache_attachments(self, json_data):
        for rIndex, record in enumerate(json_data["list"]):
            attachments = get_record_attachments(record)
            self.delete_old_attachments(attachments, record["id"])
            for attachment_field in attachments:
                for idx, attachment in enumerate(attachment_field["field"]):
                    attachment_field["field"][idx] = self.cache_attachment(attachment_field["field"][idx])
                json_data["list"][rIndex]["fields"][attachment_field["key"]] = attachment_field["field"]
        return json_data

    def cache_table(self, table_name, attachment_cache=False, **kwargs):
        """
        save table using airtable-python-wrapper's get_all function as a json file
        :param attachment_cache:
        :param table_name:
        :param kwargs:
        :return:
        """
        airtable = Airtable(self.base_id, table_name, self.api_key)
        at_json = {"list": airtable.get_all(**kwargs)}
        if attachment_cache:
            self.cache_url_base = attachment_cache
            self.load_current_table(table_name)
            at_json = self.cache_attachments(at_json)
        json_path = os.path.join(self.json_folder, f"{table_name}.json")
        if os.path.isfile(json_path):
            os.remove(json_path)
        with open(json_path, "w") as new_file:
            json.dump(at_json, new_file)

    def clear_cache(self):
        """
        delete all json files out of this base's json folder
        :return:
        """
        rmtree(self.json_folder)
        os.mkdir(self.json_folder)


class Table:
    def __init__(self, base_id, table_name, json_folder=None):
        self.base_id = base_id
        self.table_name = table_name
        self.list = None

        # get json folder path
        if json_folder is None:
            logger.info("json_folder not set")
            curr_folder = os.path.dirname(__file__)
            main_json_folder = os.path.join(curr_folder, "json")
        else:
            logger.info(f"json_folder: {json_folder}")
            main_json_folder = os.path.abspath(json_folder)
        logger.info(f"main_json_folder: {main_json_folder}")
        self.json_folder = os.path.join(main_json_folder, self.base_id)
        logger.info(f"self.json_folder: {self.json_folder}")

    def get(self, rec_id, resolve_fields=None):
        """
        reads json file for given record id, optionally resolves relationships,
        then returns the record as a dict
        :param rec_id:
        :param resolve_fields:
        :return:
        """
        self.__get_dict_list_from_json_file()
        if resolve_fields:
            self.__resolve_relationships(resolve_fields)
        recs = [rec for rec in self.list if rec["id"] == rec_id]
        if not recs:
            return None
        return recs[0]

    def query(self, resolve_fields=None):
        """
        reads json file for all records, optionally resolves relationships,
        then sets self.list as a list of dicts.
        :param resolve_fields:
        :return:
        """
        self.__get_dict_list_from_json_file()
        if resolve_fields:
            self.__resolve_relationships(resolve_fields)
        if len(self.list) < 1:
            self.list = None
        return self

    def filter_by(self, fields):
        """
        filters self.list by a given dict of {<field>:<value>}
        :param fields:
        :return:
        """
        for field, value in fields.items():
            self.list = [rec for rec in self.list if rec["fields"].get(field) == value]
        if len(self.list) < 1:
            self.list = None
        return self

    def order_by(self, field, desc=False):
        """
        orders self.list by the given field, set desc to order descending
        :param field:
        :param desc:
        :return:
        """
        try:
            self.list = sorted(self.list, key=lambda i: i["fields"].get(field, None))
        except TypeError:
            raise Exception(
                f"Invalid field error: '{field}' does not exist in {self.table_name}'s ['fields'] dict."
            )

        if len(self.list) < 1:
            self.list = None
        if desc and self.list:
            self.list.reverse()
        return self

    def all(self):
        """
        returns all of self.list
        :return:
        """
        self.query()
        return self.list

    def first(self):
        """
        returns the first record in self.list
        :return:
        """
        if len(self.list) < 1:
            return None
        return self.list[0]

    def last(self):
        """
        returns the last record in self.list
        :return:
        """
        if len(self.list) < 1:
            return None
        return self.list[-1]

    def __get_dict_list_from_json_file(self):
        json_file_path = os.path.join(self.json_folder, f"{self.table_name}.json")
        logger.info("__get_dict_list_from_json_file")
        logger.info(f"json_file_path: {json_file_path}")
        if Path(json_file_path).exists():
            with open(
                    json_file_path, "r"
            ) as json_file:
                table_dict = json.load(json_file)
                self.list = table_dict["list"]
        else:
            logger.info(f"No cached table found for {self.table_name}")
            table_dict = {"list": []}
        self.list = table_dict["list"]

    def __resolve_relationships(self, resolve_fields):
        for table_name, rel_field in resolve_fields.items():
            for rec in self.list:
                full_rec_list = []
                if rec["fields"].get(rel_field, None):
                    for related_rec in rec["fields"][rel_field]:
                        d = Table(base_id=self.base_id, table_name=self.table_name)
                        full_rec_list.append(d.get(related_rec))
                    rec["fields"][rel_field] = full_rec_list
