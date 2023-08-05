# -*- coding: utf-8 -*-


class NetworkAnnotator(object):
    """
    Contains utility methods to annotate
    a :py:class:`ndex2.nice_cx_network.NiceCXNetwork`
    object
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    def add_as_node_attribute(self, cx_network, join_node_attribute_on_network,
                              data_frame, data_column_in_dataframe,
                              join_column_in_dataframe):
        """

        :param cx_network:
        :param join_node_attribute_on_network:
        :param data_frame:
        :param data_column_in_dataframe:
        :param join_column_in_dataframe:
        :return:
        """