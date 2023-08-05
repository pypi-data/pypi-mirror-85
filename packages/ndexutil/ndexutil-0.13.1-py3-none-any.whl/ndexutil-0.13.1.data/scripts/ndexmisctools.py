#!python

import os
import sys
import argparse
import logging
import json
import tempfile
import shutil
from requests.exceptions import HTTPError
import ndexutil
from ndexutil.tsv.streamtsvloader import StreamTSVLoaderFactory
from ndexutil.config import NDExUtilConfig
from ndexutil.exceptions import NDExUtilError
from ndex2.nice_cx_network import NiceCXNetwork
from ndex2.exceptions import NDExError
from ndex2.client import Ndex2
import ndex2
from ndexutil.cytoscape import CytoscapeLayoutCommand
from ndexutil.networkx import NetworkxLayoutCommand
from ndexutil.reports import FeaturedNetworkReportCommand
from ndexutil.cytoscape import Py4CytoscapeWrapper
from ndexutil.networkx import NetworkxLayoutWrapper
from ndexutil.ndex import NDExExtraUtils


# create logger
logger = logging.getLogger('ndexutil.ndexmisctools')


LOG_FORMAT = "%(asctime)-15s %(levelname)s %(relativeCreated)dms " \
             "%(filename)s::%(funcName)s():%(lineno)d %(message)s"


class Formatter(argparse.ArgumentDefaultsHelpFormatter,
                argparse.RawDescriptionHelpFormatter):
    pass


class CopyNetwork(object):
    """
    Copies NDEx network from one account to another
    account
    """
    COMMAND = 'copynetwork'

    def __init__(self, theargs):
        """
        Constructor
        :param theargs: command line arguments ie theargs.name theargs.type
        """
        self._args = theargs
        self._srcuser = None
        self._srcpass = None
        self._srcserver = None
        self._destuser = None
        self._destpass = None
        self._destserver = None

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._srcuser = con.get(self._args.profile,
                                'source_' + NDExUtilConfig.USER)
        self._srcpass = con.get(self._args.profile,
                                'source_' + NDExUtilConfig.PASSWORD)
        self._srcserver = con.get(self._args.profile,
                                  'source_' + NDExUtilConfig.SERVER)
        self._destuser = con.get(self._args.profile,
                                 'dest_' + NDExUtilConfig.USER)
        self._destpass = con.get(self._args.profile,
                                 'dest_' + NDExUtilConfig.PASSWORD)
        self._destserver = con.get(self._args.profile,
                                   'dest_' + NDExUtilConfig.SERVER)

    def run(self):
        """
        Downloads network from source and copies to destination
        :return:
        """
        self._parse_config()
        net = ndex2.create_nice_cx_from_server(self._srcserver,
                                               self._srcuser,
                                               self._srcpass,
                                               self._args.uuid)
        net.upload_to(self._destserver, self._destuser,
                      self._destpass)

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

            Version {version}

            The copynetwork command copies an NDEx network specified by --uuid
            to another user account.

            The source and destination accounts are specified by configuration
            in --conf under section set via --profile field

            Expected format in configuration file:
            [<value of --profile>]
            source_user = <user>
            source_pass = <password>
            source_server = <server>
            dest_user = = <user>
            dest_pass = <password>
            dest_server = <server>

            WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                     ERRORS. YOU HAVE BEEN WARNED.

            """.format(version=ndexutil.__version__)

        parser = subparsers.add_parser(CopyNetwork.COMMAND,
                                       help='Copies network in NDEx '
                                            'from one user to another',
                                       description=desc,
                                       formatter_class=Formatter)

        parser.add_argument('--uuid',
                            help='The UUID of network in NDEx to update')
        return parser


class NetworkAttributeSetter(object):
    """
    Sets network attributes on a network in NDEx
    """
    COMMAND = 'networkattribupdate'

    def __init__(self, theargs):
        """
        Constructor
        :param theargs: command line arguments ie theargs.name theargs.type
        """
        self._args = theargs
        self._user = None
        self._pass = None
        self._server = None

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        return Ndex2(self._server, self._user, self._pass)

    def _remove_existing_attribute(self, net_attribs):
        """
        Removes from net_attribs any dicts whose value of 'n'
        matches self._args.name
        :param net_attribs: network attributes
        :type net_attribs: list of dicts
        :return: None
        """
        items_to_delete = []
        for theindex, entry in enumerate(net_attribs):
            if entry['n'] == self._args.name:
                items_to_delete.append(theindex)

        items_to_delete.sort(reverse=True)
        for theindex in items_to_delete:
            del net_attribs[theindex]

    def _remove_name_description_summary(self, net_attribs):
        """
        Removes from net_attribs any dicts whose value of 'n'
        matches self._args.name
        :param net_attribs: network attributes
        :type net_attribs: list of dicts
        :return: None
        """
        excludelist = ['name', 'description', 'version']
        items_to_delete = []
        for theindex, entry in enumerate(net_attribs):
            if entry['n'] in excludelist:
                items_to_delete.append(theindex)
        items_to_delete.sort(reverse=True)
        for theindex in items_to_delete:
            del net_attribs[theindex]

    def _convert_attributes_to_ndexpropertyvaluepair(self, net_attribs):
        """
        The NDEx REST endpoint used in this class
        http://openapi.ndextools.org/#/Network/put_network__networkid__properties
        actually follows a legacy implementation that differs from CX format.

        This function converts the list of dicts into structure that will
        work with the REST service endpoint
        :return: updated list
        :rtype list of dicts
        """
        new_attribs = []
        for entry in net_attribs:
            newentry = {'predicateString': entry['n']}
            if 'd' in entry:
                newentry['dataType'] = entry['d']
                if entry['d'].startswith('list'):
                    newentry['value'] = json.dumps(entry['v'])
                else:
                    newentry['value'] = entry['v']
            else:
                newentry['value'] = entry['v']
            new_attribs.append(newentry)
        return new_attribs

    def _change_attribute_type(self, net_attribs):
        for entry in net_attribs:
            if entry['n'] == self._args.name:
                entry['d'] = self._args.type

    def _get_value(self, the_type, value):
        """
        Converts the value based on 'the_type' passed in

        :param the_type: type of value
        :type the_type: str
        :param value:
        :return:
        """
        import ast
        if the_type == 'double':
            return float(value)
        if the_type == 'long' or the_type == 'integer':
            return int(value)
        if the_type == 'boolean':
            return bool(value)
        return value

    def run(self):
        """
        Connects to NDEx server, gets network attributes for network
        with --uuid set on command line, updates network attributes
        with value set in --name, --value, --type and uses
        PUT network/<NETWORKID>/properties endpoint to update
        the network attributes for network
        :raises NDExUtilError if there is an error
        :return: number of attributes updated upon success
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')
        if self._args.name in ['name', 'description', 'version']:
            raise NDExUtilError('Sorry, but name, description, and version'
                                'CANNOT be updated by this call.')
        self._parse_config()

        client = self._get_client()
        res = client.get_network_aspect_as_cx_stream(self._args.uuid,
                                                     'networkAttributes')
        if res.status_code != 200:
            raise NDExUtilError('Received error status when querying'
                                'NDEx: ' + str(res.status_code) +
                                ' : ' + str(res.text))

        net_attribs = json.loads(res.text)

        # remove name description summary
        self._remove_name_description_summary(net_attribs)

        # Change attribute type only
        if self._args.typeonly:
            if self._args.value is not None:
                logger.warning('Ignoring --value ' +
                               str(self._args.value) +
                               ' since --typeonly flag is set')
            self._change_attribute_type(net_attribs)

            new_attribs =\
                self._convert_attributes_to_ndexpropertyvaluepair(net_attribs)
        else:
            # remove existing attribute if found
            self._remove_existing_attribute(net_attribs)

            new_attribs =\
                self._convert_attributes_to_ndexpropertyvaluepair(net_attribs)

            if self._args.value is not None:
                new_entry = {'predicateString': self._args.name}
                new_entry['dataType'] = self._args.type

                # depending of value of type need to case
                # resulting data appropriately
                new_entry['value'] = self._get_value(self._args.type,
                                                     self._args.value)

                new_attribs.append(new_entry)

        logger.debug(str(new_attribs))
        client.set_network_properties(self._args.uuid, new_attribs)
        return 0

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command updates network attributes on a network
        specified by --uuid with values set in --name, --type, and --value

        NOTE: Currently only 1 attribute can be updated at a time. Invoke
              multiple times to update several attributes at once.

        BIGPROBLEM: Due to issues on server
                    (we would need to make different call)
                    the network attributes name, version, and description
                    CANNOT be updated by this call and will currently
                    return an error

        To set the --value with list data follow these rules:
        
         If --type is 'list_of_string', use brackets and quote each
         value like so:
          
           "[\\"pathway\\",\\"interactome\\"]"
          
         If --type is 'list_of_integer|double|boolean' then use brackets
         and list elements as follows:
         
           "[1, 2, 3]"
           
         If --type is 'list_of_boolean' then use brackets and
         enter 'true' and 'false' (MUST BE LOWER CASE)
         
           "[true, false, true]"
 
        Returns 0 upon success otherwise error.

        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=NetworkAttributeSetter.COMMAND)

        parser = subparsers.add_parser(NetworkAttributeSetter.COMMAND,
                                       help='Updates network attributes on network in NDEx',
                                       description=desc,
                                       formatter_class=Formatter)

        parser.add_argument('--uuid',
                            help='The UUID of network in NDEx to update',
                            required=True)
        parser.add_argument('--name',
                            help='Name of attribute',
                            required=True)
        parser.add_argument('--type',
                            choices=['string', 'double', 'boolean',
                                     'integer', 'long', 'list_of_integer',
                                     'list_of_long', 'list_of_double',
                                     'list_of_boolean',
                                     'list_of_string'],
                            help='Type of attribute',
                            default='string')
        parser.add_argument('--value',
                            help='Value of attribute, if unset then '
                                 'attribute is removed, unless --typeonly '
                                 'is set. See help above for how to pass '
                                 'a list of data')
        parser.add_argument('--typeonly', default=False, action='store_true',
                            help='If set, only the type of the attribute will '
                                 'be updated, and the value will not be '
                                 'changed')
        return parser


