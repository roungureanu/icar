import unittest
import unittest.mock

import icar.core.xml_parser


class TestCase(unittest.TestCase):
    def test_text_node_1(self):
        node = icar.core.xml_parser.TextNode('alabala')
        self.assertEqual(
            node.__repr__(),
            'alabala'
        )

    def test_text_node_2(self):
        node = icar.core.xml_parser.TextNode('alabala')
        self.assertEqual(
            node.__str__(),
            'alabala'
        )

    def test_text_node_dumps_1(self):
        node = icar.core.xml_parser.TextNode('alabala')
        self.assertEqual(
            node.dumps(level=0),
            'alabala'
        )

    def test_text_node_dumps_2(self):
        node = icar.core.xml_parser.TextNode('alabala')
        self.assertEqual(
            node.dumps(level=1),
            '    alabala'
        )

    def test_text_node_dumps_3(self):
        node = icar.core.xml_parser.TextNode('alabala')
        self.assertEqual(
            node.dumps(level=2),
            '        alabala'
        )

    def test_node_1(self):
        node = icar.core.xml_parser.Node(element='p', children=[])
        self.assertEqual(
            node.__repr__(),
            '<p></p>'
        )

    def test_node_2(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[icar.core.xml_parser.Node('a', []), icar.core.xml_parser.Node('b', [])]
        )
        self.assertEqual(
            node.__repr__(),
            '<p><a></a><b></b></p>'
        )

    def test_node_3(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[icar.core.xml_parser.TextNode('ala'), icar.core.xml_parser.TextNode('bala')]
        )
        self.assertEqual(
            node.__repr__(),
            '<p>alabala</p>'
        )

    def test_node_4(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[icar.core.xml_parser.TextNode('ala'), icar.core.xml_parser.TextNode('bala')]
        )
        self.assertEqual(
            node.__repr__(),
            '<p>alabala</p>'
        )

    def test_node_5(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[
                icar.core.xml_parser.Node(element='a', children=[icar.core.xml_parser.TextNode('abc')]),
                icar.core.xml_parser.TextNode('bala')
            ]
        )
        self.assertEqual(
            node.__repr__(),
            '<p><a>abc</a>bala</p>'
        )

    def test_node_6(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[icar.core.xml_parser.TextNode('ala'), icar.core.xml_parser.TextNode('bala')]
        )
        self.assertEqual(
            node.dumps(level=0),
            '<p>\n    ala\n    bala\n</p>'
        )

    def test_node_7(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[icar.core.xml_parser.TextNode('ala'), icar.core.xml_parser.TextNode('bala')]
        )
        self.assertEqual(
            node.dumps(level=1),
            '    <p>\n        ala\n        bala\n    </p>'
        )

    def test_node_8(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[icar.core.xml_parser.TextNode('ala'), icar.core.xml_parser.TextNode('bala')]
        )
        self.assertEqual(
            node.dumps(level=0),
            '<p>\n    ala\n    bala\n</p>'
        )

    def test_node_9(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[
                icar.core.xml_parser.Node(element='a', children=[icar.core.xml_parser.TextNode('abc')]),
                icar.core.xml_parser.TextNode('bala')
            ]
        )
        self.assertEqual(
            node.dumps(level=1),
            '    <p>\n        <a>\n            abc\n        </a>\n        bala\n    </p>'
        )

    def test_node_10(self):
        node = icar.core.xml_parser.Node(
            element='p',
            children=[
                icar.core.xml_parser.Node(element='p', children=[]),
                icar.core.xml_parser.Node(element='p', children=[])
            ]
        )
        self.assertEqual(
            node.__str__(),
            '<p><p></p><p></p></p>'
        )

    def test_parser_1(self):
        with self.assertRaises(Exception):
            icar.core.xml_parser.Parser('xml_parsers_tests\\invalid.xml')

    def test_parser_2(self):
        icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')

    def test_parser_3(self):
        parser = icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')
        self.assertEqual(parser.dumps(), '<p>\n    alabala\n</p>')

    def test_parser_4(self):
        parser = icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')
        result = parser._build_tree(body='<p>alabala</p>')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].element, 'p')
        self.assertEqual(len(result[0].children), 1)
        self.assertEqual(result[0].children[0].text, 'alabala')

    def test_parser_5(self):
        parser = icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')
        with self.assertRaises(Exception):
            result = parser._build_tree(body='<p>alabala')

    def test_parser_6(self):
        parser = icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')
        with self.assertRaises(Exception):
            result = parser._build_tree(body='<p>ana are mere<a>alabala<p>')

    def test_parser_7(self):
        parser = icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')
        with self.assertRaises(Exception):
            result = parser._build_tree(body='<p ana are mere')

    def test_parser_8(self):
        parser = icar.core.xml_parser.Parser('xml_parsers_tests\\valid.xml')
        with self.assertRaises(Exception):
            result = parser._build_tree(body='<p>ana are mere<asd</p>')


if __name__ == '__main__':
    unittest.main()
