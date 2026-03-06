def parse_code(source, lang):
    parser = get_parser(lang)
    tree = parser.parse(bytes(source, "utf-8"))
    return tree
