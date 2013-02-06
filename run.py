import datetime
import logging

from job import AnalyticJob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import SourceAggregate, RevenueAggregate
from settings import *



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
    input_path = INPUT_PATH.format(date=datetime.date.today().strftime('%Y-%m-%d'))
    logger.info('Preparing Hadoop Job directed to path ' + input_path)

    job = AnalyticJob(args=['-r', 'hadoop', input_path])
    with job.make_runner() as runner:
        runner.run()
        logger.info('Saving...')

        for line in runner.stream_output():
            keys, values = job.parse_output_line(line)

            logger.debug(keys)
            logger.debug(values)

            if 'source' in keys:
                save(SourceAggregate, keys, values)
            else:
                save(RevenueAggregate, keys, values)

        session.commit()

    logger.info('Complete')



if __name__ == '__main__':
    engine = create_engine(MYSQL_DB)
    session = sessionmaker(bind=engine)()

    logger = logging.getLogger('mrjob.hadoop')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.info('Initialize')

    main()


