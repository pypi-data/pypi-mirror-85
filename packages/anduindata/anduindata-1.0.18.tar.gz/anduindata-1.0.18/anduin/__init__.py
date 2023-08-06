'''Anduin: A light python mysql connector.

Copyright (c) 2020-2024 Campanula<421248329@qq.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.'''

from .server import Data

def create(table, colums, show_sql=False):
    return Data.Base.create(table, colums, show_sql)

def insert(table, params, is_commit=True, show_sql=False):
    data = Data.Base.insert(table, params, is_commit, show_sql)
    return data

def find(table, conditions, or_cond=None, fields=('*',), order=None, show_sql=False):
    return Data.Base.find(table, conditions, or_cond, fields, order, show_sql)

def select(table, conditions, or_cond=None, fields=('*',), group=None, order=None, limit=None, show_sql=False):
    return Data.select(table, conditions, or_cond, fields, group, order, limit, show_sql)

def update(table, conditions, or_cond=None, params=None, is_commit=True, show_sql=False):
    Data.update(table, conditions, params, or_cond, is_commit, show_sql)
    return

def delete(table, conditions, or_cond=None, is_commit=True, show_sql=False):
    data = Data.delete(table, conditions, or_cond, is_commit, show_sql)
    return data

def find_last(table, conditions, info, limit, fields="*", show_sql=False):
    return Data.find_last(table, conditions, info, limit, fields, show_sql)


def query(sql, show_sql=False):
    return Data.query(sql, show_sql)
