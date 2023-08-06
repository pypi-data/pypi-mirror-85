import fnmatch
import logging
import os
import posixpath
import re
from typing import List, Any
from urllib.parse import urlparse

from googleapiclient.discovery import build

from gdrive.auth import GoogleAuth
from gdrive.exception import GDriveException
from gdrive.utils import query_string_to_dict

log = logging.getLogger(__name__)


class GDriveClient:
    def __init__(self, gauth: GoogleAuth):
        self.service = build('drive', 'v3', credentials=gauth.credentials, cache_discovery=False)

    def get(self, path_qs):
        """
        :param path_qs: gdrive://a/b/c/file?mime_type=text/plain
        :param mime_type:
        :return:
        """
        log.debug("finding file: %s", path_qs)
        query_parsed, query_dict = query_string_to_dict(path_qs)
        mime_type = query_dict.get("mime_type", None)
        file_meta = self.get_file_meta(path_qs)
        contents = self.get_file(file_meta, mime_type)
        if mime_type == "text/plain":
            return contents.decode("utf-8")
        else:
            return contents

    def export(self, file_id: str, mime_type: str = None):
        '''
        Exports Google Doc to mime_type
        :param file_id: Google Drive's file ID
        :param mime_type: user-picked mime type
        :return: File contents in requested mime type
        '''
        exported = self.service.files().export(fileId=file_id, mimeType=mime_type).execute()
        return exported.decode("utf-8")

    def download(self, file_id: str):
        '''
        Download file as-is
        :param file_id: the Google file ID
        :return: file contents without any conversion
        '''
        exported = self.service.files().get_media(fileId=file_id).execute()
        return exported

    def get_file(self, file_meta, mime_type=None):
        if file_meta['mimeType'] == 'application/vnd.google-apps.document':
            log.debug("Exporting file: {}".format(file_meta))
            return self.export(file_meta['id'], mime_type if mime_type else file_meta['mimeType'])
        else:
            log.debug("Downloading file: {}".format(file_meta))
            return self.download(file_meta['id'])

    def walk(self, path_qs, current_path, include_pat=None, exclude_pat=None) -> List[Any]:
        start_path = current_path  # the path can be in the form of scheme://path/
        log.debug("walk: {}, start_path: {}".format(path_qs, start_path))
        dir_file_meta = self.get_file_meta(path_qs)

        def merge(indict, cpath):
            indict.update({'content': loop(indict, os.path.join(cpath, indict['name']))})
            return indict

        def loop(current_file_meta, cpath):
            def f(file_meta):
                relpath = posixpath.relpath(os.path.join(cpath, file_meta['name']), start_path)
                return self._check_include_exclude(relpath, include_pat, exclude_pat)

            return [(merge(e, cpath) if e['mimeType'] == 'application/vnd.google-apps.folder' else e) for e in
                    filter(f, self._list_children(current_file_meta))]

        return loop(dir_file_meta, start_path)

    def get_file_meta(self, path_qs):
        '''
        Asserts that path exists on the google drive

        :return: full file_meta of file/folder traversed to (the last one)
        '''
        path_segment_list = self._path_to_list(path_qs)
        log.debug("gdrive segment list: {}".format(path_segment_list))

        def go(parent_meta, idx):
            if idx >= len(path_segment_list):
                return parent_meta
            next_name = path_segment_list[idx]
            file_list = self._list_children(parent_meta)
            r = [e for e in file_list if e['name'] == next_name]
            if len(r) > 0:
                # don't care if name occurred in other pages or already multiple times
                return go(r[0], idx + 1)
            raise GDriveException(f'Unable to lookup: {next_name}, under directory with meta: {parent_meta}, requested path: {path_qs}')

        if not path_segment_list:
            return {'id': 'root', 'mimeType': ''}
        else:
            return go({'id': 'root'}, 0)

    def _list_children(self, parent_meta):
        def query(extra_params={}):
            r = self.service.files().list(q="'{}' in parents and trashed = false".format(parent_meta['id']),
                                          **extra_params).execute()
            self._assert_incomplete_search(r)
            return r

        json_response = query()
        ret_list = json_response['files']
        while 'nextPageToken' in json_response:
            log.debug("Fetching next page of files under: {}".format(parent_meta))
            json_response = query({'pageToken': json_response['nextPageToken']})
            ret_list.extend(json_response['files'])
        return ret_list

    def _path_to_list(self, path):
        source = urlparse(path)
        p = source.netloc + source.path
        return p.strip(os.sep).split(os.sep)

    def _assert_incomplete_search(self, json_response):
        if json_response['incompleteSearch']:
            raise GDriveException('google drive query ended due to incompleteSearch')

    @staticmethod
    def _check_include_exclude(path_str, include_pat=None, exclude_pat=None):
        """
        Check for glob or regexp patterns for include_pat and exclude_pat in the
        'path_str' string and return True/False conditions as follows.
          - Default: return 'True' if no include_pat or exclude_pat patterns are
            supplied
          - If only include_pat or exclude_pat is supplied: return 'True' if string
            passes the include_pat test or fails exclude_pat test respectively
          - If both include_pat and exclude_pat are supplied: return 'True' if
            include_pat matches AND exclude_pat does not match
        """

        def _pat_check(path_str, check_pat):
            if re.match("E@", check_pat):
                return True if re.search(check_pat[2:], path_str) else False
            else:
                return True if fnmatch.fnmatch(path_str, check_pat) else False

        ret = True  # -- default true
        # Before pattern match, check if it is regexp (E@'') or glob(default)
        if include_pat:
            if isinstance(include_pat, list):
                for include_line in include_pat:
                    retchk_include = _pat_check(path_str, include_line)
                    if retchk_include:
                        break
            else:
                retchk_include = _pat_check(path_str, include_pat)

        if exclude_pat:
            if isinstance(exclude_pat, list):
                for exclude_line in exclude_pat:
                    retchk_exclude = not _pat_check(path_str, exclude_line)
                    if not retchk_exclude:
                        break
            else:
                retchk_exclude = not _pat_check(path_str, exclude_pat)

        # Now apply include/exclude conditions
        if include_pat and not exclude_pat:
            ret = retchk_include
        elif exclude_pat and not include_pat:
            ret = retchk_exclude
        elif include_pat and exclude_pat:
            ret = retchk_include and retchk_exclude
        else:
            ret = True

        return ret
