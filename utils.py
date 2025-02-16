"""TeXで安全な文字列に変換する"""
def escape_tex_string(s):
    if isinstance(s, (int, float)):
        s = str(s)
    s = s.replace("\\", "\\\\")
    s = s.replace("{", "\\{")
    s = s.replace("}", "\\}")
    s = s.replace("%", "\\%")
    s = s.replace("$", "\\$")
    s = s.replace("&", "\\&")
    s = s.replace("#", "\\#")
    s = s.replace("~", "\\~")
    s = s.replace("^", "\\^")
    s = s.replace("_", "\\_")
    return s



