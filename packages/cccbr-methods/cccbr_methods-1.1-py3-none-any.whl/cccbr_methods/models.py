from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from re import sub
import os

module_path = '/'.join(__file__.split('/')[:-1])

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine('sqlite:///{}/data/methods.db?check_same_thread=False'.format(module_path))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Method(Base):
    __tablename__ = 'methods'
    id = Column(Integer, primary_key=True)               # method['id'] (formatted)

    stage = Column(Integer)                              # mset.properties.stage
    classification = Column(String(32))                  # mset.properties.classification.string
    plain = Column(Boolean, default=False)               # mset.properties.classification['plain']
    trebledodging = Column(Boolean, default=False)       # mset.properties.classification['trebledodging']
    little = Column(Boolean, default=False)              # mset.properties.classification['little']
    differential = Column(Boolean, default=False)        # mset.properties.classification['differential']
    lengthoflead = Column(Integer)                       # mset.properties.lengthoflead
    numberofhunts = Column(Integer)                      # mset.properties.numberofhunts
    huntbellpath = Column(String(32))                    # mset.properties.huntbellpath
    methodset_notes = Column(String(128))                # mset.properties.notes

    title = Column(String(128), index=True, unique=True) # method.title
    name = Column(String(128), index=True)               # method.name
    leadhead = Column(String(32))                        # method.leadhead
    leadheadcode = Column(String(32))                    # method.leadheadcode
    symmetry = Column(String(32))                        # method.symmetry
    notation = Column(String(128))                       # method.notation
    falseness = Column(String(32))                       # method.falseness.fchgroups
    extensionconstruction = Column(String(32))           # method.extensionconstruction
    notes = Column(String(128))                          # method.notes


    pmmref = Column(String(32))                          # method.references.pmmref
    bnref = Column(String(32))                           # method.references.bnref
    cbref = Column(String(32))                           # method.references.cbref
    rwref = Column(String(32))                           # method.references.rwref
    tdmmref = Column(String(32))                         # method.references.tdmmref


    performances = relationship("Performance", back_populates="method")

    @staticmethod
    def get(search_string='', *args, **kwargs):
        """
        Search for a method in the database and return the first result.
        """
        # If there's an exact match for the search_string, we want to return that
        # but we still want to respect the other search terms
        exact = session.query(Method).filter_by(title=search_string, **kwargs).first()
        if exact:
            return exact
        query = session.query(Method).filter(Method.title.like('%' + search_string + '%'))
        return query.filter_by(**kwargs).first()

    @staticmethod
    def search(search_string='', *args, **kwargs):
        """
        Search for a method in the database and return all results.
        """
        query = session.query(Method).filter(Method.title.like('%' + search_string + '%'))
        return query.filter_by(**kwargs).all()

    @staticmethod
    def query():
        return session.query(Method)

    @property
    def full_notation(self):
        if not ',' in self.notation: return self.notation



        segments = [seg.split('.') for seg in sub('-','.-.',self.notation).strip('.').split(',')]

        full_notation = ['.'.join(seg + seg[:-1][::-1]) if len(seg) > 1 else seg[0] for seg in segments]

        return '.'.join(full_notation)

    @property
    def full_notation_list(self):
        return self.full_notation.split('.')

    def __repr__(self):
        return '<Method {}>'.format(self.title)

    def __iter__(self):
        for key, val in self.__dict__.items():
            if key == '_sa_instance_state': continue
            yield (key, val)


class Performance(Base):
    __tablename__ = 'performances'
    id = Column(Integer, primary_key=True, autoincrement=True) # id
    kind = Column(String(32))                                  # method.performances.KIND
    date = Column(Date)                                        # PERF.date
    society = Column(String(32))                               # PERF.society
    town = Column(String(32))                                  # PERF.location.town
    county = Column(String(32))                                # PERF.location.county
    building = Column(String(32))                              # PERF.location.building
    address = Column(String(32))                               # PERF.location.address
    country = Column(String(32))                               # PERF.location.country
    room = Column(String(32))                                  # PERF.location.room
    region = Column(String(32))                                # PERF.location.region
    method_id_fk = Column(Integer, ForeignKey('methods.id'))
    method = relationship("Method", back_populates="performances")

    def __repr__(self):
        return '<Performance {}: {}>'.format(self.kind, self.method.title)

    def __iter__(self):
        for key, val in self.__dict__.items():
            if key == '_sa_instance_state': continue
            if key == 'method': continue
            yield (key, val)

