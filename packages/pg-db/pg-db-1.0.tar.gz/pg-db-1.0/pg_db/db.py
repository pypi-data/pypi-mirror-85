from psycopg2 import connect
from time import perf_counter
from typing import Union


class DB:
  conn = None
  cur = None
  dbname: str = ''
  dbuser: str = ''
  debug: bool = False
  start: float = 0

  def __init__(self, dbname: str, dbuser: str, debug: bool=False) -> None:
    self.dbname = dbname
    self.dbuser = dbuser
    self.debug = debug

  def connect(self, schema: str='public', readonly: bool=False) -> None:
    self.conn = connect(database=self.dbname,  user=self.dbuser, options='-c search_path=' + schema)
    if readonly:
      self.conn.commit()
      self.conn.set_session(readonly=True)
    self.cur = self.conn.cursor() 
    if self.debug:
      self.start = perf_counter()
      print('------------------db connected!------------------')

  def execute(self, sql: str, args: Union[dict, tuple, None]=None) -> None:
    if self.debug:
      start = perf_counter()
      print(self.cur.mogrify(sql, args))
    self.cur.execute(sql, args)
    if self.debug:
      print("Query elapsed time: {:0.4f} sec".format(perf_counter() - start))

  def description(self) -> tuple:
    return tuple(map(lambda c: c[0], self.cur.description))

  def one(self, sql: str, args: Union[dict, tuple, None]=None, as_dict: bool=False) -> Union[dict, tuple]:
    self.execute(sql, args)
    row = self.cur.fetchone()
    return dict(zip(self.description(), row)) if row and as_dict else row

  def all(self, sql: str, args: Union[dict, tuple, None]=None, as_dict: bool=False) -> list:
    self.execute(sql, args)
    rows = self.cur.fetchall()
    if rows and as_dict:
      cols = self.description()
      return [dict(zip(cols, row)) for row in rows]
    return rows

  def commit(self) -> None:
    self.conn.commit()

  def rollback(self) -> None:
    self.conn.rollback()

  def close(self) -> None:
    self.cur.close()
    self.conn.close()
    if self.debug:
      print("Total elapsed time: {:0.4f} sec".format(perf_counter() - self.start))
      print('-----------------db disconnected!-----------------')
