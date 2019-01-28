def escape(raw_string):
    return raw_string.encode('unicode_escape').decode('utf8')

def unescape(escaped_string):
    return escaped_string.encode('utf-8').decode('unicode_escape')

def quote(raw_string):
    return '\'' + escape(raw_string).replace('\'', '\\\'') + '\''

def unquote(quoted_string):
    if len(quoted_string) >= 2 and _quoted(quoted_string):
        return unescape(quoted_string[1:-1])
    else:
        raise ValueError(quoted_string)

def _quoted(value):
    return _single_quoted(value) or _double_quoted(value)

def _double_quoted(value):
    return value[0] == '"' and value[-1] == '"'

def _single_quoted(value):
    return value[0] == '\'' and value[-1] == '\''