class NodeAttributeAdder(object):
    """
    Adds attribute to nodes on a network in NDEx
    """
    COMMAND = 'addnodeattrib'

    def __init__(self, theargs, altclient=None):
        """
        Constructor
        :param theargs: command line arguments ie theargs.name theargs.type
        """
        self._args = theargs

        self._user = None
        self._pass = None
        self._server = None
        self._altclient = altclient

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        if self._altclient is not None:
            return self._altclient
        return Ndex2(self._server, self._user, self._pass)

    def _get_network(self, client, network_uuid):
        """
        Gets network from NDEx

        :param client:
        :type client: :py:class:`~ndex2.client.Ndex2`
        :param network_uuid: id of network in NDEx
        :type network_uuid: str
        :raises NDExUtilError: If there is any error
        :return: Network
        :rtype: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        """
        try:
            res = client.get_network_as_cx_stream(network_uuid)
        except Exception as e:
            raise NDExUtilError('Caught an exception downloading'
                                ' network: ' + str(e))

        if res.status_code != 200:
            raise NDExUtilError('Unable to download network '
                                'with id: ' + str(network_uuid) + ' from NDEx')

        try:
            return ndex2.create_nice_cx_from_raw_cx(res.json())
        except Exception as e:
            raise NDExUtilError('Caught an exception converting downloaded network'
                                'to NiceCXNetwork object: ' + str(e))

    def _get_nodes_to_skip(self):
        """
        Gets a list of nodes to skip

        :return: list of node ids
        :rtype: list
        """
        if self._args.nodestoskip is None:
            return []
        node_list = []
        for node_id in self._args.nodestoskip.split(','):
            try:
                node_list.append(int(node_id))
            except ValueError:
                raise NDExUtilError('Non numeric node id in '
                                    '--nodestoskip parameter: ' +
                                    str(node_id))
        return node_list

    def _get_value_in_correct_type(self):
        """
        Casts the value set via --value to correct type and
        return it
        :return:
        """
        if self._args.type is None or self._args.type == 'string':
            return self._args.value

        try:
            if self._args.type == 'integer' or self._args.type == 'long':
                return int(self._args.value)
            if self._args.type == 'double':
                return float(self._args.value)
            if self._args.type == 'boolean':
                return bool(self._args.value)
        except ValueError as ve:
            raise NDExUtilError('Unable to convert --value ' +
                                str(self._args.value) + ' to ' +
                                self._args.type + ' : ' + str(ve))

    def run(self):
        """
        Connects to NDEx server, downloads network(s) specified by --uuid
        or by --networkset and applies style specified by --style flag
        updating those networks in place on the server.
        WARNING: This is very inefficient method since the full network
                 is downloaded and uploaded. YOU HAVE BEEN WARNED.

        :raises NDExUtilError if there is an error
        :return: number of networks updated
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')

        value_with_correct_type = self._get_value_in_correct_type()
        self._parse_config()
        client = self._get_client()
        net = self._get_network(client, self._args.uuid)
        node_skip_list = self._get_nodes_to_skip()
        for node_id, node in net.get_nodes():
            if node_id in node_skip_list:
                logger.info(str(node_id) + ' in skip list. Skipping...')
                continue
            net.set_node_attribute(node_id, self._args.name,
                                   value_with_correct_type, type=self._args.type,
                                   overwrite=True)

        client.update_cx_network(net.to_cx_stream(), self._args.uuid)

        return 0

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command adds a node attribute to network specified by
        by --uuid

        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=NodeAttributeAdder.COMMAND)

        parser = subparsers.add_parser(NodeAttributeAdder.COMMAND,
                                       help='Adds new attribute to all nodes',
                                       description=desc,
                                       formatter_class=Formatter)

        parser.add_argument('--uuid',
                            default=None,
                            help='The UUID of the network in NDEx to add the '
                                 'node attribute to')

        parser.add_argument('--name',
                            default=None, required=True,
                            help='Name of node attribute')
        parser.add_argument('--value',
                            default=None, required=True,
                            help='Value of node attribute')
        parser.add_argument('--type',
                            default=None,
                            choices=[None, 'string', 'integer',
                                     'long', 'boolean', 'double'],
                            help='Data type, if unset, it assumed to be '
                                 'string. '
                                 'Currently list attributes are NOT supported')
        parser.add_argument('--nodestoskip',
                            help='Comma delimited list of node ids '
                                 'to SKIP or NOT add attribute to')
        return parser


class NodeAttributeRemover(object):
    """
    Removes attribute from nodes on a network in NDEx
    """
    COMMAND = 'removenodeattrib'

    def __init__(self, theargs, altclient=None):
        """
        Constructor
        :param theargs: command line arguments ie theargs.name theargs.type
        """
        self._args = theargs
        self._altclient = altclient
        self._user = None
        self._pass = None
        self._server = None
        self._client = None

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        if self._altclient is not None:
            return self._altclient
        return Ndex2(self._server, self._user, self._pass)

    def _get_network(self, client, network_uuid):
        """
        Gets network from NDEx

        :param client:
        :type client: :py:class:`~ndex2.client.Ndex2`
        :param network_uuid: id of network in NDEx
        :type network_uuid: str
        :raises NDExUtilError: If there is any error
        :return: Network
        :rtype: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        """
        try:
            res = client.get_network_as_cx_stream(network_uuid)
        except Exception as e:
            raise NDExUtilError('Caught an exception downloading'
                                ' network: ' + str(e))

        if res.status_code != 200:
            raise NDExUtilError('Unable to download network '
                                'with id: ' + str(network_uuid) + ' from NDEx')

        try:
            return ndex2.create_nice_cx_from_raw_cx(res.json())
        except Exception as e:
            raise NDExUtilError('Caught an exception converting downloaded network'
                                'to NiceCXNetwork object: ' + str(e))

    def _get_nodes_to_include(self):
        """
        Gets a list of nodes to include from
        --nodestoinclude parameter

        :raises NDExUtilError: If a node id is non numeric
        :return: list of node ids or None if there are none
        :rtype: list
        """
        if self._args.nodestoinclude is None:
            return None
        node_list = None
        for node_id in self._args.nodestoinclude.split(','):
            try:
                if node_list is None:
                    node_list = []
                node_list.append(int(node_id))
            except ValueError as ve:
                raise NDExUtilError('Non numeric node id in '
                                    '--nodestoinclude parameter: ' +
                                    str(node_id))
        return node_list

    def run(self):
        """
        Connects to NDEx server, downloads network(s) specified by --uuid
        and removes all node attributes matching name set via --name
        flag and updating that network in place on the server.
        WARNING: This is very inefficient method since the full network
                 is downloaded and uploaded. YOU HAVE BEEN WARNED.
        :raises NDExUtilError if there is an error
        :return: number of networks updated
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')

        self._parse_config()
        client = self._get_client()
        net = self._get_network(client, self._args.uuid)
        node_include_list = self._get_nodes_to_include()
        for node_id, node in net.get_nodes():
            if node_include_list is None or node_id in node_include_list:
                logger.info(str(node_id) + ' removing attribute')
                net.remove_node_attribute(node_id, self._args.name)

        client.update_cx_network(net.to_cx_stream(), self._args.uuid)

        return 0

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command removes a node attribute to network specified by
        by --uuid

        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=NodeAttributeRemover.COMMAND)

        parser = subparsers.add_parser(NodeAttributeRemover.COMMAND,
                                       help='Removes attribute from all nodes',
                                       description=desc,
                                       formatter_class=Formatter)

        parser.add_argument('--uuid',
                            default=None,
                            help='The UUID of the network in NDEx to add the '
                                 'node attribute to')

        parser.add_argument('--name',
                            default=None, required=True,
                            help='Name of node attribute')
        parser.add_argument('--nodestoinclude',
                            help='Comma delimited list of node ids '
                                 'to remove attribute from')
        return parser


