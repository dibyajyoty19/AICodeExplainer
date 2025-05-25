import ast

def extract_python_info(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"SyntaxError: {e}"}

    functions = []
    classes = []
    docstrings = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            if ast.get_docstring(node):
                docstrings.append(ast.get_docstring(node))
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
            if ast.get_docstring(node):
                docstrings.append(ast.get_docstring(node))

    return {
        "functions": functions,
        "classes": classes,
        "docstrings": docstrings,
    }

# Optional helper for explanation
def summarize_python_structure(info):
    if "error" in info:
        return info["error"]

    summary = []
    if info["functions"]:
        summary.append(f"Functions: {', '.join(info['functions'])}")
    if info["classes"]:
        summary.append(f"Classes: {', '.join(info['classes'])}")
    if info["docstrings"]:
        summary.append(f"Docstrings:\n- " + "\n- ".join(info["docstrings"]))

    return "\n".join(summary) if summary else "No significant structure found."
