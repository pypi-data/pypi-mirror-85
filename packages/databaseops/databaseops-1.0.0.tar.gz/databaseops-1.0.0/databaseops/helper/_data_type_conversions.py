# coding=utf-8
import itertools


class ListConversion:
    """
    This class is developed for creating helper methods for different classes in
    projects. All this methods will focus on conversion for list data type to
    any other required data type.
    
    """
    
    @staticmethod
    def list_of_tuple_to_list(list_of_tuple: list) -> list:
        """
        This method list of tuples to list.
        :param list_of_tuple: list containing multiple tuples
        :return: list contain values from the tuples
        """
        return list(itertools.chain(*list_of_tuple))
