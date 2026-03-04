# src/parsers/tree_builder.py


from tree_sitter_languages import get_parser
def build_tree(code: str, language: str):
   
    parser = get_parser(language)
    tree = parser.parse(bytes(code, "utf-8"))
    return tree

