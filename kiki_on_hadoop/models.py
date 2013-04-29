from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey, Float

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


class DailyStatisticData(Base):
    """Base class for all entities crawled online.  """
    __tablename__ = 'daily_statistic_data'

    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, index=True, nullable=False)

    feed_ext_id = Column(Integer, index=True, nullable=False, default=0)
    channel_name = Column(String(100), index=True, nullable=False)  # cohort_name
    source = Column(String(100), index=True)
    geo = Column(String(100), index=True)       # market

    dau_ip = Column(Integer, default=0)         # (DAU-IP) Unique IPs by day
    dau_guid = Column(Integer, default=0)       # (DAU-GUID) Unique GUIDs by day

    our_biddedsearches = Column(Integer, default=0)   # Total Number of Searches based on our raw data by day
    our_nonbiddedsearches = Column(Integer, default=0)   # Total Number of Searches based on our raw data by day
    our_clicks = Column(Integer, default=0)     # Total Number of Clicks based on our raw data by day
    our_installations = Column(Integer, default=0)   # Total number of installs for day
    our_impressions = Column(Integer, default=0)   # Total number of impressions for day

    feed_searches = Column(Integer, default=0)  # Total Number of Searches based on Feed Reports by day
    feed_clicks = Column(Integer, default=0)    # Total Number of Clicks based on Feed Reports by day
    gross_revenue = Column(Float, default=0)    # Total Revenue from Feed Reports for day
