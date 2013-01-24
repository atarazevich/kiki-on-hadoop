from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey

Base = declarative_base()

class SourceAggregate(Base):
    __tablename__ = 'source_aggregates'

    id = Column(Integer, primary_key=True)

    cohort = Column(String(50), default=None, index=True)
    market = Column(String(50), default=None, index=True)
    source = Column(String(50), default=None, index=True)
    feed = Column(Integer, default=None, index=True)

    dt = Column(DateTime, default=None, index=True)

    searches = Column(Integer, default=0, nullable=False)

    bidded_searches = Column(Integer, default=0, nullable=False)
    bidded_results = Column(Integer, default=0, nullable=False)
    bidded_clicks = Column(Integer, default=0, nullable=False)

    source_searches = Column(Integer, default=0)
    source_bidded_searches = Column(Integer, default=0)
    source_bidded_results = Column(Integer, default=0)
    source_bidded_clicks = Column(Integer, default=0)

    estimated_gross_revenue = Column(Integer, default=0)
    source_coverage = Column(Integer, default=0)
    source_ctr = Column(Integer, default=0)
    source_ppc = Column(Integer, default=0)

    suggested_revenue_allocation = Column(Integer, default=0)
    traffic_quality = Column(Integer, default=None)
    channel_revenue = Column(Integer, default=0)

    approved = Column(SmallInteger, default=0, nullable=False)

    #revenue_aggregate_id = Column(Integer, ForeignKey('revenue_aggregates.id'))

class RevenueAggregate(Base):
    __tablename__ = 'revenue_aggregates'

    id = Column(Integer, primary_key=True)

    cohort = Column(String(50), default=None, index=True)
    market = Column(String(50), default=None, index=True)
    feed = Column(Integer, default=None, index=True)

    dt = Column(DateTime, default=None, index=True)

    searches = Column(Integer, default=0, nullable=False)

    bidded_searches = Column(Integer, default=0, nullable=False)
    bidded_results = Column(Integer, default=0, nullable=False)
    bidded_clicks = Column(Integer, default=0, nullable=False)

    source_searches = Column(Integer, default=0)
    source_bidded_searches = Column(Integer, default=0)
    source_bidded_results = Column(Integer, default=0)
    source_bidded_clicks = Column(Integer, default=0)

    estimated_gross_revenue = Column(Integer, default=0)
    source_coverage = Column(Integer, default=0)
    source_ctr = Column(Integer, default=0)
    source_ppc = Column(Integer, default=0)

    suggested_revenue_allocation = Column(Integer, default=0)
    average_traffic_quality = Column(Integer, default=None)
    channel_revenue = Column(Integer, default=0)

    approved = Column(SmallInteger, default=0, nullable=False)

    daily_actives = Column(Integer, default=0, nullable=False)
    daily_installs = Column(Integer, default=0, nullable=False)
