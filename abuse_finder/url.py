from __future__ import unicode_literals

from dns.resolver import query, NoAnswer
from tldextract import extract
from urlparse import urlparse

from .ip import ip_abuse


def url_abuse(url):
    url = url if '://' in url else "http://" + url
    url = urlparse(url)

    parts = extract(url.netloc.split(':')[0])
    ip_addresses = set()

    if parts.registered_domain:
        answers = query(parts.registered_domain, 'A')
        for rdata in answers:
            ip_addresses.add(rdata.address)
    else:
        ip_addresses.add(parts.domain)

    results = {'value': [], 'names': [], 'abuse': []}
    for ip in ip_addresses:
        results['value'].append(ip)
        ip_results = ip_abuse(ip)
        for key in ['names', 'abuse']:
            for value in ip_results[key]:
                if value not in results[key]:
                    results[key].append(value)

    return results