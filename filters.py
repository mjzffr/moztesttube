# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from time import sleep


def get_crash_urls(data):
    assert 'hits' in data
    return {hit['url'] for hit in data['hits']}


def get_urls_by_top_crash(data, api_session, params, total):
    assert 'facets' in data
    sig_stats = data['facets'].get('signature')[:10]
    top_signatures = [i['term'].strip() for i in sig_stats]
    if len(top_signatures) < 1:
        return {}
    # how many urls to get for each signature
    params['_results_number'] = (total / len(top_signatures)) or 1
    sig_dict = {}
    for sig_name in top_signatures:
        params['signature'] = ''.join(['=', sig_name])
        hits = api_session.request_json(params)['hits']
        sleep(1)
        urls = {hit['url'] for hit in hits}
        print 'Request url: \t{0}\n'.format(api_session.last_request.url)
        sig_dict[sig_name] = urls
    return sig_dict
