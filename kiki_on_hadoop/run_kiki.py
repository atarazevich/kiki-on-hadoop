import datetime
import logging
import time
import os
import ConfigParser

from job import AnalyticJob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import SourceAggregate, RevenueAggregate


config = ConfigParser.ConfigParser()
config.read('/etc/kiki/kiki.cfg')

engine = create_engine(config.get('kiki', 'db'))
session = sessionmaker(bind=engine)()

logger = logging.getLogger('mrjob.hadoop')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.info('Initialize')


FIELD_MAPPER = (
    ('search', 'bidded_searches'),
    ('impression', 'bidded_results'),
    ('click', 'bidded_clicks'),
)


def save(Model, keys, values):
    filter_by = {key: val for key, val in keys.items() if key in Model.__table__.columns}
    item = session.query(Model).filter_by(**filter_by).first() or Model(**filter_by)

    mapper = dict(FIELD_MAPPER)
    for key, val in values.items():
        if key not in mapper:
            continue

        setattr(item, mapper[key], val)

    session.add(item)


def main():
    input_path = config.get('kiki', 'input_path').format(date=datetime.date.today().strftime('%Y%m%d'))
    output_path = os.path.join(config.get('kiki', 'output_path'), str(time.time()))
    result_path = os.path.join(output_path, 'part-*')

    logger.info('Preparing Hadoop Job directed to path ' + input_path)

    job = AnalyticJob(args=['-r', 'hadoop', '--no-output', '-o', output_path, input_path])
    with job.make_runner() as runner:
        runner.run()
        logger.info('Saving...')

        for filename in runner.ls(result_path):
            # Fix filename trouble with HADOOP 2.0
            filename = filename.replace('hdfs://hdfs://', 'hdfs://')

            for line in runner._cat_file(filename):

                keys, values = job.parse_output_line(line)

                logger.info(keys)
                logger.info(values)

                if 'source' in keys:
                    save(SourceAggregate, keys, values)
                else:
                    save(RevenueAggregate, keys, values)

        session.commit()

    logger.info('Complete')



if __name__ == '__main__':
    main()