class StyleUpdator(object):
    """
    Updates style on a network in NDEx
    """

    COMMAND = 'styleupdate'

    def __init__(self, theargs, altclient=None):
        """
        Constructor

        :param theargs: command line arguments ie theargs.name theargs.type
        """
        self._args = theargs

        self._user = None
        self._pass = None
        self._server = None
        self._client = None
        self._altclient = altclient
        self._count = None
        self._style = None
        self._old_to_new = None

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`

        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        if self._altclient is not None:
            return self._altclient
        return Ndex2(self._server, self._user, self._pass)

    def _get_style_file(self, file):
        """
        Loads :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        from 'file'

        :param file: Path to file containing CX network to load
        :type file: str
        :return: network loaded from 'file' passed in
        :rtype: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        """
        return ndex2.create_nice_cx_from_file(file)

    def _get_networks_from_networkset(self, uuid):
        """
        Gets networks from networkset with id 'uuid' from
        server

        :param uuid: NDEx networkset id
        :type uuid: str
        :return: NDEx UUIDs of networks belonging to networkset
        :rtype: list
        """
        info = self._client.get_networkset(uuid)
        return info['networks']

    def _get_network(self, uuid):
        """
        Gets network with NDEx UUID of 'uuid' from NDEx server

        :param uuid: NDEx UUID identifying network
        :type uuid: str
        :return: Network
        :rtype: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        """
        return ndex2.create_nice_cx_from_server(
            self._server,
            username=self._user,
            password=self._pass,
            uuid=uuid)

    def _get_network_visibility(self, uuid):
        """
        Gets visibility of network of network with NDEx UUID of 'uuid'
        from server

        :param uuid: NDEx UUID identifying network
        :type uuid: str
        :return:
        """
        return self._client.get_network_summary(uuid)['visibility']

    def _get_network_and_visibility(self, uuid):
        """
        Gets a tuple containing network and its visibility for
        network with NDEx UUID of 'uuid'

        :param uuid: NDEx UUID identifying network
        :type uuid: str
        :return: (network, network visibility)
        :rtype: tuple (:py:class:`~ndex2.nice_cx_network.NiceCXNetwork`, str)
        """
        return self._get_network(uuid), self._get_network_visibility(uuid)
    
    def _create_new_network(self, old_uuid, network, visibility):
        """
        Adds 'network' as a new network on NDEx with visibility
        set via the 'visibility' flag. Method also updates
        self._old_to_new dict setting key to old UUID of network and
        value set to UUID of newly created network

        :param old_uuid: NDEx UUID of old/original network
        :type old_uuid: str
        :param network:
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :param visibility: visibility of network on NDEx
        :type visibility: str
        """
        uri = self._client.save_new_network(network.to_cx(), visibility)
        new_uuid = self._get_id_from_uri(uri)
        self._old_to_new[old_uuid] = new_uuid

    def _apply_style_from_file_to_new_network(self, uuid):
        network, visibility = self._get_network_and_visibility(uuid)
        network.apply_style_from_network(self._style)
        self._create_new_network(uuid, network, visibility)
        self._count += 1

    def _apply_style_from_uuid_to_new_network(self, uuid):
        network, visibility = self._get_network_and_visibility(uuid)
        network.apply_template(server=self._server,
                               username=self._user,
                               password=self._pass,
                               uuid=self._args.styleuuid)
        self._create_new_network(uuid, network, visibility)
        self._count += 1

    def _apply_style_from_file_to_original_network(self, uuid):
        network = self._get_network(uuid)
        network.apply_style_from_network(self._style)
        self._client.update_cx_network(network.to_cx_stream(), uuid)
        self._count += 1

    def _apply_style_from_uuid_to_original_network(self, uuid):
        network = self._get_network(uuid)
        network.apply_template(server=self._server,
                               username=self._user,
                               password=self._pass,
                               uuid=self._args.styleuuid)
        self._client.update_cx_network(network.to_cx_stream(), uuid)
        self._count += 1

    def _get_id_from_uri(self, uri):
        return uri.split('/')[-1]

    def _copy_networkset(self, networkset_uuid):
        """
        Creates a new networkset and adds in all new
        networks into that set. The new network set is
        named Copy of <ORIGINAL NETWORKSET NAME>

        If the there is an error creating the copy of the
        network set, the operation is attempted again
        where the networkset name is set to
        Copy of <ORIGINAL NETWORKSET NAME> (COPY NUMBER STARTING AT 1)

        Example if original network set is foo:

        If successful on first try network set will be named:
        Copy of foo

        If failure on first try, but second works network set will
        be named:
        Copy of foo (1)

        :param networkset_uuid: NDEx UUID identifying networkset to copy
        :type networkset_uuid: str
        :return: id of new networkset
        :rtype: str
        """

        info = self._client.get_networkset(networkset_uuid)
        name = info['name']
        description = info['description']

        # Make sure network set name is unique
        copy_number = 0
        while copy_number < self._args.networksetretry:
            try:
                if copy_number == 0:
                    copy_string = ''
                else:
                    copy_string = ' (' + str(copy_number) + ')'
                netset_name = 'Copy of ' + name + copy_string
                uri = self._client.create_networkset(netset_name,
                                                     description)
                # Copy put new networks in new network set
                networkset_id = self._get_id_from_uri(uri)
                networks = list(self._old_to_new.values())
                self._client.add_networks_to_networkset(networkset_id,
                                                        networks)
                return networkset_id
            except HTTPError as e:
                logger.warning('Attempting to create'
                               'network set named ' +
                               netset_name +
                               ' failed, possibly due to ' +
                               'duplicate name : ' + str(e))
            copy_number += 1

        raise NDExUtilError('After ' + str(self._args.networksetretry) +
                            ' attempts unable to create a network set with ' +
                            ' name of Copy of ' + name + ' (#)')

    def _get_new_uuid_string(self, old_uuid, new_uuid):
        """
        Creates string reporting what network was copied to what

        :param old_uuid: NDEx UUID identifying a network
        :type old_uuid: str
        :param new_uuid: NDEx UUID identifying a network
        :type new_uuid: str
        :return: Message about what network was copied
        :rtype: str
        """
        return ('Network with uuid {old_uuid} was copied to network with '
                'uuid {new_uuid}').format(old_uuid=old_uuid,
                                          new_uuid=new_uuid)

    def _print_new_networkset_uuids(self, old_networkset_id, new_networkset_id):
        old_name = self._client.get_networkset(old_networkset_id)['name']
        new_name = self._client.get_networkset(new_networkset_id)['name']
        print_string = ('\nNetworks in old networkset "{old_name}" ({old_uuid}) '
                        'have been copied to new networkset "{new_name}" '
                        '({new_uuid}) with new style:').format(
                           old_name=old_name, 
                           old_uuid=old_networkset_id,
                           new_name=new_name,
                           new_uuid=new_networkset_id)
        for old_network, new_network in self._old_to_new.items():
            print_string += '\n\t' + self._get_new_uuid_string(
                                        old_network, new_network)
        print(print_string + '\n')

    def _get_style_function_to_use(self):
        """

        :return:
        """
        if self._args.stylefile:
            self._style = self._get_style_file(self._args.stylefile)
            if self._args.newcopy:
                return self._apply_style_from_file_to_new_network
            else:
                return self._apply_style_from_file_to_original_network
        if self._args.newcopy:
            return self._apply_style_from_uuid_to_new_network
        else:
            return self._apply_style_from_uuid_to_original_network

    def _update_networkset_style(self,
                                 style_function=None):
        """
        Updates style on networks in network set with id
        `self._args.networkset` using `style_function` passed in.
        If `self._args.newcopy` is True then new networks are uploaded
        along with networkset otherwise update occurs in place

        :param style_function: function that takes NDEx networkset UUID
                               to apply styles to networks
        :type style_function: python function
        :return: 0 for success
        :rtype: int
        """
        uuids = self._get_networks_from_networkset(self._args.networkset)
        for uuid in uuids:
            style_function(uuid)
        if self._args.newcopy:
            # Make new networkset
            networkset_uuid = self._copy_networkset(self._args.networkset)
            # Print new uuids
            self._print_new_networkset_uuids(
                self._args.networkset,
                networkset_uuid)
        return 0

    def _update_network_style(self, style_function=None):
        """
        Updates style of network with id `self._args.uuid`
        via `style_function`. If `self._args.newcopy` is True then
        a new network is uploaded otherwise update occurs in place

        :param style_function:
        :return:
        """
        style_function(self._args.uuid)
        if self._args.newcopy:
            print('\n' + self._get_new_uuid_string(
                self._args.uuid,
                self._old_to_new[self._args.uuid]) + '\n')
        return 0

    def run(self):
        """
        Connects to NDEx server, downloads network(s) specified by
        --uuid or by --networkset and applies style specified by
        --styleuuid or --stylefile flag
        updating those networks in place on the server unless --newcopy
        flag is set in which case new networks and networkset is created
        WARNING: This is very inefficient method since the full network
                 is downloaded and uploaded. YOU HAVE BEEN WARNED.

        :raises NDExUtilError if there is an error
        :return: 0 upon success
        :rtype: int
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')

        self._parse_config()
        self._client = self._get_client()

        # Set up counter
        self._count = 0

        # setup dict for mapping of old network to
        # new network
        if self._args.newcopy:
            self._old_to_new = {}

        # Find function to use
        style_function = self._get_style_function_to_use()

        # Apply style to networkset networks
        if self._args.networkset is not None:
            return self._update_networkset_style(style_function=style_function)

        # Apply style to single network
        return self._update_network_style(style_function=style_function)

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command updates the style of a network or networks specified 
        by --uuid or --networkset with the style specified by --styleuuid or
        --stylefile flags.
        
        NOTE: Either --uuid or --networkset must be specified and either
              --styleuuid or --stylefile must be specified.

        If --newcopy flag is set then new networks will be uploaded with
        same name. If --networkset is also specified, a new network set will
        be created and named Copy of <ORIG NAME> and if that exists then
        (#) will be appended to name starting at 1. 
        
        For example, if networkset is named foo and Copy of foo exists then
        the new networkset will be named Copy of foo (1). If Copy of foo (1)
        is taken then Copy of foo (2) will be created. This goes on until
        the value in (#) reaches value of --networksetretry which is set
        to a default of 50. 
        
        
        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=StyleUpdator.COMMAND)

        parser = subparsers.add_parser(StyleUpdator.COMMAND,
                                       help='Updates style of network on NDEx',
                                       description=desc,
                                       formatter_class=Formatter)
        src_grp = parser.add_mutually_exclusive_group(required=True)
        src_grp.add_argument('--uuid', default=None,
                             help='The UUID of the network in NDEx to '
                                  'apply the new style to. Either this '
                                  'flag or --networkset must be specified '
                                  'on the commandline')
        src_grp.add_argument('--networkset', default=None,
                             help='The UUID of the network set in NDEx to '
                                  'apply the new style to. Either this '
                                  'flag or --uuid must be specified on the '
                                  'commandline')
        style_src_grp = parser.add_mutually_exclusive_group(required=True)
        style_src_grp.add_argument('--styleuuid',
                                   default=None,
                                   help='The UUID of the network whose '
                                        'style should be applied to the '
                                        'other networks. Either this flag '
                                        'or --stylefile must be specified '
                                        'on the commandline')
        style_src_grp.add_argument('--stylefile',
                                   default=None,
                                   help='The path to a cx file whose '
                                        'style should be applied to '
                                        'the other networks. Either this '
                                        'flag or --styleuuid must be '
                                        'specified on the commandline')
        parser.add_argument('--newcopy',
                            default=False,
                            action='store_true',
                            help='If set, a new copy of each network or '
                            'network set will be made, and the original '
                            'or network set will not be changed')
        parser.add_argument('--networksetretry', default=50, type=int,
                            help='Maximum number of retries before failing '
                                 'to make a copy of a network set. The'
                                 'failure is usually due to a networkset'
                                 'with an identical name')
        return parser


class UpdateNetworkSystemProperties(object):
    """
    Updates system properties on network in NDEx
    """
    COMMAND = 'systemproperty'

    def __init__(self, theargs):
        """
        Constructor
        :param theargs: command line arguments ie theargs.name theargs.type
        """
        self._args = theargs
        self._user = None
        self._pass = None
        self._server = None

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        return Ndex2(self._server, self._user, self._pass)

    def _get_uuid_list_from_args(self, client):
        """
        Looks at command line args in self._args and
        if self._args.uuid is set grabs that otherwise
        looks at self._args.networksetid and queries for all
        networks in that networkset
        :return: list of network UUIDs as strings
        :rtype: list
        """
        # if uuid is set then just return that in a list
        try:
            if isinstance(self._args.uuid, str):
                return [self._args.uuid]
        except AttributeError:
            pass

        # if networksetid is set then query
        # ndex for all uuids and return them in a list
        try:
            res = client.get_networkset(self._args.networksetid)
            logger.debug('networks: ' + str(res['networks']))
            return res['networks']
        except HTTPError:
            logger.exception('Caught exception querying for networks in '
                             'networkset')
            return None

    def run(self):
        """
        Connects to NDEx server, downloads network(s) specified by --uuid
        or by --networkset and applies style specified by --style flag
        updating those networks in place on the server.
        WARNING: This is very inefficient method since the full network
                 is downloaded and uploaded. YOU HAVE BEEN WARNED.

        :raises NDExUtilError if there is an error
        :return: number of networks updated
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')

        self._parse_config()

        client = self._get_client()
        uuidlist = self._get_uuid_list_from_args(client)
        if uuidlist is None:
            return 1
        prop_dict = {}
        try:
            if self._args.showcase is True:
                prop_dict['showcase'] = True
        except AttributeError:
            pass

        try:
            if self._args.disableshowcase is True:
                prop_dict['showcase'] = False
        except AttributeError:
            pass

        try:
            if self._args.indexlevel is not None:
                prop_dict['index_level'] = self._args.indexlevel.upper()
        except AttributeError:
            pass

        try:
            if self._args.visibility is not None:
                prop_dict['visibility'] = self._args.visibility.upper()
        except AttributeError:
            pass
        error_count = 0
        for netid in uuidlist:
            try:
                logger.debug('Updating network: ' + str(netid) +
                             ' sysprops:  ' + str(prop_dict))
                res = client.set_network_system_properties(netid, prop_dict)
                if res != '':
                    error_count += 1
            except NDExError:
                logger.exception('Caught NDExError trying to set '
                                 'network props')
                error_count += 1
            except HTTPError:
                logger.exception('Caught HTTPError trying to set '
                                 'network props')
                error_count += 1
        if error_count > 0:
            return 1
        return 0

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command updates system properties on a network
        specified by --uuid, or all networks under a given
        networkset via --networksetid

        Currently this command supports updating the following
        attributes: showcase, visibility, and indexing.

        If no flags are set for a given attribute then that value is NOT
        modified

        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=NetworkAttributeSetter.COMMAND)

        parser = subparsers.add_parser(UpdateNetworkSystemProperties.COMMAND,
                                       help='Updates system properties on '
                                            'network in NDEx',
                                       description=desc,
                                       formatter_class=Formatter)

        id_grp = parser.add_mutually_exclusive_group()

        id_grp.add_argument('--uuid',
                            help='The UUID of network in NDEx to update')
        id_grp.add_argument('--networksetid',
                            help='The UUID of networkset which will '
                                 'update all networks within set')
        showcase_grp = parser.add_mutually_exclusive_group()
        showcase_grp.add_argument('--showcase', action='store_true',
                                  help='If set, network will be showcased')
        showcase_grp.add_argument('--disableshowcase', action='store_true',
                                  help='If set, network will NOT be showcased')
        parser.add_argument('--indexlevel',
                            choices=['none', 'meta', 'all'],
                            help='If set, network indexing will be updated')
        parser.add_argument('--visibility',
                            choices=['public', 'private'],
                            help='If set, updates visibility of network')
        return parser


class LayoutWrapper(object):
    """
    Wrapper class to apply a layout to a network
    """
    def __init__(self, netx_layout=NetworkxLayoutWrapper(),
                 cyto_layout=Py4CytoscapeWrapper(),
                 ndexextra=NDExExtraUtils()):
        """
        Constructor
        """
        self._netx_layout = netx_layout
        self._cyto_layout = cyto_layout
        self._ndexextra = ndexextra

    def apply_layout(self, layout=None,
                     input_cx_file=None,
                     output_cx_file=None,
                     center=None,
                     scale=None,
                     base_url=ndexutil.cytoscape.DEFAULT_CYREST_API):
        """

        :param layout: layout to run supports 'spring' from networkx and
                       if Cytoscape is running with py4cytoscape installed
                       then any cytoscape layout
        :type layout: str
        :param input_cx_file:
        :type input_cx_file: str
        :param output_cx_file:
        :type output_cx_file: str
        :param center:
        :param scale:
        :param base_url: Cytoscape REST endpoint passed to py4cytoscape
        :type base_url: str
        :return:
        """
        if layout is None:
            raise NDExUtilError('Layout is None')

        if layout == 'spring':
            self._netx_layout.apply_layout(layout=layout,
                                           input_cx_file=input_cx_file,
                                           output_cx_file=output_cx_file,
                                           center=center,
                                           scale=scale)
            return
        if self._cyto_layout.is_py4cytoscape_loaded() is False:
            raise NDExUtilError('py4cytoscape is not loaded ')

        try:
            self._cyto_layout.cytoscape_ping()
        except Exception as e:
            raise NDExUtilError('WARNING: A locally running Cytoscape was '
                                'not found Please start Cytoscape on '
                                'this machine : ' + str(e))
        adjusted_layout = layout
        if adjusted_layout == '-':
            adjusted_layout = 'force-directed-cl'
        tmp_output = output_cx_file + '.tmp.cx'
        self._ndexextra.add_node_id_as_node_attribute(cxfile=input_cx_file,
                                                      outcxfile=tmp_output)

        net_dict = self._cyto_layout.import_network_from_file(tmp_output,
                                                              base_url=base_url)

        if 'networks' not in net_dict:
            raise NDExUtilError('Error network view could not '
                                'be created, this could be cause '
                                'this network is larger then '
                                '100,000 edges. Try increasing '
                                'viewThreshold property in '
                                'Cytoscape preferences')

        net_suid = net_dict['networks'][0]
        logger.info('Applying layout ' + adjusted_layout +
                    ' on network with suid: ' +
                    str(net_suid) + ' in Cytoscape')

        res = self._cyto_layout.layout_network(layout_name=adjusted_layout,
                                               network=net_suid,
                                               base_url=base_url)
        logger.debug(res)

        # remove destination file to prevent cytoscape hang
        if os.path.isfile(tmp_output):
            os.unlink(tmp_output)

        self._cyto_layout.export_network(filename=tmp_output,
                                         type='CX', network=net_suid,
                                         base_url=base_url)
        layout_data = self._ndexextra.\
            extract_layout_aspect_from_cx(input_cx_file=tmp_output)
        if layout_data is None:
            raise NDExUtilError('No layout data found in result')
        net = ndex2.create_nice_cx_from_file(input_cx_file)
        net.set_opaque_aspect('cartesianLayout', layout_data)
        with open(output_cx_file, 'w') as f:
            json.dump(net.to_cx(), f)


class TSVLoader(object):
    """
    Runs tsvloader to import data as a network into NDEx
    """
    COMMAND = 'tsvloader'

    def __init__(self, theargs, altclient=None,
                 streamtsvfac=StreamTSVLoaderFactory(),
                 layout_wrapper=LayoutWrapper()):
        """
        Constructor
        :param theargs: command line arguments from argparse. This method
                        expects the following to be set: theargs.username,
                        theargs.password, theargs.server and if any of these
                        three are '-' theargs.conf must be None or a path to
                        directory containing a valid configuration file
        :raises ConfigError: if there was a problem parsing the
                             configuration file
        """
        self._args = theargs
        self._user = self._args.username
        self._pass = self._args.password
        self._server = self._args.server
        self._tmpdir = None  # set in run() function
        self._altclient = altclient
        self._tsvfac = streamtsvfac
        self._layout = layout_wrapper
        self._parse_config()

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        if self._user != '-' and self._pass != '-' and self._server != '-':
            return
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        if self._user == '-':
            self._user = con.get(self._args.profile, NDExUtilConfig.USER)

        if self._pass == '-':
            self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)

        if self._server == '-':
            self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        if self._altclient is not None:
            return self._altclient
        return Ndex2(self._server, self._user, self._pass)

    def _get_aspect_from_server(self, client, aspect):
        """

        :param client:
        :return:
        """
        try:
            logger.debug('Downloading ' + aspect + ' for network ' +
                         str(self._args.t) + ' from NDEx')
            res = client.get_network_aspect_as_cx_stream(self._args.t,
                                                         aspect)
            return json.loads(res.text)
        except HTTPError as e:
            logger.exception('Got error trying to get ' + aspect + ' ' +
                             str(e))
        return None

    def _get_stripped_down_style_cx_from_server(self, client):
        """
        Downloads only network attributes and visual properties from
        the template network on NDEx and creates a network from this
        data. This is done to reduce IO if a large network was used
        as a template.

        :param client: NDEx2 python client object with valid credentials
        :type client: :py:class:`~ndex2.client.Ndex2`
        :return: network object with only networkAttributes
                 and cyVisualProperties set
        :rtype: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        """
        net_a = self._get_aspect_from_server(client,
                                             'networkAttributes')

        style_a = self._get_aspect_from_server(client,
                                               'cyVisualProperties')
        if style_a is None:
            style_a = self._get_aspect_from_server(client,
                                                   'visualProperties')

        cx_dict = [{'numberVerification': [{'longNumber': 281474976710655}]}]
        meta_dict = dict()
        meta_dict['metaData'] = []
        cx_dict.append(meta_dict)

        if net_a is not None:
            meta_dict['metaData'].append({'name': 'networkAttributes',
                                          'elementCount': len(net_a),
                                          'idCounter': len(net_a),
                                          'version': "1.0",
                                          'consistencyGroup': 1,
                                          'properties': []})
            cx_dict.append({'networkAttributes': net_a})

        if style_a is not None:
            meta_dict['metaData'].append({'name': 'cyVisualProperties',
                                          'elementCount': len(style_a),
                                          'idCounter': len(style_a),
                                          'version': "1.0",
                                          'consistencyGroup': 1,
                                          'properties': []})
            cx_dict.append({'cyVisualProperties': style_a})
        if style_a is None:
            raise NDExUtilError('No style found on template network: ' +
                                self._args.t)

        return ndex2.create_nice_cx_from_raw_cx(cx_dict)

    def _get_cx_style(self, client=None):
        """
        Attempts to get :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        from -t argument which can be a path to a file or a NDEx UUID
        that can be retrieved from NDEx server
        :raises JSONDecodeError: if CX file is not valid JSON
        :return: network or None if not found
        :rtype: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        """
        if self._args.t is None:
            logger.info('Template network is not set')
            return None

        # if argument is a file try loading it
        if os.path.isfile(os.path.abspath(self._args.t)):
            self._args.t = os.path.abspath(self._args.t)
            logger.info('Loading template network from file: ' + self._args.t)
            return ndex2.create_nice_cx_from_file(self._args.t)

        if len(self._args.t) > 40 or len(self._args.t) < 36:
            raise NDExUtilError(str(self._args.t) + ' does not appear to be'
                                                    ' a valid NDEx UUID')

        # otherwise assume its a UUID and try getting it from server
        logger.info('Downloading template network from NDEx')
        return self._get_stripped_down_style_cx_from_server(client)

    def _get_network_attributes(self, cxnetwork):
        """
        Gets network attributes from network passed in. The network
        attributes are stored in the 'networkAttributes' aspect
        :param cxnetwork: network to get network attributes
        :type cxnetwork: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: None if not found or list of dicts with each dict in
                 format of:
                 {'n': 'NAME','v': 'VALUE', 'd': 'DATA TYPE'}
                 NOTE: the 'd' is optional and if missing DATA_TYPE is
                 'string'
        :rtype: list
        """
        if cxnetwork is None or self._args.copyattribs is False:
            temp_network = NiceCXNetwork()
        else:
            temp_network = cxnetwork

        if self._args.name is not None:
            temp_network.set_name(self._args.name.replace('"', ''))

        if self._args.description is not None:
            temp_network.set_network_attribute('description',
                                               values=self._args.description.
                                               replace('"', ''),
                                               type='string')

        # this is not efficient cause it converts
        # the whole network to CX in memory
        for element in temp_network.to_cx():
            if 'networkAttributes' in element:
                for net_a in element['networkAttributes']:
                    if net_a['n'] == '@context':
                        element['networkAttributes'].remove(net_a)
                return element['networkAttributes']
        return None

    def _upload_network(self, client, networkfile):
        """
        Uploads or updates network in NDEx
        :param networkfile:
        :return:
        """

        with open(networkfile, 'rb') as net_stream:
            try:
                if self._args.u is not None:
                    logger.info('Updating network in NDEx')
                    logger.info('Output from updating network in NDEx: ' +
                                client.update_cx_network(net_stream,
                                                         self._args.u))
                    return 0
                logger.info('Saving new network to NDEx')
                logger.info('Output from saving network to NDEx: ' +
                            client.save_cx_stream_as_new_network(net_stream))
            except HTTPError as he:
                if '401 Client Error' in str(he):
                    logger.fatal('Error uploading network. '
                                 'Invalid username "' + str(self._user) +
                                 '" and/or password '
                                 'for server "' + str(self._server) + '"')
                    return 2
                else:
                    logger.exception('Caught exception trying to '
                                     'upload network: ' + str(he))
                return 3

        return 0

    def _get_tsvfile(self):
        """
        Returns path to TSV file stored normally in self._args.tsv_file
        unless user set --header in which case the contents of
        header are written to a tmp file and the self._args.tsv_file is
        appended to this tmp file so the tsv file has a header
        :return:
        """

        if self._args.header is not None:
            logger.info('Prepending custom header to tsv file')
            tmptsv = os.path.join(self._tmpdir, 'temp.tsv')
            with open(os.path.abspath(self._args.tsv_file), 'r') as tsv_input:
                with open(tmptsv, 'w') as f:
                    f.write(self._args.header + '\n')
                    shutil.copyfileobj(tsv_input, f)
            return tmptsv
        if self._args.uppercaseheader is True:
            logger.info('Upper casing header line in tsv file')
            tmptsv = os.path.join(self._tmpdir, 'temp.tsv')
            with open(os.path.abspath(self._args.tsv_file), 'r') as tsv_input:
                with open(tmptsv, 'w') as f:
                    f.write(tsv_input.readline().upper())
                    for line in tsv_input:
                        f.write(line)
            return tmptsv

        return self._args.tsv_file

    def _get_streamtsvloader(self, stylenetwork):
        """
        Gets streamtsvloader from factory
        :return:
        """
        return self._tsvfac.get_tsv_streamloader(self._args.load_plan,
                                                 stylenetwork)

    def run(self):
        """

        :raises NDExUtilError if there is an error
        :return: 0 upon success otherwise failure
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')

        client = self._get_client()
        self._tmpdir = tempfile.mkdtemp(dir=self._args.tmpdir)
        try:
            # get network containing style and network attributes
            stylenetwork = self._get_cx_style(client)

            # extract network attributes from stylenetwork
            net_attribs = self._get_network_attributes(stylenetwork)

            # create tsv loader
            tsvloader = self._get_streamtsvloader(stylenetwork)

            # create input stream and output stream which is fed
            # to tsv loader to create cx
            cxout = os.path.join(self._tmpdir, 'tsvloader.cx')
            with open(self._get_tsvfile(), 'r') as tsv_in_stream:
                with open(cxout, 'w') as cx_out_stream:
                    tsvloader.write_cx_network(tsv_in_stream, cx_out_stream,
                                               network_attributes=net_attribs)

            if self._args.layout is not None:
                logger.info('Applying ' + str(self._args.layout) +
                            ' layout to network')
                self._layout.apply_layout(layout=self._args.layout,
                                          input_cx_file=cxout,
                                          output_cx_file=cxout,
                                          center=self._args.center,
                                          scale=self._args.scale)
            if self._args.outputcx is not None:
                logger.info('Writing CX to file: ' + self._args.outputcx)
                shutil.copyfile(cxout, self._args.outputcx)

            if self._args.skipupload is True:
                logger.info('--skipupload is set. Skipping upload to NDEx')
                return 0

            # update or upload network stored in `cxout` file to NDEx
            # server
            return self._upload_network(client, cxout)
        finally:
            shutil.rmtree(self._tmpdir)

        return 1

    @staticmethod
    def add_subparser(subparsers):
        """
        adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command loads an edge list file in tab separated
        format (hence TSV) and using a load plan, loads that data as
        a network into NDEx.

        This tool attempts to mimic behavior of the older
        tsv_uploader.py script located
        here: https://github.com/ndexbio/load-content

        This new version uses the more memory efficient
        streamtsvloader.

        This command requires five positional parameters.

        The first three (username, password, and server) are
        credentials for
        NDEx server to upload the network.

        Any of these first three credential fields set to '-' will
        force this tool to obtain the information from {cfig} file
        under the profile specified by the --profile field in this format:

        [<value of --profile>]
        {user} = <NDEx username>
        {password} = <NDEx password>
        {server} = <NDEx server ie public.ndexbio.org>

        The forth positional parameter (tsv_file) should be
        set to edge list file in tab separated format and the
        fifth or last positional parameter (load_plan) should be
        set to the load plan. The load plan is a JSON formatted text
        file that maps the columns to nodes, edges, and attributes
        in the network.

        By default this tool does not generate much output to
        standard out/error. For more verbosity add one or more -v parameters
        to left of command name tsvloader as seen in examples below.


        Example usage:

        ndexmisctools.py -vvvv tsvloader - - - datafile.tsv load.plan

        ndexmisctools.py -vv tsvloader bob xx public.ndexbio.org \\
                         datafile.tsv loadplan.json --uppercaseheader  \\
                         -t dafe07ca-0676-11ea-93e0-525400c25d22 \\
                         --name mynetwork --description 'some text'

        ndexmisctools.py -v --profile foo tsvloader - - public.ndexbio.org \\
                         datafile.tsv loadplan.json \\
                         --header 'col1\tcol2\tcol3' \\
                         -t some_cx_file.cx \\
                         -u 48a26aa0-0677-11ea-93e0-525400c25d22 \\
                         --layout -

        If successful 0 is returned otherwise there was an error.

        For more information visit:

        https://github.com/ndexbio/ndexutils


        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=TSVLoader.COMMAND,
                   cfig='~/' + NDExUtilConfig.CONFIG_FILE,
                   user=NDExUtilConfig.USER,
                   password=NDExUtilConfig.PASSWORD,
                   server=NDExUtilConfig.SERVER)

        parser = subparsers.add_parser(TSVLoader.COMMAND,
                                       help='Parses network in TSV format '
                                            'and loads into NDEx',
                                       description=desc,
                                       formatter_class=Formatter)
        parser.add_argument('username', help='NDEx username, if set to - '
                                             'then value from config will '
                                             'be used')
        parser.add_argument('password', help='NDEx password, if set to - '
                                             'then value from config will '
                                             'be used')
        parser.add_argument('server', help='NDEx server, if set to - then '
                                           'value from config will be used')
        parser.add_argument('tsv_file', help='Path to data file')
        parser.add_argument('load_plan', help='Path to load plan')
        parser.add_argument('-u',
                            help='If set, the UUID of network in NDEx '
                                 'to update. If not set,a new network '
                                 'will be added')
        parser.add_argument('-t', '--style', dest='t',
                            help='Style template network. '
                                 'This parameter can '
                                 'be a path to CX file OR '
                                 'NDEx UUID of a network '
                                 '(present on the same server)')
        parser.add_argument('--copyattribs', action='store_true',
                            help='If set, copies all network attributes '
                                 '(minus @context) '
                                 'from template network set via -t flag')
        parser.add_argument('--description',
                            help='Sets description for network (any double '
                                 'quotes will be removed) otherwise '
                                 'description (if any) '
                                 'will be taken from template network')
        parser.add_argument('--uppercaseheader', action='store_true',
                            help='If set, the first line in tsv_file '
                                 'is upper cased before being processed.'
                                 'This has no effect if --header is set.')
        parser.add_argument('--header', dest='header',
                            help='Header to prepend to the tsv_file. '
                                 'WARNING: Does NOT replace an existing '
                                 'header')
        parser.add_argument('--name',
                            help='Sets name for network (any double quotes '
                                 'will be removed) otherwise '
                                 'name (if any) '
                                 'will be taken from template network')
        parser.add_argument('--tmpdir',
                            help='Sets temp directory used for processing. If '
                                 'not set, then directory used is the '
                                 'default for Python\'s '
                                 'tempfile.mkdtemp() function')
        parser.add_argument('--skipupload', action='store_true',
                            help='If set, network will NOT be uploaded '
                                 'to NDEx')
        parser.add_argument('--layout',
                            help='If set, specifies layout '
                                 'algorithm to run. If Cytoscape is running '
                                 'and py4cytoscape is loaded any layout from '
                                 'Cytoscape can be used. If "-" is passed in '
                                 'force-directed-cl from Cytoscape will '
                                 'be used. If no Cytoscape is available, '
                                 '"spring" from networkx can be used. ')
        parser.add_argument('--scale', type=float, default=300.0,
                            help='Scale to pass to layout algorithm. Only '
                                 'applies if --layout flag is set')
        parser.add_argument('--center', type=str,
                            help='Comma delimited coordinate denoting '
                                 'center for layout. Should be in format '
                                 'of X,Y or Y,X not sure which way networkx '
                                 'does coordinates. Only apples if --layout '
                                 'flag is set')
        parser.add_argument('--' + ndexutil.networkx.SPRING_LAYOUT +
                            '_iterations', type=int,
                            default=50,
                            help='Maximum number of iterations taken. '
                                 'Only apples if --layout flag is '
                                 'set to ' + ndexutil.networkx.SPRING_LAYOUT)
        parser.add_argument('--' + ndexutil.networkx.SPRING_LAYOUT +
                            '_k', type=float,
                            help='Optimal distance between nodes. '
                                 'If unset the distance is set to 1/sqrt(n) '
                                 'where n is the number of nodes. Increase '
                                 'this value to move nodes farther apart. '
                                 'Only apples if --layout flag is '
                                 'set to ' + ndexutil.networkx.SPRING_LAYOUT)
        parser.add_argument('--outputcx',
                            help='If set, CX will be written to this file')
        return parser


class NetworkDeleter(object):
    """
    Deletes network or network set in NDEx
    """
    COMMAND = 'deletenetwork'

    def __init__(self, theargs):
        """
        Constructor
        :param theargs: command line arguments ie theargs.uuid
        """
        self._args = theargs
        self._user = None
        self._pass = None
        self._server = None
        self._client = None

    def _parse_config(self):
        """
        Parses config extracting the following fields:
        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`
        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _get_client(self):
        """
        Gets Ndex2 client
        :return: Ndex2 python client
        :rtype: :py:class:`~ndex2.client.Ndex2`
        """
        return Ndex2(self._server, self._user, self._pass)

    def _delete_network(self, uuid):
        return self._client.delete_network(uuid)

    def _delete_networkset(self, uuid):
        info = self._client.get_networkset(uuid)
        errors = {}
        for network in info['networks']:
            return_string = self._client.delete_network(network)
            if return_string != '':
                errors[network] = return_string
        return errors

    def run(self):
        """
        Connects to NDEx server, deletes network(s) specified by --uuid
        or by --networkset
        """
        logger.warning('THIS IS AN UNTESTED ALPHA IMPLEMENTATION '
                       'AND MAY CONTAIN ERRORS')

        self._parse_config()
        self._client = self._get_client()

        # Delete networks
        network_return_string = ''
        errors = {}
        if self._args.uuid:
            network_return_string = self._delete_network(self._args.uuid)
        if self._args.networkset:
            errors = self._delete_networkset(self._args.networkset)

        # Handle errors
        if network_return_string != '':
            errors[self._args.uuid] = network_return_string

        if len(errors) > 0:
            error_string = ''
            for uuid, error in errors.values():
                error_string = error_string + 'Received error status when ' +\
                               'deleting network ' + uuid + ': ' + error + '\n'
            raise NDExUtilError(error_string)
        
        return 0

    @staticmethod
    def add_subparser(subparsers):
        """
        Adds a subparser
        :param subparsers:
        :return:
        """
        desc = """

        Version {version}

        The {cmd} command deletes the network specified by --uuid or every 
        network in the network set specified by --networkset. 
        
        NOTE: --uuid and --networkset can both be set in a single call
        
        Return 0 upon success otherwise failure. 

        WARNING: THIS IS AN UNTESTED ALPHA IMPLEMENTATION AND MAY CONTAIN
                 ERRORS. YOU HAVE BEEN WARNED.

        """.format(version=ndexutil.__version__,
                   cmd=NetworkDeleter.COMMAND)

        parser = subparsers.add_parser(NetworkDeleter.COMMAND,
                                       help='Deletes networks and networksets from NDEx',
                                       description=desc,
                                       formatter_class=Formatter)
        parser.add_argument('--uuid',
                            default=None,
                            help='The UUID of the network in NDEx to delete')
        parser.add_argument('--networkset',
                            default=None,
                            help='The UUID of the network set in NDEx to '
                            'delete. Note that this will delete all the '
                            'networks in the network set but not the network '
                            'set itself')
        return parser


