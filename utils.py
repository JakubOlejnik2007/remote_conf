import re
from typing import List

from readJson import jsonInputControl


def replace_based_on_content(text, controls: List[jsonInputControl]):
    def replacer(match):
        content = match.group(1)
        for idx, control in enumerate(controls):
            if control.id == content:
                return control.control.value
        return ""
    pattern = r'\{(.*?)\}'

    result = re.sub(pattern, replacer, text)

    return result