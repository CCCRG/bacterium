
import psycopg as pg
import json
from typing import Any, Sequence
from psycopg import Cursor
from cub.models import Vision

ratings_dictionary = {'s00': 10, 'c00': 20, 's01': 30}
new_obj = Vision()
new_obj.save(**ratings_dictionary)
# conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
# cur = conn.cursor()
# cur.execute("select s1,c1,s2,c2,s3,c3,s4,c4,s5,c5,s6,c6,s7,c7,s8,c8,s9,c9,s10,c10,s11,c11,s12,c12,s13,c13,s14,c14,s15,c15,s16,c16,s17,c17,s18,c18,s19,c19,s20,c20,s21,c21,s22,c22,s23,c23,s24,c24,s25,c25,s26,c26,s27,c27,s28,c28,s29,c29,s30,c30,s31,c31,s32,c32,s33,c33,s34,c34,s35,c35,s36,c36,s37,c37,s38,c38,s39,c39,s40,c40,s41,c41,s42,c42,s43,c43,s44,c44,s45,c45,s46,c46,s47,c47,s48,c48,s49,c49,s50,c50,s51,c51,s52,c52,s53,c53,s54,c54,s55,c55,s56,c56,s57,c57,s58,c58,s59,c59,s60,c60 from eyes where num = (SELECT MAX(num) FROM eyes)")
# conn.commit()
# data = cur.fetchall()
# cur.close()
# conn.close()

# class DictRowFactory:
#     def __init__(self, cursor: Cursor[Any]):
#         self.fields = [c.name for c in cursor.description]

#     def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
#         return dict(zip(self.fields, values))

# conn = pg.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
# # cur = conn.cursor(pymysql.cursors.DictCursor)
# cur = conn.cursor(row_factory=DictRowFactory)
# cur.execute("SELECT * FROM test where num = (SELECT MAX(num) FROM test)")
# data = cur.fetchall()
# cur.close()
# #conn.close()
# cur = conn.cursor()
# cur.execute("select s1,c1,s2,c2,s3,c3,s4,c4,s5,c5,s6,c6,s7,c7,s8,c8,s9,c9,s10,c10,s11,c11,s12,c12,s13,c13,s14,c14,s15,c15,s16,c16,s17,c17,s18,c18,s19,c19,s20,c20,s21,c21,s22,c22,s23,c23,s24,c24,s25,c25,s26,c26,s27,c27,s28,c28,s29,c29,s30,c30,s31,c31,s32,c32,s33,c33,s34,c34,s35,c35,s36,c36,s37,c37,s38,c38,s39,c39,s40,c40,s41,c41,s42,c42,s43,c43,s44,c44,s45,c45,s46,c46,s47,c47,s48,c48,s49,c49,s50,c50,s51,c51,s52,c52,s53,c53,s54,c54,s55,c55,s56,c56,s57,c57,s58,c58,s59,c59,s60,c60 from eyes where num = (SELECT MAX(num) FROM eyes)")
# conn.commit()
# data2 = cur.fetchall()
# cur.close()
# conn.close()
# data[0]['plot'] = data2
# print(json.dumps(data))
# json.dumps(data)