def _parse_arguments(desc, args):
    """Parses command line arguments using argparse.
    """

    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=Formatter)

    subparsers = parser.add_subparsers(dest='command',
                                       help='Command to run. '
                                            'Type <command> -h for '
                                            'more help')
    subparsers.required = True

    NetworkAttributeSetter.add_subparser(subparsers)
    CopyNetwork.add_subparser(subparsers)
    UpdateNetworkSystemProperties.add_subparser(subparsers)
    TSVLoader.add_subparser(subparsers)
    NetworkDeleter.add_subparser(subparsers)
    StyleUpdator.add_subparser(subparsers)
    NodeAttributeAdder.add_subparser(subparsers)
    NodeAttributeRemover.add_subparser(subparsers)
    FeaturedNetworkReportCommand.add_subparser(subparsers)
    CytoscapeLayoutCommand.add_subparser(subparsers)
    NetworkxLayoutCommand.add_subparser(subparsers)

    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module and '
                             '. Messages are '
                             'output at these python logging levels '
                             '-v = ERROR, -vv = WARNING, -vvv = INFO, '
                             '-vvvv = DEBUG, -vvvvv = NOTSET (default is to '
                             'log CRITICAL)')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'format consumable by fileConfig. See '
                             'https://docs.python.org/3/library/logging.html '
                             'for more information. '
                             'Setting this overrides -v|--verbose parameter '
                             'which uses default logger. (default None)')
    parser.add_argument('--conf', help='Configuration file to load '
                                       '(default ~/' +
                                       NDExUtilConfig.CONFIG_FILE)
    parser.add_argument('--profile', help='Profile in configuration '
                                          'file to use to load '
                                          'NDEx credentials which means'
                                          'configuration under [XXX] will be'
                                          'used '
                                          '(default '
                                          'ndexmisctools)',
                        default='ndexmisctools')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' + ndexutil.__version__))

    return parser.parse_args(args)


