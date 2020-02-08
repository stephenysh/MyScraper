import re

_re_multi_space = re.compile(r"\s+")
_re_bold = re.compile(r"\*\*([^\*]+)\*\*")
_re_ital = re.compile(r"\_([^\_]+)\_")
_re_ref = re.compile(r"\[\d+\]")
_re_img = re.compile(r"\*\[\!\[[^\[]+\]\([^\(]+\)\]\:")
_re_start_bracket = re.compile(r"\*\[[^\[]+\]\:")
_re_bracket = re.compile(r"\([^\(]+\)")

def regex_process(text):
    text = re.sub(_re_multi_space, " ", text)
    text = re.sub(_re_bold, lambda match: match.group(1), text)
    text = re.sub(_re_ital, lambda match: match.group(1), text)
    text = re.sub(_re_ref, "", text)
    text = re.sub(_re_img, "", text) # img should before start bracket
    text = re.sub(_re_start_bracket, "", text)
    text = re.sub(_re_bracket, "", text)
    return text