#!/usr/bin/env python3

import argparse
import inspect
import json
import os

from jinja2 import Environment
from jinja2 import FileSystemLoader
from seoanalyzer import analyze

def main(args=None):
    if not args:
        module_path = os.path.dirname(inspect.getfile(analyze))

        arg_parser = argparse.ArgumentParser()

        arg_parser.add_argument('site', help='URL of the site you are wanting to analyze.')
        arg_parser.add_argument('-s', '--sitemap', help='URL of the sitemap to seed the crawler with.')
        arg_parser.add_argument('-f', '--output-format', help='Output format.', choices=['json', 'html'],
                                default='json')
        arg_parser.add_argument('-o', '--output-file', default=None, type=str, help="File to save results to instead of sending to stdout.")
        arg_parser.add_argument('-k', '--keyword-limit', type=int, default=4, help='Set count limit for keywords to include in the output.')
        arg_parser.add_argument('-b', '--bigram-limit', type=int, default=4, help='Set count limit for bigrams to include in the output.')
        arg_parser.add_argument('-t', '--trigram-limit', type=int, default=4, help='Set count limit for trigrams to include in the output.')

        arg_parser.add_argument('--analyze-headings', default=False, action='store_true', help='Analyze heading tags (h1-h6).')
        arg_parser.add_argument('--analyze-extra-tags', default=False, action='store_true', help='Analyze other extra additional tags.')
        arg_parser.add_argument('--follow-links', default=False, action='store_true', help='Analyze all the existing inner links as well (might be time consuming).')

        args = arg_parser.parse_args()

        output = analyze(args.site, args.sitemap,
                         analyze_headings=args.analyze_headings,
                         analyze_extra_tags=args.analyze_extra_tags,
                         follow_links=args.follow_links,
                         keyword_limit=args.keyword_limit,
                         bigram_limit=args.bigram_limit,
                         trigram_limit=args.trigram_limit)

        if args.output_format == 'html':
            env = Environment(loader=FileSystemLoader(os.path.join(module_path, 'templates')))
            template = env.get_template('index.html')
            output_from_parsed_template = template.render(result=output)
            print(output_from_parsed_template)
        elif args.output_format == 'json':
            if args.output_file:
                with open(args.output_file, 'w', encoding='utf-8') as file:
                    json.dump(output, file, ensure_ascii=False, indent=4)
            else:
                print(json.dumps(output, indent=4, separators=(',', ': ')))
    else:
        exit(1)

if __name__ == "__main__":
    main()