def _setup_logging(args):
    """
    Sets up logging based on parsed command line arguments.
    If args.logconf is set use that configuration otherwise look
    at args.verbose and set logging for this module and the one
    in ndexutil specified by TSV2NICECXMODULE constant
    :param args: parsed command line arguments from argparse
    :raises AttributeError: If args is None or args.logconf is None
    :return: None
    """

    if args.logconf is None:
        level = (50 - (10 * args.verbose))
        logging.basicConfig(format=LOG_FORMAT,
                            level=level)
        logger.setLevel(level)
        return

    # logconf was set use that file
    logging.config.fileConfig(args.logconf,
                              disable_existing_loggers=False)


def main(arglist):
    desc = """
              Version {version}
              """.format(version=ndexutil.__version__)

    theargs = _parse_arguments(desc, arglist[1:])
    theargs.program = arglist[0]
    theargs.version = ndexutil.__version__
    _setup_logging(theargs)
    try:
        logger.debug('Command is: ' + str(theargs.command))
        if theargs.command == NetworkAttributeSetter.COMMAND:
            cmd = NetworkAttributeSetter(theargs)
        if theargs.command == CopyNetwork.COMMAND:
            cmd = CopyNetwork(theargs)
        if theargs.command == UpdateNetworkSystemProperties.COMMAND:
            cmd = UpdateNetworkSystemProperties(theargs)
        if theargs.command == TSVLoader.COMMAND:
            cmd = TSVLoader(theargs)
        if theargs.command == NetworkDeleter.COMMAND:
            cmd = NetworkDeleter(theargs)
        if theargs.command == StyleUpdator.COMMAND:
            cmd = StyleUpdator(theargs)
        if theargs.command == NodeAttributeAdder.COMMAND:
            cmd = NodeAttributeAdder(theargs)
        if theargs.command == NodeAttributeRemover.COMMAND:
            cmd = NodeAttributeRemover(theargs)
        if theargs.command == FeaturedNetworkReportCommand.COMMAND:
            cmd = FeaturedNetworkReportCommand(theargs)
        if theargs.command == CytoscapeLayoutCommand.COMMAND:
            cmd = CytoscapeLayoutCommand(theargs)
        if theargs.command == NetworkxLayoutCommand.COMMAND:
            cmd = NetworkxLayoutCommand(theargs)

        if cmd is None:
            raise NDExUtilError('Invalid command: ' + str(theargs.command))

        return cmd.run()
    finally:
        logging.shutdown()
    return 100


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
