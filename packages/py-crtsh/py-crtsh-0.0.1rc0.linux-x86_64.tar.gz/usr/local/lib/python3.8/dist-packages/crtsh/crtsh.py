import requests
from scrapy.selector import Selector
import re


class Crtsh(object):
    """
    A class for querying crt.sh

    ...

    Methods
    -------
    identify(query: str) -> list
    Queries crt.sh with the required and supplied domain
    """
    def __init__(self):
        self.base_url = "https://crt.sh/"
        # self.site_certs will hold all the results from querying crt.sh
        self.site_certs = []
        # Compiling our regex to match for dates in the 'title' tag
        self.dates = re.compile('[0-9]{4}-[0-1][0-9]-[0-3][0-9]')

    def identify(self, query: str) -> list:
        """
        Queries crt.sh with the required and supplied domain
        :param query: The domain you wish to query, e.g. 'test.com'
        :return: List of dictionaries of each entry
        """
        # Here we're querying crt.sh's atom feed as opposed to the UI, to be nice to us and the server
        sites = requests.get(self.base_url + "atom?q={}".format(query))
        '''
        The layout and tags for the returned atom feed for each entry, 
        starting at the <entry> tags:
          <entry>
            <id>https://crt.sh/?id=558185#q;test.com</id>
            <link rel="alternate" type="text/html" 
            href="https://crt.sh/?id=558185"/>
            <summary type="html">secure.test.com
                                 www.secure.test.com ... 
                                 -----BEGIN CERTIFICATE----- ...
                                 -----END CERTIFICATE-----
            </summary>
            <title>[Certificate] Issued by Go Daddy Secure 
                                 Certification Authority; 
                                 Valid from 2012-12-14 to 2018-01-09;
                                 Serial number 2b4e7c52cf349b</title>
            <published>2012-12-14T15:40:21Z</published>
            <updated>2013-03-26T11:49:20Z</updated>
          </entry>
        '''
        sel_page = Selector(text=sites.content)
        rows = sel_page.xpath('//feed//entry')
        for row in rows:
            '''
            Here, the domains are pulled by selecting the 'summary' 
            tag, then splitting at the first '<' as the associated 
            domains precede that. Then in the returned list, we grab 
            the first entry which has the domains we want. Finally, we 
            split at newlines, as each domain is on a newline. The
            above XML example doesnt include all data returned in the
            summary tag, as it's cumbersome to include due to size
            '''

            domains = row.xpath('summary/text()').get().split('<')[0].split('\n')

            # Here we use the previously compiled regex to pull the cert's issue/expiration dates
            matches = self.dates.findall(row.xpath('title/text()').get())
            # Here we create a list of dictionaries. Each entry is inserted into the list at 0 as the feed returns
            # results in reverse order from the UI results
            self.site_certs.insert(0, {'crt.sh_id': row.xpath('id/text()').get().split('#')[0].split('=')[1],
                                       'Logged_At': row.xpath('published/text()').get(),
                                       'Not_Before': matches[0],
                                       'Not_After': matches[1],
                                       'Common_Name': domains[0],
                                       'Matching_Identities': domains,
                                       'Issuer_Name': row.xpath('title/text()').get().split(';')[0],
                                       'Updated': row.xpath('updated/text()').get()})
        return self.site_certs
