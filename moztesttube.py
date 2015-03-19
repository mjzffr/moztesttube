# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import datetime
import requests
from urlparse import parse_qs

import filters


class APISession:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def request_json(self, params):
        """ Returns the json-encoded response, if any """
        self.last_request = r = requests.get(self.url,
                                             headers=self.headers,
                                             params=params)
        data = r.json()
        if not r.ok:
            raise requests.HTTPError(r.status_code, data.get('error'),
                                     r.url)
        elif data.get('error'):
            raise RuntimeError(r.status_code, data.get('error'), r.url)
        return data


def format_none(column):
    """ Expects a list of strings. """
    return '\n'.join(column)


def format_ini(column):
    """
    Expects a dictionary whose values are lists of strings.
    Represents each key:list pair as:
        # key
        [item1]
        [item2]
        ...
    """
    lines = []
    for key in column:
        lines.append('# {0}'.format(key))
        lines.extend(['[{0}]'.format(i) for i in column[key]])
    return '\n'.join(lines)


def make_parser():
    default_query = ('build_id=>20140101000000&'
                     'product=Firefox&'
                     'url=$https://www.youtube.com/watch&'
                     'url=!~list&'
                     'url=!~index')
    description = ('Prints one column (default field: url) of a '
                   'crash-stats query result-set.')
    parser = argparse.ArgumentParser(prog='moztesttube.py',
                                     description=description)
    # required
    parser.add_argument('--token',
                        required=True,
                        help='API token for data source',
                        metavar='T')

    # optional
    parser.add_argument('--base_query',
                        default=default_query,
                        help=('URL query string to include '
                              'when calling data source; '
                              'default: %(default)s'),
                        metavar='Q')
    parser.add_argument('--max_results',
                        default=50,
                        type=int,
                        help=('maximum number of results to obtain; '
                              'default: %(default)s'),
                        metavar='N')
    parser.add_argument('--file',
                        default='',
                        const='test_data.ini',
                        nargs='?',
                        help=('save result in ini format; '
                              'default: ./%(const)s'))
    parser.add_argument('--source',
                        default='crash-stats',
                        # nargs='+',
                        # choices=['crash-stats', 'bugzilla'],
                        help=('data source; '
                              'default: %(default)s'))
    parser.add_argument('--target_field',
                        default='url',
                        help=('field to list in output; '
                              'default: %(default)s'),
                        metavar='F')

    return parser


def adjust_params(query_string, max_results):
    params = parse_qs(query_string)
    # specific to crash-stats
    params['_results_number'] = max_results
    if 'date' not in params:
        lastweek = datetime.date.today() - datetime.timedelta(days=7)
        params['date'] = '>' + lastweek.isoformat()
    return params


def main():
    args = make_parser().parse_args()
    headers = {'content-type': 'application/json',
               'accept': 'application/json',
               'Auth-Token': args.token}
    url = 'https://crash-stats.mozilla.com/api/SuperSearchUnredacted/'
    params = adjust_params(args.base_query, args.max_results)
    crash_stats = APISession(url, headers)
    data = crash_stats.request_json(params)
    print 'Request url: \t{0}\n'.format(crash_stats.last_request.url)
    sig_dict = filters.get_urls_by_top_crash(data, crash_stats,
                                             params, args.max_results)
    print format_ini(sig_dict)
    # TODO if target-field is != url, print err message
    # TODO if source is != just crash-stats, print err mesage
    # TODO if file-option is non-empty, write to ini file, If no file
    # specified, should print to stdout.


if __name__ == '__main__':
    main()
