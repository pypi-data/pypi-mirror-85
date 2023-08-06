# -*- coding: utf-8 -*-

import pytest

from wallabag.api.api import Api, Response
from wallabag.api.get_list_entries import GetListEntries
from wallabag.commands.list import ListCommand, ListParams
from wallabag.config import Configs
from tags import tags_test


def get_authorization_header(self):
    return {'Authorization': "Bearer a1b2"}


class TestListCommand():

    def setup_method(self, method):
        self.config = Configs("/tmp/config")
        self.config.config.read_string("""
                [api]
                serverurl = url
                username = user
                password = pass
                [oauth2]
                client = 100
                secret = 100
                """)

    def test_empty_list(self, monkeypatch):

        def list_entries(self):
            text = '{ "_embedded": { "items": [] } }'
            return Response(200, text)

        monkeypatch.setattr(GetListEntries, 'request', list_entries)

        command = ListCommand(self.config)
        result, entries = command.execute()
        assert result
        assert not entries

    @pytest.mark.parametrize('values', [
        ((0, 0), '1 title'), ((0, 1), '1 * title'),
        ((1, 0), '1 ✔ title'), ((1, 1), '1 ✔* title'),
        ])
    def test_entries_list(self, monkeypatch, values):

        def list_entries(self):
            text = '''
            { "_embedded": { "items": [
                {
                "id": 1,
                "title": "title",
                "content": "content",
                "url": "url",
                "is_archived": %s,
                "is_starred": %s
                }
            ] } }
            ''' % (values[0][0], values[0][1])
            return Response(200, text)

        monkeypatch.setattr(GetListEntries, 'request', list_entries)

        command = ListCommand(self.config)
        result, entries = command.execute()
        assert result
        assert entries
        assert entries == values[1]

    def test_list(self, monkeypatch):

        def list_entries(self):
            text = '''
            { "_embedded": { "items": [
                { "id": 1, "title": "title", "content": "content",
                "url": "url", "is_archived": 0, "is_starred": 1},
                { "id": 2, "title": "title", "content": "content",
                "url": "url", "is_archived": 0, "is_starred": 1}
            ] } }
            '''
            return Response(200, text)

        monkeypatch.setattr(GetListEntries, 'request', list_entries)

        command = ListCommand(self.config)
        result, entries = command.execute()
        assert result
        assert len(entries.split('\n')) == 2

    @pytest.mark.parametrize('tags', tags_test)
    def test_tags_param(self, monkeypatch, tags):
        make_request_runned = False

        def _make_request(self, request):
            nonlocal make_request_runned
            make_request_runned = True
            assert GetListEntries.ApiParams.TAGS.value in request.api_params
            assert request.api_params[
                    GetListEntries.ApiParams.TAGS.value].split(',') == tags[1]
            text = '{ "_embedded": { "items": [] } }'
            return Response(200, text)

        monkeypatch.setattr(GetListEntries, '_make_request', _make_request)
        monkeypatch.setattr(
                Api, '_get_authorization_header', get_authorization_header)

        command = ListCommand(self.config, ListParams(tags=tags[0]))
        result, entries = command.execute()
        if tags[0]:
            assert make_request_runned
            assert result
        else:
            assert not make_request_runned
            assert not result
