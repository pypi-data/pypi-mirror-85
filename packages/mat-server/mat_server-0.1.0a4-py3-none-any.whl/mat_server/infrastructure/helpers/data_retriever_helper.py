from typing import Any

import lark

from mat_server.domain import helpers, exceptions


class DataRetrieverHelper(helpers.DataRetrieverHelperBase):
    RETRIEVER_GRAMMAR = """
        generate_retrieve_func: "." 
                              | ("." get_value)+

        get_value: get_value_by_list_index
                 | get_value_by_dict_attr

        get_value_by_list_index: "[" INT "]"
        get_value_by_dict_attr: /[^.]+/

        %import common.INT -> INT
        %import common.WORD -> WORD
    """

    @lark.v_args(inline=True)
    class Transformer(lark.Transformer):

        @staticmethod
        def generate_retrieve_func(*nodes):
            def _retrieve_func(data):
                for node in nodes:
                    retrieve_func = node
                    data = retrieve_func(data)
                return data

            return _retrieve_func

        @staticmethod
        def get_value_by_dict_attr(node):
            dict_attr = str(node)

            def _retrieve_func(data):
                if not isinstance(data, dict):
                    return None
                return data.get(dict_attr)

            return _retrieve_func

        @staticmethod
        def get_value_by_list_index(node):
            list_index = int(node)

            def _retrieve_func(data):
                if not isinstance(data, list):
                    return None
                if len(data) - 1 < list_index:
                    return None

                return data[list_index]

            return _retrieve_func

        @staticmethod
        def get_value(node):
            _retrieve_func = node
            return _retrieve_func

    def __init__(self):
        self._grammar_parser = lark.Lark(self.RETRIEVER_GRAMMAR, start='generate_retrieve_func')

    def get_value(self, data: Any, path: str, default: Any = None) -> Any:
        try:
            parser = self._grammar_parser.parse(path)
        except lark.exceptions.LarkError as e:
            raise exceptions.ValidationError('path 文法錯誤') from e

        retrieve_func = self.Transformer().transform(parser)
        value = retrieve_func(data)
        return value if value is not None else default
