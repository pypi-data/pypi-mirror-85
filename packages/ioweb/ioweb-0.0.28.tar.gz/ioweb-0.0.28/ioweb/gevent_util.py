def assert_gevent_enabled():
    from gevent.monkey import saved
    if not len(saved):
        raise Exception('Gevent monkey patching is not activated.')
