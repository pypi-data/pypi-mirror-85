#!/usr/bin/env python
# coding: utf-8

from os import path
from textwrap import dedent
from operator import itemgetter
import re
import panflute as pf
from comment_parser import comment_parser


def is_include_line(elem):
    if len(elem.content) < 3:
        return False
    elif not all(isinstance(x, (pf.Str, pf.Space)) for x in elem.content):
        return False
    elif elem.content[0].text != '<<<':
        return False
    elif type(elem.content[1]) != pf.Space:
        return False
    else:
        return True


DEFAULT_PARAMS = {'filename': None, 'region': 'snippet'}


def get_args(elem):
    fn, region = itemgetter('filename', 'region')(DEFAULT_PARAMS)
    params = pf.stringify(elem, newlines=False).split(maxsplit=2)
    if params[1][0:2] == '@/':
        fn = './' + params[1][2:]
    else:
        raise ValueError(f'[code import] {params} should begin with @/')
    if len(params) > 2:
        region = params[2]
    return fn, region


SUPPORTED_SUBEXT = {
    'sh': ('session'),
    'conf': ('apache', 'nginx')
}


def get_code_type(extension, subextension):
    """convert a file extension to a prism.js language type alias

    see https://github.com/PrismJS/prism/issues/178

    Args:
        extension (str): The file extension (without dot)
        subtension (str): "sub" extension
            e.g. "session" in ".session.sh" for shell-session instead of bash

    Returns:
        str: prism.js language type alias (see https://github.com/PrismJS/prism/issues/178)
    """
    valid_subexts = SUPPORTED_SUBEXT.get(extension)
    if valid_subexts is None or subextension not in valid_subexts:
        subextension = ''

    return {
        # js, jsx, ts, tsx, html, md, py
        'sh': 'bash',
        'sessionsh': 'shell-session',
        'apacheconf': 'apacheconf',
        'nginxconf': 'nginx'
    }.get(subextension + extension, extension)


REGION_REGEXPS = (
    r'^\/\/ ?#?((?:end)?region) ([\w*-]+)$',  # javascript, typescript, java
    r'^\/\* ?#((?:end)?region) ([\w*-]+) ?\*\/$',  # css, less, scss
    r'^#pragma ((?:end)?region) ([\w*-]+)$',  # C, C++
    r'^<!-- #?((?:end)?region) ([\w*-]+) -->$',  # HTML, markdown
    r'^#((?:End )Region) ([\w*-]+)$',  # Visual Basic
    r'^::#((?:end)region) ([\w*-]+)$',  # Bat
    # Csharp, PHP, Powershell, Python, perl & misc
    r'^# ?((?:end)?region) ([\w*-]+)$'
)

def test_line(line, regexp, regionName, end=False):
    search = re.search(regexp, line.strip())
    if search is None:
        return
    (tag, name) = search.groups()
    tag_exist = tag is not None and len(tag) > 0
    name_exist = name is not None and len(name) > 0
    name_is_valid = name == regionName
    start_or_close = re.compile(
        r'^[Ee]nd ?[rR]egion$' if end else r'^[rR]egion$')
    tag_is_valid = start_or_close.match(tag) is not None
    return tag_exist and name_exist and name_is_valid and tag_is_valid


def find_region(lines, regionName):
    regexp = None
    start = -1

    for lineId, line in enumerate(lines):
        if regexp is None:
            for reg in REGION_REGEXPS:
                if test_line(line, reg, regionName):
                    start = lineId + 1
                    regexp = reg
                    break
        elif test_line(line, regexp, regionName, True):
            return {'start': start, 'end': lineId, 'regexp': regexp}

    return None


def extract_region(code, key, filepath):
    lines = code.splitlines()
    region_limits = find_region(lines, key)

    if region_limits is not None:
        regexp = re.compile(region_limits['regexp'])
        subset = lines[region_limits['start']:region_limits['end']]
        return '\n'.join(filter(lambda x: not regexp.match(x.strip()), subset))

    if key is not None and region_limits is None:
        raise ValueError(f'[code import] {filepath}#{key} not found')
    return code


def action(elem, doc):
    if isinstance(elem, pf.Para) and is_include_line(elem):
        raw_path = pf.stringify(elem, newlines=False).split(
            maxsplit=1)[1].strip()
        if raw_path[0:2] == '@/':
            raw_path = './' + raw_path[2:]
        else:
            raise ValueError(f'[code import] {raw_path} should begin with @/')

        rawPathRegexp = r'^(.+(?:\.([a-z]+)))(?:#([\w-]+))?(?: ?({\d+(?:[,-]\d+)?}))?$'
        search = re.search(rawPathRegexp, raw_path)

        if search is None:
            raise ValueError(f'[code import] invalid parameter {raw_path}')

        (filepath, extension, region_name, meta) = search.groups()

        if not path.isfile(filepath):
            raise ValueError(f'[code import] file not found: {filepath}')

        basename = path.basename(filepath).split('.')
        extension = basename[-1]
        subextension = ''
        if len(basename) > 2:
            subextension = basename[-2]

        with open(filepath) as f:
            raw = f.read()

        region = extract_region(raw, region_name, filepath)
        return pf.CodeBlock(dedent(region), '', [get_code_type(extension, subextension)])


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
