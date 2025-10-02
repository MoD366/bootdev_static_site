import re

def choose_heading_level(text):
    for i in range(7):
        if text[i] != "#":
            return f"h{i}"
    raise ValueError("This is not a proper heading.")

def extract_title(markdown):
    lines = markdown.split("\n")
    try:
        for line in lines:
            candidate = re.findall(r"^# .*", line)
            if len(candidate) > 0:
                h1 = candidate[0][2:].strip()
                return h1
    except Exception:
        raise Exception("There is no h1 header in the given Markdown")
    raise Exception("There is no h1 header in the given Markdown")