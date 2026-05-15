#!/usr/bin/env python3
"""
Prepare the build/ directory for app/build.sh by generating the files that
prepare_build normally creates during a release pipeline:
  - translators.json  (translator index at build root)
  - deleted.txt       (moved from translators/ to build root)
"""
import json
import os
import re
import shutil
import sys
from collections import OrderedDict

def prepare(build_dir):
    translators_dir = os.path.join(build_dir, 'translators')

    # Move deleted.txt from translators/ to build root
    src = os.path.join(translators_dir, 'deleted.txt')
    dst = os.path.join(build_dir, 'deleted.txt')
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'Copied deleted.txt to build root')
    elif not os.path.exists(dst):
        print('Warning: deleted.txt not found in translators/', file=sys.stderr)

    # Build translator index
    index = OrderedDict()
    for fn in sorted((fn for fn in os.listdir(translators_dir)), key=str.lower):
        if not fn.endswith('.js'):
            continue
        with open(os.path.join(translators_dir, fn), 'r', encoding='utf-8') as f:
            contents = f.read()
        m = re.match(r'^\s*{[\S\s]*?}\s*?[\r\n]', contents)
        if not m:
            print(f'Warning: metadata block not found in {fn}', file=sys.stderr)
            continue
        metadata = json.loads(m.group(0))
        index[metadata['translatorID']] = {
            'fileName': fn,
            'label': metadata['label'],
            'lastUpdated': metadata['lastUpdated'],
        }

    out = os.path.join(build_dir, 'translators.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=True, ensure_ascii=False)
    print(f'Wrote translators.json ({len(index)} entries)')

if __name__ == '__main__':
    build_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', 'build')
    prepare(os.path.realpath(build_dir))
