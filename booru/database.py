from flask_sqlalchemy import SQLAlchemy
from multiprocessing import cpu_count, Pool


db = SQLAlchemy()


def merge_all(db, instances):
    pool = Pool(cpu_count() - 1)
    pool.map(db.session.merge, instances)