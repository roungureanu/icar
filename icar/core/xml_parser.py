import os
import icar.helpers.constants as constants


class Node(object):
    def __init__(self, element, children):
        assert isinstance(element, str)
        assert isinstance(children, list)

        self.element = element
        self.children = children

    def __repr__(self):
        return '<{element}>{body}</{element}>'.format(
            element=self.element,
            body=''.join(map(str, self.children))
        )

    def dumps(self, level=0):
        return '{indent}<{element}>\n{body}\n{indent}</{element}>'.format(
            element=self.element,
            body='\n'.join(child.dumps(level + 1) for child in self.children),
            indent=' ' * level * 4
        )


class TextNode(object):
    def __init__(self, text):
        assert isinstance(text, str)
        self.text = text.strip()

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text

    def dumps(self, level=0):
        return ' ' * level * 4 + self.text


class Parser(object):
    def __init__(self, file_path):
        assert os.path.exists(file_path)

        with open(file_path, 'r') as handle:
            self.content = handle.read()

        assert self.content.startswith('<')
        assert self.content.endswith('>')
        if not self.content or self.content[0] != '<':
            raise Exception('Invalid XML. It must start with a valid XML element.')

        self.tree = self._build_tree(self.content)[0]

    def _build_tree(self, body):
        assert isinstance(body, str)

        i = 0
        children = []
        child = ''
        while i < len(body):
            character = body[i]

            if character == '<':
                if child.strip():
                    children.append(
                        TextNode(child)
                    )
                    child = ''

                element_start = i + 1
                end = body.find('>', i)

                if end == -1:
                    raise Exception('Enclosing bracket not found.')
                element_end = end

                element = body[element_start:element_end]

                end_tag = '</{}>'.format(element)
                enclosing_tag = body.find(end_tag, end + 1)
                if enclosing_tag == -1:
                    raise Exception('Enclosing tag not found')

                element_body = body[element_end + 1:enclosing_tag]
                i = enclosing_tag + len(end_tag)

                children.append(
                    Node(
                        element=element,
                        children=self._build_tree(element_body)
                    )
                )
            else:
                child = child + character
                i = i + 1

        if child.strip():
            children.append(
                TextNode(child)
            )

        return children

    def dumps(self):
        return self.tree.dumps()


if __name__ == '__main__':
    path = os.path.join(constants.RESOURCES_FOLDER_PATH, 'export.xml')
    parser = Parser(path)
    print(parser.tree.children)
    print(parser.dumps())
