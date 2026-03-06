# src/parsers/function_extractor.py

"""
Finds all function definitions in source code.
"""

from src.parsers.tree_builder import build_tree


# Different languages use different node types for functions
FUNCTION_NODE_TYPES = {
    "python": ["function_definition"],
    "javascript": ["function_declaration", "arrow_function",
                   "method_definition"],
    "typescript": ["function_declaration", "arrow_function",
                   "method_definition"],
    "java": ["method_declaration"],
    "go": ["function_declaration", "method_declaration"],
    "rust": ["function_item"],
}


def extract_functions(code: str, language: str) -> list:
    """
    Find all functions in the code.

    Returns:
    [
        {
            "name": "greet",
            "parameters": ["name"],
            "start_line": 1,
            "end_line": 2,
            "body": "def greet(name):\n    print(...)"
        }
    ]
    """
    tree = build_tree(code, language)
    target_types = FUNCTION_NODE_TYPES.get(language, ["function_definition"])
    functions = []

   # Node types that contain classes — we skip functions inside these
    class_types = ["class_definition", "class_declaration"]

    def walk(node, inside_class=False):
        # If we're inside a class, skip — class_extractor handles those
        if node.type in class_types:
            inside_class = True

        if node.type in target_types and not inside_class:
            info = _extract_one_function(node, code)
            if info:
                functions.append(info)

        for child in node.children:
            walk(child, inside_class)
    walk(tree.root_node)
    return functions


def _extract_one_function(node, code: str) -> dict:
    """
    Given a single function node from the AST,
    extract its name, parameters, line numbers, and body.
    """
    name = None
    parameters = []

    for child in node.children:
        # Find the function name
        if child.type in ("name", "identifier"):
            name = code[child.start_byte:child.end_byte]

        # Find the parameters
        elif child.type in ("parameters", "formal_parameters"):
            for param in child.children:
                if param.type in ("identifier", "name",
                                  "typed_parameter", "parameter"):
                    param_text = code[param.start_byte:param.end_byte]
                    # Skip punctuation and self/this
                    if param_text not in ("(", ")", ",", "self", "this"):
                        parameters.append(param_text)

    if not name:
        return None

    return {
        "name": name,
        "parameters": parameters,
        "start_line": node.start_point[0] + 1,
        "end_line": node.end_point[0] + 1,
        "body": code[node.start_byte:node.end_byte],
    }

def sum (a,b):
    return a+b 
