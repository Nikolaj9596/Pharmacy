from re import sub


def camel_case(line: str) -> str:
    line = sub(r"(_|-)+", " ", line).title().replace(" ", "")
    return ''.join([line[0].lower(), line[1:]])


def snake_case(line: str) -> str:
    """Transform camelCase string into snake_case"""
    def sub_function(match):
        return f"{match.group(1)}_{match.group(2).lower()}"
    return sub('([a-z])([A-Z]+)', sub_function, line)
