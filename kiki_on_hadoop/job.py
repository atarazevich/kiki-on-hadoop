#!/usr/bin/env python

from collections import defaultdict

from mrjob.job import MRJob
try:
    import simplejson as json
except ImportError:
    import json

#EVENT_SEARCH = 0
#EVENT_CLICK = 1
#EVENT_IMPRESSION = 2
#
#EVENTS = (
#    (EVENT_SEARCH, 'searches'),
#    (EVENT_CLICK, 'clicks'),
#    (EVENT_IMPRESSION, 'impressions')
#)

class LogProtocol(object):
    def read(self, line):
        dt, event, log = line.split()
        event = event.split('.')[-1]

        return (dt, event), json.loads(log)

    def write(self, key, value):
        raise NotImplemented


def flat_dict(list_of_dicts):
    """ Convert list of dicts into dict """
    dct = defaultdict(int)

    for dct_element in list_of_dicts:
        for key, val in dct_element.items():
            if isinstance(val, dict):
                dct[key] = flat_dict(val)
            if isinstance(val, (int, long)):
		dct[key] += val


    return dct

def datetime2date(dt):
    date, time = dt.split('T')
    return date



class AnalyticJob(MRJob):
    INPUT_PROTOCOL = LogProtocol

    def mapper(self, key, log):
        dt, event = key

        keys = dict(
            channel_name=log.get('cohort'),
            geo=log.get('market'),
            dt=datetime2date(dt),
            feed_ext_id=log.get('feed'),
            source=log.get('source')
        )

       	yield keys, dict(**{event: 1}, dau_ip={log.get('ip'): 1}, dau_guid={log.get('guid'):1})
	#yield 'ip', {log.get('ip'): 1}
	#yield 'guid', {log.get('guid'): 1} 


    def reducer(self, key, values):
        yield key, flat_dict(values)

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
