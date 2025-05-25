import re

def extract_java_info(code):
    try:
        class_pattern = r'\bclass\s+(\w+)'
        method_pattern = r'\b(?:public|private|protected)?\s*(?:static\s+)?(?:[\w<>[\]]+\s+)+(\w+)\s*\([^)]*\)\s*\{?'
        comment_pattern = r'(?:/\*\*(.*?)\*/|//(.*))'

        classes = re.findall(class_pattern, code)
        methods = re.findall(method_pattern, code)
        raw_comments = re.findall(comment_pattern, code, re.DOTALL)

        comments = [c[0].strip() or c[1].strip() for c in raw_comments if c[0] or c[1]]

        return {
            "classes": classes,
            "methods": list(set(methods)),
            "comments": comments,
        }

    except Exception as e:
        return {"error": f"Parsing error: {e}"}

def summarize_java_structure(info):
    if "error" in info:
        return info["error"]

    summary = []
    if info["classes"]:
        summary.append(f"Classes: {', '.join(info['classes'])}")
    if info["methods"]:
        summary.append(f"Methods: {', '.join(info['methods'])}")
    if info["comments"]:
        summary.append("Comments:\n- " + "\n- ".join(info["comments"]))

    return "\n".join(summary) if summary else "No significant structure found."
