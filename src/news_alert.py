"""Simple script to alert me about interesting news stories.

Must provide environment variables to configure (see `get_vars`) function.
"""

import os
import re

import feedparser

from ox_task.core.comm_utils import send_email

def get_vars():
    "Get required variables from environment (or complain if missing)."
    my_vars = {}
    for name, reason, default in (
            ('FROM_EMAIL', 'Email account sending email.', ''),
            ('GMAIL_APP_PASSWD', 'App password for your sending account.', ''),
            ('TO_EMAIL', 'Email account to send to.', ''),
            ('FEEDS', 'Comma separated URLs for RSS feeds to scan.',
             'https://www.ft.com/rss/home'
             ',https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'),
            ('KEYWORDS', 'Comma separated keywords to search for.',
             'a.i.,nuclear')
            ):
        value = os.environ.get(name, default)
        if not value and not default:
            raise ValueError(f'Must provide env var {name} as {reason}.')
        my_vars[name] = value
    return my_vars


def main():
    """Main function to run to get weather and alert user if necessary.
    """
    timeout = 30
    my_vars = get_vars()
    results = {}
    keywords = [i.strip().lower() for i in my_vars['KEYWORDS'].split(',')]
    for feed in my_vars['FEEDS'].split(','):
        data = feedparser.parse(feed)
        for item in data['entries']:
            hits = {}
            title = item['title'].lower()
            summary = item['summary'].lower()
            for word in keywords:
                if word in title or word in summary:
                    hits[word] = True
            if hits:
                group = results.get(data['feed']['title'], [])
                if not group:
                    results[data['feed']['title']] = group
                group.append({'feed': feed, 'item': item, 'hits': set(hits)})
    if results:
        msg = ['<HTML><BODY>\n<P>News scan results:</P><BR>\n<UL>\n']
        for group, hits in results.items():
            group = re.sub(r'[^\s\w]', '', group)
            msg.append(f'<LI><strong>{group}</strong>\n  <UL>')
            for entry in hits:
                item = entry['item']
                msg.append(('    <LI> <A HREF="' + item['link'] + '">'
                            + item['title'] + '</A></LI>'))
            msg.append('</LI></UL>')
        msg.append('</UL></BODY></HTML>')
        msg = '\n'.join(msg)
                   
    print(f'Keyword hits:\n{results}')
    if results:
        send_email(msg, 'RSS alert', my_vars['TO_EMAIL'],
                   my_vars['FROM_EMAIL'], my_vars['GMAIL_APP_PASSWD'],
                   mode='html')

    return results


if __name__ == '__main__':
    main()
