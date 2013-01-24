import re
import datetime
from collections import defaultdict

from mrjob.job import MRJob
try:
    import simplejson as json
except ImportError:
    import json

EVENT_SEARCH = 0
EVENT_CLICK = 1
EVENT_IMPRESSION = 2

EVENTS = (
    (EVENT_SEARCH, 'searches'),
    (EVENT_CLICK, 'clicks'),
    (EVENT_IMPRESSION, 'impressions')
)

class LogProtocol(object):
    re_object_key = re.compile(':(\w+)=>')

    def parse_log(self, line):
        line = self.re_object_key.sub('"\\1":', line)
        line = line.replace('nil', 'null')

        return json.loads(line)

    def read(self, line):
        try:
            event_type, log = line.split('|')
        except ValueError:
            return None, None

        return int(event_type), self.parse_log(log)

    def write(self, key, value):
        raise NotImplemented


def flat_dict(list_of_dicts):
    """ Convert list of dicts into dict of lists """

    dct = defaultdict(list)
    for dct_element in list_of_dicts:
        for key, value in dct_element.items():
            dct[key].append(value)

    return dct

class AnalyticJob(MRJob):
    INPUT_PROTOCOL = LogProtocol

    def mapper(self, event_type, log):
        if event_type not in dict(EVENTS) or not isinstance(log, dict):
            return

        revenue_key = dict(
            cohort=log.get('cohort'),
            market=log.get('market'),
            dt=datetime.datetime.fromtimestamp(log.get('dt')).strftime('%Y-%m-%d'),
            feed=log.get('feed')
        )

        source_key = revenue_key.copy()
        source_key['source'] = log.get('source')

        event = dict(EVENTS)[event_type]

        yield revenue_key, dict(**{event: 1})
        yield source_key, dict(**{event: 1})


    def reducer(self, key, values):
        yield key, {key: sum(vals) for key, vals in flat_dict(values).items()}

    def steps(self):
        return [
            self.mr(
                mapper=self.mapper,
                combiner=self.reducer,
                reducer=self.reducer
            )
        ]

if __name__ == '__main__':
    AnalyticJob.run()