def extract_text_from_response(response):
    """
    Extract plain text from LangChain/Gemini responses.

    Works with:
    - AIMessage.content as string
    - AIMessage.content as list of blocks
    - Future LangChain response formats
    """

    if response is None:
        return ""

    content = getattr(response, "content", response)

    # Plain string
    if isinstance(content, str):
        return content.strip()

    # List of content blocks
    if isinstance(content, list):
        text_parts = []

        for item in content:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

            elif hasattr(item, "text"):
                text_parts.append(item.text)

            else:
                text_parts.append(str(item))

        return "\n".join(text_parts).strip()

    return str(content)