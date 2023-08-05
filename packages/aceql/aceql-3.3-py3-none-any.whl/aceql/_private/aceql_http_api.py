#
# This file is part of AceQL Python Client SDK.
# AceQL Python Client SDK: Remote SQL access over HTTP with AceQL HTTP.
# Copyright (C) 2020,  KawanSoft SAS
# (http://www.kawansoft.com). All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

import sys

import marshmallow_dataclass

from aceql._private.file_util import FileUtil
from aceql._private.parms import Parms
from aceql._private.user_login_store import UserLoginStore
from aceql._private.jdbc_database_meta_data_dto import JdbcDatabaseMetaDataDto
from aceql._private.table_dto import TableDto
from aceql._private.table_names_dto import TableNamesDto

import requests
from requests_toolbelt.multipart import encoder

from aceql._private.file_util import os
from aceql.error import Error
from aceql._private.aceql_debug import AceQLDebug
from aceql._private.result_analyzer import ResultAnalyzer
from aceql._private.result_set_info import ResultSetInfo
from aceql._private.row_counter import RowCounter
from aceql._private.stream_result_analyzer import StreamResultAnalyzer
from aceql._private.version_values import VersionValues


class AceQLHttpApi(object):
    """ AceQL HTTP wrapper for all apis. Takes care of all
    HTTP calls and operations."""

    __trace_on = False
    __stateless = False
    __timeout = 0
    __debug = True

    def __init__(self, server_url, database, username, password, session_id=None, proxies=None, auth=None):

        if server_url is None:
            raise TypeError("server_url is null!")
        if database is None:
            raise TypeError("database is null!")
        if username is None:
            raise TypeError("username is null!")

        if password is None and session_id is None:
            raise TypeError("password and session_id are both null!")

        self.__server_url = server_url
        self.__database = database
        self.__username = username
        self.__password = password
        self.__proxies = proxies
        self.__auth = auth

        self.__http_status_code = requests.codes.ok

        # Other self for other methods
        self._pretty_printing = True
        self._gzip_result = False
        self._temp_length = 0
        self.__total_length = 0
        self.__progress_indicator = None

        self.__headers = {}

        # url = c + "/database/" + database + "/username/" \
        #       + username + "/connect" + "?password=" \
        #       + password + "&stateless=" + str(AceQLHttpApi.__stateless)

        user_login_store = UserLoginStore(server_url, username, database)

        if session_id is not None:
            user_login_store.set_session_id(session_id);

        try:
            if user_login_store.is_already_logged():
                session_id = user_login_store.get_session_id()
                the_url = server_url + "/session/" + session_id + "/get_connection";

                result = self.call_with_get_url(the_url)

                result_analyzer = ResultAnalyzer(result, self.__http_status_code)
                if not result_analyzer.is_status_ok():
                    raise Error(result_analyzer.get_error_message(),
                                result_analyzer.get_error_type(), None, None, self.__http_status_code)

                connection_id = result_analyzer.get_value("connection_id");
                self._url = server_url + "/session/" + session_id + "/connection/" + connection_id + "/";

            else:
                url = server_url + "/database/" + database + "/username/" \
                      + username + "/login"

                dict_params = {"password": password, "stateless": str(AceQLHttpApi.__stateless)}

                result = self.call_with_post_url(url, dict_params)

                result_analyzer = ResultAnalyzer(result, self.__http_status_code)
                if not result_analyzer.is_status_ok():
                    raise Error(result_analyzer.get_error_message(),
                                result_analyzer.get_error_type(), None, None, self.__http_status_code)

                session_id = result_analyzer.get_value("session_id")
                connection_id = result_analyzer.get_value("connection_id");
                self._url = server_url + "/session/" + session_id + "/" + connection_id + "/" + connection_id + "/"

                user_login_store.set_session_id(session_id);
        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    # *
    # * Says if session is stateless.
    # *
    # * @return {@code true} if session is stateless, else {@code false}.
    #
    @staticmethod
    def is_stateless():
        return AceQLHttpApi.__stateless

    # *
    # * Sets the session mode
    # *
    # * @param stateless
    # * if true, the session will be stateless, else stateful.
    #
    @staticmethod
    def set_stateless(the_stateless):
        if the_stateless is None:
            raise TypeError("stateless is null!")
        if str(the_stateless) == "True":
            AceQLHttpApi.__stateless = True
        else:
            AceQLHttpApi.__stateless = False

    # *
    # * Sets the timeout in seconds
    #
    @staticmethod
    def set_timeout(timeout):
        if timeout is None:
            raise TypeError("timeout is null!")
        AceQLHttpApi.__timeout = timeout

    def set_progress_indicator(self, progress_indicator):
        self.__progress_indicator = progress_indicator

    def get_progress_indicator(self):
        return self.__progress_indicator

    def call_with_get_url(self, url):

        if AceQLHttpApi.__timeout == 0:
            response = requests.get(url, headers=self.__headers, proxies=self.__proxies, auth=self.__auth)
        else:
            response = requests.get(url, headers=self.__headers, proxies=self.__proxies, auth=self.__auth, timeout=AceQLHttpApi.__timeout)

        self.__http_status_code = response.status_code

        return response.text

    def call_with_post_url(self, url, dict_params):

        if AceQLHttpApi.__timeout == 0:
            response = requests.post(url, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth)
        else:
            response = requests.post(url, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth,
                                     timeout=AceQLHttpApi.__timeout)

        self.__http_status_code = response.status_code

        return response.text

    def call_with_get_action(self, action, action_parameter):
        url_withaction = self._url + action

        if action_parameter is not None and len(action_parameter) > 1:
            url_withaction += "/" + action_parameter

        return self.call_with_get_url(url_withaction)

    def call_api_with_result(self, command_name, command_option):
        if command_name is None:
            raise TypeError("command_name is null!")

        try:
            result = self.call_with_get_action(command_name, command_option)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

            return result_analyzer.get_result_default()

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def call_api_no_result(self, command_name, command_option):
        if command_name is None:
            raise TypeError("command_name is null!")

        try:
            result = self.call_with_get_action(command_name, command_option)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def set_auto_commit(self, auto_commit):
        auto_commit_str = str(auto_commit)

        if auto_commit_str == "True":
            auto_commit_str = "true"
        else:
            auto_commit_str = "false"

        self.call_api_no_result("set_auto_commit", auto_commit_str)

    def get_auto_commit(self):
        is_auto_commit_str = self.call_api_with_result("get_auto_commit", None)
        if is_auto_commit_str == "true":
            return True
        else:
            return False

    def commit(self):
        self.call_api_no_result("commit", None)

    def rollback(self):
        self.call_api_no_result("rollback", None)

    @staticmethod
    def trace(s):
        if AceQLHttpApi.__trace_on:
            print(s)

    # *
    # * Says if trace is on
    # *
    # * @return true if trace is on
    #
    @staticmethod
    def is_trace_on():
        return AceQLHttpApi.__trace_on

    # *
    # * Sets the trace on/off
    # *
    # * @param TRACE_ON
    # * if true, trace will be on
    #
    @staticmethod
    def set_trace_on(trace_on):
        AceQLHttpApi.__trace_on = trace_on

    # *
    # * @return the prettyPrinting
    #
    def is_pretty_printing(self):
        return self._pretty_printing

    # *
    # * Says the query result is returned compressed with the GZIP file format.
    # *
    # * @return the gzipResult
    #
    def is_gzip_result(self):
        return self._gzip_result

    # *
    # * Says if JSON contents are to be pretty printed.  Defaults to false.
    # *
    # * @param prettyPrinting
    # * if true, JSON contents are to be pretty printed
    #
    def set_pretty_printing(self, pretty_printing):
        self._pretty_printing = pretty_printing

    # *
    # * Define if result sets are compressed before download.  Defaults to true.
    # *
    # * @param gzipResult
    # * if true, sets are compressed before download
    #
    def set_gzip_result(self, gzip_result):

        if str(gzip_result) == 'True':
            self._gzip_result = True
        else:
            self._gzip_result = False

    # *
    # * Calls /get_version API
    # *
    # * @
    # * if any Exception occurs
    #
    def get_server_version(self):
        the_version = self.call_api_with_result("get_version", None)
        return the_version

    # *
    # * Gets the SDK version
    # *
    # * @
    # * if any Exception occurs
    #
    @staticmethod
    def get_client_version():
        return VersionValues.NAME + " - " + VersionValues.VERSION + " - " + VersionValues.DATE

    # *
    # * Gets the SDK version + Python version
    # *
    # * @
    # * if any Exception occurs
    #
    @staticmethod
    def get_client_version_full():
        return AceQLHttpApi.get_client_version() + " - " + sys.version

    # *
    # * Calls /close API
    # *
    # * @
    # * if any Exception occurs
    #
    def close(self):
        self.call_api_no_result("close", None)

    # *
    # * Calls /logout API
    # *
    # * @
    # * if any Exception occurs
    #
    def logout(self):
        user_login_store = UserLoginStore(self.__server_url, self.__username, self.__database)
        user_login_store.remove()
        self.call_api_no_result("logout", None)

    # *
    # * Calls /get_transaction_isolation_level API
    # *
    # * @return the current transaction isolation level, which will be one of the
    # * following constants: <code>transaction_read_uncommitted</code>,
    # * <code>transaction_read_committed</code>,
    # * <code>transaction_repeatable_read</code>,
    # * <code>transaction_serializable</code>, or
    # * <code>transaction_none</code>.
    # * @
    # * if any Exception occurs
    #
    def get_transaction_isolation(self):
        transaction_isolation = self.call_api_with_result("get_transaction_isolation_level", None)
        return transaction_isolation

    # *
    # * Calls /set_transaction_isolation_level API
    # *
    # * @param level
    # * the isolation level
    # * @
    # * if any Exception occurs
    #
    def set_transaction_isolation(self, level):
        self.call_api_no_result("set_transaction_isolation_level", level)

    #
    # * Calls /get_holdability API
    # *
    # * @return the holdability, one of <code>hold_cursors_over_commit</code> or
    # * <code>close_cursors_at_commit</code>
    # * @throws Error
    # * if any Exception occurs
    #
    def get_holdability(self):
        holdability = self.call_api_with_result("get_holdability", None)
        return holdability

    # *
    # * Calls /set_holdability API
    # *
    # * @param holdability
    # * the holdability
    # * @
    # * if any Exception occurs
    #
    def set_holdability(self, holdability):
        self.call_api_no_result("set_holdability", holdability)

    # *
    # * Calls /get_auto_commit API
    # *
    # * @return <code>true</code> if this <code>Connection</code> object is
    # * read-only; <code>false</code> otherwise
    # * @
    # * if any Exception occurs
    #
    def is_read_only(self):
        is_read_only_str = self.call_api_with_result("is_read_only", None)
        if is_read_only_str == "true":
            return True
        else:
            return False

    # *
    # * Calls /set_read_only API
    # *
    # * @param readOnly
    # * {@code true} enables read-only mode; {@code false} disables it
    # * @
    # * if any Exception occurs
    #
    def set_read_only(self, read_only):
        if read_only is None:
            raise TypeError("read_only is null!")

        read_only_str = "false"

        if str(read_only) == "True":
            read_only_str = "true"

        self.call_api_no_result("set_read_only", read_only_str)

    # *
    # * @return the httpStatus
    #
    def get_http_status_code(self):
        return self.__http_status_code

    # *
    # * @return the httpStatusMessage
    #
    def get_http_status_message(self):
        status_messages = requests.status_codes.codes[self.__http_status_code]
        return status_messages[0]

    # *
    # * Calls /execute_update API
    # *
    # * @param sql
    # * an SQL <code>INSERT</code>, <code>UPDATE</code> or
    # * <code>DELETE</code> statement or an SQL statement that returns
    # * nothing
    # * @param isPreparedStatement
    # * if true, the server will generate a prepared statement, else a
    # * simple statement
    # * @param statementParameters
    # * the statement parameters in JSON format.  Maybe null for simple
    # * statement call.
    # * @return either the row count for <code>INSERT</code>, <code>UPDATE</code>
    # * or <code>DELETE</code> statements, or <code>0</code> for SQL
    # * statements that return nothing
    # * @
    # * if any Exception occurs
    #
    def execute_update(self, sql, is_prepared_statement, statement_parameters):

        try:

            action = "execute_update"

            self.check_values(is_prepared_statement, sql)

            dict_params = {}
            dict_params["sql"] = sql

            self.set_is_prepared_statement(dict_params, is_prepared_statement)

            url_withaction = self._url + action

            AceQLDebug.debug("url_withaction: " + url_withaction)
            AceQLDebug.debug("dict_params 1: " + str(dict_params))

            if statement_parameters is not None:
                if not isinstance(statement_parameters, dict):
                    raise TypeError("statement_parameters is not a dictionnary!")

                dict_params.update(statement_parameters)

            AceQLDebug.debug("dictParams 2: " + str(dict_params))

            # r = requests.post('http://httpbin.org/post', data = {'key':'value'})
            # print("Before update request")

            if AceQLHttpApi.__timeout == 0:
                response = requests.post(url_withaction, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth)
            else:
                response = requests.post(url_withaction, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth,
                                         timeout=AceQLHttpApi.__timeout)

            # if AceQLHttpApi.__timeout == 0:
            #     response = requests.post(url_withaction, data=dict_params, proxies=self.__proxies, auth=self.__auth)
            # else:
            #     response = requests.post(url_withaction, data=dict_params, proxies=self.__proxies, auth=self.__auth,
            #                              timeout=AceQLHttpApi.__timeout)

            self.__http_status_code = response.status_code
            result = response.text

            # print("self.__http_status_code: " + str(self.__http_status_code ))
            # print("result                 : " + str(result))
            AceQLDebug.debug("result: " + result)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

            row_count = result_analyzer.get_int_value("row_count")
            return row_count

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    # *
    # * Calls /execute_query API
    # *
    # * @param sql
    # * an SQL <code>INSERT</code>, <code>UPDATE</code> or
    # * <code>DELETE</code> statement or an SQL statement that returns
    # * nothing
    # * @param isPreparedStatement
    # * if true, the server will generate a prepared statement, else a
    # * simple statement
    # * @param statementParameters
    # * the statement parameters in JSON format.  Maybe null for simple
    # * statement call.
    # * @return the input stream containing either an error, or the result set in
    # * JSON format.  See user documentation.
    # * @
    # * if any Exception occurs
    #
    def execute_query(self, sql, isPreparedStatement, statementParameters):

        try:

            action = "execute_query"

            self.check_values(isPreparedStatement, sql)

            dict_params = {"sql": sql}
            self.set_is_prepared_statement(dict_params, isPreparedStatement)

            url_withaction = self._url + action

            AceQLDebug.debug("url_withaction: " + url_withaction)
            AceQLDebug.debug("dictParams 1: " + str(dict_params))

            if statementParameters is not None:
                if not isinstance(statementParameters, dict):
                    raise TypeError("statementParameters is not a dictionnary!")

                dict_params.update(statementParameters)

            self.update_dict_params(dict_params)

            AceQLDebug.debug("dictParams 2: " + str(dict_params))

            # r = requests.post('http://httpbin.org/post', data = {'key':'value'})

            if AceQLHttpApi.__timeout == 0:
                response = requests.post(url_withaction, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth)
            else:
                response = requests.post(url_withaction, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth,
                                         timeout=AceQLHttpApi.__timeout)

            self.__http_status_code = response.status_code

            filename = FileUtil.build_result_set_file()
            AceQLDebug.debug("filename1: " + filename)

            # We dump the JSon stream into user.home/.kawansoft/tmp
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=2048):
                    fd.write(chunk)

            AceQLDebug.debug("after open filename")

            result_set_info = self.treat_result(filename)

            return result_set_info

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def treat_result(self, filename):
        file_out = None
        if self.is_gzip_result():
            file_out = filename[0: len(filename) - 4] + ".ungzipped.txt"
            FileUtil.decompress(filename, file_out)
            if Parms.DELETE_FILES:
                os.remove(filename)
        else:
            file_out = filename
        AceQLDebug.debug("Before StreamResultAnalyzer")
        result_analyzer = StreamResultAnalyzer(file_out, self.__http_status_code)
        if not result_analyzer.is_status_ok():
            if Parms.DELETE_FILES:
                os.remove(filename)
            raise Error(result_analyzer.get_error_message(),
                        result_analyzer.get_error_type(), None, None, self.__http_status_code)
        row_counter = RowCounter(file_out)
        row_count = row_counter.count()
        result_set_info = ResultSetInfo(file_out, row_count)
        AceQLDebug.debug("Before resultSetInfo")
        return result_set_info

    def update_dict_params(self, dict_params):
        if self._gzip_result:
            dict_params["gzip_result"] = "true"
        if self._pretty_printing:
            dict_params["pretty_printing"] = "true"
        # Force pretty printing to True because parser needs it
        dict_params["pretty_printing"] = "true"
        # We need the types
        dict_params["column_types"] = "true"

    def check_values(self, is_prepared_statement, sql):
        if sql is None:
            raise TypeError("sql is null!")
        if is_prepared_statement is None:
            raise TypeError("isPreparedStatement is null!")

    @staticmethod
    def set_is_prepared_statement(dict_params, is_prepared_statement):
        if str(is_prepared_statement) == 'True':
            dict_params["prepared_statement"] = "true"
        else:
            dict_params["prepared_statement"] = "false"

    def get_blob_stream(self, blob_id):
        """ returns a BLOB stream as a Requests response """
        try:

            if blob_id is None:
                raise TypeError("blob_id is null!")

            the_url = self._url + "/blob_download?blob_id=" + blob_id

            if AceQLHttpApi.__timeout == 0:
                response = requests.get(the_url, headers=self.__headers, proxies=self.__proxies, auth=self.__auth)
            else:
                response = requests.get(the_url, headers=self.__headers, proxies=self.__proxies, auth=self.__auth,
                                        timeout=AceQLHttpApi.__timeout)

            self.__http_status_code = response.status_code

            return response

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def db_schema_download(self, file_format, table_name):
        """ returns a schema stream as a Requests response """
        try:
            if file_format is None:
                raise TypeError("format is null!")

            the_url = self._url + "/metadata_query/db_schema_download"

            dict_params = {}
            dict_params["format"] = file_format

            if table_name is not None:
                table_name = table_name.lower()
                dict_params["table_name"] = table_name

            if AceQLHttpApi.__timeout == 0:
                response = requests.post(the_url, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth)
            else:
                response = requests.post(the_url, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth,
                                         timeout=AceQLHttpApi.__timeout)

            self.__http_status_code = response.status_code

            return response

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def get_blob_length(self, blob_id):
        """ Gets the blob length. """
        try:

            if blob_id is None:
                raise TypeError("blob_id is null!")

            action = "get_blob_length"

            dict_params = {}
            dict_params["blob_id"] = blob_id

            url_withaction = self._url + action

            AceQLDebug.debug("urlWithaction: " + url_withaction)
            AceQLDebug.debug("dictParams   : " + str(dict_params))

            # r = requests.post('http://httpbin.org/post', data = {'key':'value'})

            if AceQLHttpApi.__timeout == 0:
                response = requests.post(url_withaction, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth)
            else:
                response = requests.post(url_withaction, headers=self.__headers, data=dict_params, proxies=self.__proxies, auth=self.__auth,
                                         timeout=AceQLHttpApi.__timeout)

            self.__http_status_code = response.status_code
            result = response.text

            AceQLDebug.debug("result: " + result)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

            length_str = result_analyzer.get_value("length")
            AceQLDebug.debug("result: " + length_str + ":")
            return int(length_str)

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def my_callback(self, monitor):
        """ The callback function when uploading a BLOB """
        try:
            if self.__total_length == 0 or self.__progress_indicator is None:
                return

            the_read = monitor.bytes_read

            self._temp_length += the_read
            if self._temp_length >= self.__total_length / 100:
                self._temp_length = 0
                self.__progress_indicator._increment()

        except Exception as e:
            print(str(e))

    def blob_upload(self, blob_id, fd, total_length):
        """ Upload the BLOB and use a callback function for progress indicator. """

        self.__total_length = total_length

        # fields={'field0': 'value', 'field1': 'value',
        # 'field2': ('filename', open('file.py', 'rb'), 'text/plain')}

        the_fields = dict()
        the_fields["blob_id"] = blob_id
        the_fields["file"] = ("filename", fd, "application/octet-stream")

        e = encoder.MultipartEncoder(fields=the_fields)
        m = encoder.MultipartEncoderMonitor(e, self.my_callback)

        the_headers = dict(self.__headers)  # or orig.copy()
        the_headers["Content-Type"] = m.content_type

        the_url = self._url + "blob_upload"
        #requests.post(the_url, data=m, headers={'Content-Type': m.content_type}, proxies=self.__proxies,
        #              auth=self.__auth)
        requests.post(the_url, data=m, headers=the_headers, proxies=self.__proxies,
                      auth=self.__auth)

    def get_db_metadata(self):
        try:
            url_withaction = self._url + "metadata_query/get_db_metadata"
            result = self.call_with_get_url(url_withaction)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

            if AceQLHttpApi.__debug:
                print(result)

            holder_jdbc_database_meta_data_schema = marshmallow_dataclass.class_schema(JdbcDatabaseMetaDataDto)
            jdbc_database_meta_data_holder: JdbcDatabaseMetaDataDto = holder_jdbc_database_meta_data_schema().loads(
                result)

            if AceQLHttpApi.__debug:
                print(jdbc_database_meta_data_holder)

            return jdbc_database_meta_data_holder;

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def get_table_names(self, table_type):
        try:
            url_withaction = self._url + "metadata_query/get_table_names"

            if table_type is not None:
                url_withaction += "?table_type=" + table_type

            result = self.call_with_get_url(url_withaction)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

            if AceQLHttpApi.__debug:
                print(result)

            table_names_dto_schema = marshmallow_dataclass.class_schema(TableNamesDto)
            table_names_dto: TableNamesDto = table_names_dto_schema().loads(result)

            if AceQLHttpApi.__debug:
                print(table_names_dto)

            return table_names_dto;

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def get_table(self, name):
        try:
            url_withaction = self._url + "metadata_query/get_table"

            if name is None:
                raise TypeError("name is null!")
            url_withaction += "?table_name=" + name

            result = self.call_with_get_url(url_withaction)

            if AceQLHttpApi.__debug:
                print(result)

            result_analyzer = ResultAnalyzer(result, self.__http_status_code)
            if not result_analyzer.is_status_ok():
                raise Error(result_analyzer.get_error_message(),
                            result_analyzer.get_error_type(), None, None, self.__http_status_code)

            table_dto_schema = marshmallow_dataclass.class_schema(TableDto)
            table_dto: TableDto = table_dto_schema().loads(result)

            if AceQLHttpApi.__debug:
                print(table_dto)

            return table_dto;

        except Exception as e:
            if isinstance(e, Error):
                raise
            else:
                raise Error(str(e), 0, e, None, self.__http_status_code)

    def add_request_headers(self, headers):
        self.__headers = headers

    def reset_request_headers(self):
        self.__headers = {}
