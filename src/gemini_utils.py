def extract_text(response):
    """Extract text content from a response object.

    The response may be a string, an object with a .content attribute,
    a list of items, or other types. Returns a string.
    """
    # If a wrapper object passed with .content, unwrap it
    content = getattr(response, "content", response)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if hasattr(item, "text"):
                parts.append(item.text)
            elif isinstance(item, dict):
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(parts)

    return str(content)