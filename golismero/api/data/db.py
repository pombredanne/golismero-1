#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Information, resources and vulnerabilities database API.
"""

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/golismero
Golismero project mail: golismero.project<@>gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

__all__ = ["Database"]

from ..config import Config
from ...common import Singleton
from ...messaging.codes import MessageCode


#------------------------------------------------------------------------------
class Database(Singleton):
    """
    Access to information, resources and vulnerabilities found by the plugins.
    """


    #--------------------------------------------------------------------------
    @staticmethod
    def add(data):
        """
        Add data to the database.

        :param data: Data to add.
        :type data: Data

        :returns: True if the data was added, False if it was updated.
        :rtype: bool
        """
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_ADD, data)


    #--------------------------------------------------------------------------
    @staticmethod
    def async_add(data):
        """
        Asynchronously add data to the database.

        :param data: Data to add.
        :type data: Data
        """
        Config._context.async_remote_call(
            MessageCode.MSG_RPC_DATA_ADD, data)


    #--------------------------------------------------------------------------
    @staticmethod
    def async_add_many(dataset):
        """
        Asynchronously add multiple data objects to the database.

        :param dataset: Data to add.
        :type dataset: list(Data)
        """
        Config._context.async_remote_call(
            MessageCode.MSG_RPC_DATA_ADD_MANY, dataset)


    #--------------------------------------------------------------------------
    @staticmethod
    def remove(identity, data_type = None):
        """
        Remove an object given its identity hash.

        Optionally restrict the result by data type. Depending on the
        underlying database, this may result in a performance gain.

        :param identity: Identity hash.
        :type identity: str

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int

        :returns: True if the object was removed, False if it didn't exist.
        :rtype: bool
        """
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_REMOVE, identity, data_type)


    #--------------------------------------------------------------------------
    @staticmethod
    def async_remove(identity, data_type = None):
        """
        Asynchronously remove an object given its identity hash.

        Optionally restrict the result by data type. Depending on the
        underlying database, this may result in a performance gain.

        :param identity: Identity hash.
        :type identity: str

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int
        """
        Config._context.async_remote_call(
            MessageCode.MSG_RPC_DATA_REMOVE, identity, data_type)


    #--------------------------------------------------------------------------
    @staticmethod
    def async_remove_many(identities, data_type = None):
        """
        Asynchronously remove multiple objects given their identity hashes.

        Optionally restrict the result by data type. Depending on the
        underlying database, this may result in a performance gain.

        :param identities: Identity hashes.
        :type identities: str

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int
        """
        Config._context.async_remote_call(
            MessageCode.MSG_RPC_DATA_REMOVE_MANY, identities, data_type)


    #--------------------------------------------------------------------------
    @staticmethod
    def has_key(identity, data_type = None):
        """
        Check if an object with the given
        identity hash is present in the database.

        Optionally restrict the result by data type. Depending on the
        underlying database, this may result in a performance gain.

        :param identity: Identity hash.
        :type identity: str

        :returns: True if the object is present, False otherwise.
        :rtype: bool
        """
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_CHECK, identity, data_type)


    #--------------------------------------------------------------------------
    @staticmethod
    def get(identity, data_type = None):
        """
        Get an object given its identity hash.

        Optionally restrict the result by data type. Depending on the
        underlying database, this may result in a performance gain.

        :param identity: Identity hash.
        :type identity: str

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int

        :returns: Data object if found, None otherwise.
        :rtype: Data | None
        """
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_GET, identity, data_type)


    #--------------------------------------------------------------------------
    @staticmethod
    def get_many(identities, data_type = None):
        """
        Get an object given its identity hash.

        :param identities: Identity hashes.
        :type identities: list(str)

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int

        :returns: Data objects.
        :rtype: list(Data)
        """
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_GET_MANY, identities, data_type)


    #--------------------------------------------------------------------------
    @staticmethod
    def keys(data_type = None, data_subtype = None):
        """
        Get the identity hashes for all objects of the requested
        type, optionally filtering by subtype.

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int

        :param data_subtype: Optional data subtype.
        :type data_subtype: int | str

        :returns: Identity hashes.
        :rtype: set(str)
        """
        if data_type is None:
            if data_subtype is not None:
                raise NotImplementedError(
                    "Can't filter by subtype for all types")
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_KEYS, data_type, data_subtype)


    #--------------------------------------------------------------------------
    @staticmethod
    def count(data_type = None, data_subtype = None):
        """
        Count all objects of the requested type,
        optionally filtering by subtype.

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int

        :param data_subtype: Optional data subtype.
        :type data_subtype: int | str

        :returns: Count of requested objects.
        :rtype: int
        """
        if data_type is None:
            if data_subtype is not None:
                raise NotImplementedError(
                    "Can't filter by subtype for all types")
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_COUNT, data_type, data_subtype)


    #--------------------------------------------------------------------------
    @classmethod
    def iterate(self, data_type = None, data_subtype = None):
        """
        Iterate through all objects of the requested type,
        optionally filtering by subtype.

        :param data_type: Optional data type. One of the Data.TYPE_* values.
        :type data_type: int

        :param data_subtype: Optional data subtype.
        :type data_subtype: int | str

        :returns: Generator of Data objects.
        :rtype: generator(Data)
        """
        for identity in self.keys(data_type, data_subtype):
            yield self.get(identity)


    #--------------------------------------------------------------------------
    @staticmethod
    def get_plugin_history(identity):
        """
        Find out which plugins have already processed this data object.

        :param identity: Identity hash.
        :type identity: str

        :returns: Names of the plugins that already processed this data object.
        :rtype: set(str)
        """
        return Config._context.remote_call(
            MessageCode.MSG_RPC_DATA_PLUGINS, identity)


    #--------------------------------------------------------------------------
    @classmethod
    def __len__(self):
        return self.count()


    #--------------------------------------------------------------------------
    @classmethod
    def __contains__(self, data):
        try:
            identity = data.identity
        except AttributeError:
            identity = data
        return self.has_key(identity)


    #--------------------------------------------------------------------------
    @classmethod
    def __iter__(self):
        """
        Iterate through all objects of the database.

        :returns: Generator of Data objects.
        :rtype: generator(Data)
        """
        return self.iterate()
