import logging
from pprint import pprint, pformat
import time
from copy import deepcopy
#from collections import defaultdict

from pymongo import UpdateOne, InsertOne
from pymongo.errors import BulkWriteError


def bulk_write(db, item_type, ops, stat=None, retries=3, log_first_failop=True):
    """
    Tries to apply `ops` Update operations to `item_type`
    collection with `bulk_write` method.
    Gives up if `retries` retries failed.

    Args:
        db - pymongo collection object
        item_type - name of collection
        ops - list of operations like UpdateOne
        stat - instance of `ioweb.stat:Stat`
        retries - number of retries
    """
    if stat:
        stat.inc('bulk-write-%s' % item_type)
    for retry in range(retries):
        try:
            res = db[item_type].bulk_write(ops, ordered=False)
        except BulkWriteError as ex:
            # TODO: repeat only failed operations!!!
            # TODO: repeat only in case of DUP (11000) errors
            if retry == (retries - 1):
                if log_first_failop:
                    logging.error(
                        'First failed operation:\n%s' % (
                            pformat(ex.details['writeErrors'][0])
                        )
                    )
                raise
            else:
                if stat:
                    stat.inc('bulk-write-%s-retry' % item_type)
        else:
            if stat:
                stat.inc(
                    'bulk-write-%s-upsert' % item_type,
                    res.bulk_api_result['nUpserted']
                )
                stat.inc(
                    'bulk-write-%s-change' % item_type,
                    res.bulk_api_result['nModified']
                )
            break
    return res


class BulkWriter(object):
    def __init__(self, db, item_type, bulk_size=100, stat=None, retries=3):
        self.db = db
        self.item_type = item_type
        self.stat = stat
        self.retries = retries
        self.bulk_size = bulk_size
        self.ops = []

    def _write_ops(self):
        res = bulk_write(self.db, self.item_type, self.ops, self.stat)
        self.ops = []
        return res

    def update_one(self, *args, **kwargs):
        self.ops.append(UpdateOne(*args, **kwargs))
        if len(self.ops) >= self.bulk_size:
            return self._write_ops()
        else:
            return None

    def insert_one(self, *args, **kwargs):
        self.ops.append(InsertOne(*args, **kwargs))
        if len(self.ops) >= self.bulk_size:
            return self._write_ops()
        else:
            return None

    def flush(self):
        if len(self.ops):
            return self._write_ops()
        else:
            return None


def iterate_collection(
        db, item_type, query, sort_field, iter_chunk=1000,
        fields=None, infinite=False, limit=None
    ):
    """
    Iterate over `db[item_type]` collection items matching `query`
    sorted by `sort_field`.

    Intenally, it fetches chunk of `iter_chunk` items at once and
    iterates over it. Then fetch next chunk.
    """
    recent_id = None
    count = 0
    query = deepcopy(query) # avoid side effects
    if sort_field in query:
        logging.error(
            'Function `iterate_collection` received query'
            ' that contains a key same as `sort_field`.'
            ' That might goes unexpected and weird ways.'
        )
    while True:
        if recent_id:
            query[sort_field] = {'$gt': recent_id}
        else:
            if sort_field in query:
                del query[sort_field]
        items = list(db[item_type].find(
            query, fields, sort=[(sort_field, 1)], limit=iter_chunk
        ))
        if not items:
            if infinite:
                sleep_time = 5
                logging.debug(
                    'No items to process. Sleeping %d seconds'
                    % sleep_time
                )
                time.sleep(sleep_time)
                recent_id = None
            else:
                return
        else:
            for item in items:
                yield item
                recent_id = item[sort_field]
                count += 1
                if limit and count >= limit:
                    return


def bulk_dup_insert(db, item_type, ops, dup_key, stat=None):
    if stat:
        stat.inc('bulk-dup-insert-%s' % item_type, len(ops))
    all_keys = set()
    uniq_ops = []
    for op in ops:
        if not isinstance(op, InsertOne):
            raise Exception(
                'Function bulk_dup_insert accepts only'
                ' InsertOne operations. Got: %s'
                % op.__class__.__name__
            )
        if dup_key not in op._doc:
            raise Exception(
                'Operation for bulk_dup_insert'
                ' does not have key "%s": %s'
                % (dup_key, str(op._doc)[:1000])
            )
        key = op._doc[dup_key]
        if key not in all_keys:
            all_keys.add(key)
            uniq_ops.append(op)

    try:
        db[item_type].bulk_write(uniq_ops, ordered=False)
    except BulkWriteError as ex:
        if (
                all(x['code'] == 11000 for x in ex.details['writeErrors'])
                and
                not ex.details['writeConcernErrors']
            ):
            error_keys = set(
                x['op'][dup_key] for x in ex.details['writeErrors']
            )
            res_keys = list(all_keys - error_keys)
            if stat:
                stat.inc(
                    'bulk-dup-insert-%s-inserted' % item_type,
                    len(res_keys)
                )
            return res_keys
        else:
            raise
    else:
        if stat:
            stat.inc(
                'bulk-dup-insert-%s-inserted' % item_type,
                len(all_keys)
            )
        return list(all_keys)


def bulk_simple_insert(db, item_type, ops, stat=None):
    if stat:
        stat.inc('bulk-dup-insert-%s' % item_type, len(ops))
    for op in ops:
        if not isinstance(op, InsertOne):
            raise Exception(
                'Function simple_bulk_insert accepts only'
                ' InsertOne operations. Got: %s'
                % op.__class__.__name__
            )
    try:
        db[item_type].bulk_write(ops, ordered=False)
    except BulkWriteError as ex:
        if (
                all(x['code'] == 11000 for x in ex.details['writeErrors'])
                and
                not ex.details['writeConcernErrors']
            ):
            if stat:
                stat.inc(
                    'bulk-dup-insert-%s-inserted' % item_type,
                    len(ops) - len(ex.details['writeErrors'])
                )
        else:
            raise
    else:
        if stat:
            stat.inc(
                'bulk-dup-insert-%s-inserted' % item_type,
                len(ops)
            )
