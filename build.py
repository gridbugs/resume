#!/usr/bin/env python

import sys
import os
import argparse

import jinja2
import pdfkit
import markdown

def make_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'), nargs=1)
    parser.add_argument('-f', '--format', type=str, choices=['html', 'pdf'],
                        default='pdf')
    parser.add_argument('-o', '--output', type=str, required=True)

    return parser

def main(argv):

    parser = make_parser()
    args = parser.parse_args(argv)

    f = args.file[0]

    md = f.read()
    content_html = markdown.markdown(md)

    cwd = os.path.dirname(os.path.realpath(__file__))
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(cwd))
    rendered_html = template_env.get_template('template.html').render(content=content_html)

    if args.format == 'html':
        with open(args.output, 'w') as outfile:
            outfile.write(rendered_html)

        return 0

    if args.format == 'pdf':
        pdfkit.from_string(rendered_html, args.output)
        return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
