import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker


class DBEngine(object):
    def __init__(self):
        engine = create_engine('sqlite:///votes.db', echo=True)

        metadata = MetaData()
        votes_table = Table('votes', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('devil', Integer),
                            Column('notdevil', Integer))
        ips_table = Table('ips', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('ip', String),
                          Column('date', String))

        metadata.create_all(engine)
        mapper(Votes, votes_table)        
        mapper(Ip, ips_table)
        self.session = sessionmaker(bind=engine)()

        db_votes = self.session.query(Votes).filter_by(id=1).first()
        print('db_votes', db_votes)
        if not db_votes:
            self.session.add(Votes(1,0,0))
            self.session.commit()


    def get_stat(self):
        for row in self.session.query(Votes).all():
            return (row.devil, row.notdevil)

    def get_ips(self):
        return self.session.query(Ip).all()

    def save(self, votes):
        db_votes = self.session.query(Votes).filter_by(id=1).first()
        db_votes.devil = votes.devil
        db_votes.notdevil = votes.notdevil
        self.session.add(db_votes)
        self.session.commit()

    def check_ip(self, ip):
        if not self.session.query(Ip).filter_by(ip=ip.ip).first():
            self.session.add(ip)
            self.session.commit()
            return True #"New IP saved. Vote registered."
        return False #"Ip already used. Vote forbidden."


class Votes(object):
    def __init__(self, id, devil, notdevil):
        self.id = id
        self.devil = devil
        self.notdevil = notdevil

    def __repr__(self):
        return "<Votes('%s','%s', '%s')>" % (self.id, self.devil, self.notdevil)

class Ip(object):
   def __init__(self, ip, date):
        self.ip = ip
        self.date = date

   def __repr__(self):
        return "<Ip('%s', '%s')>" % (self.ip, self.date)
