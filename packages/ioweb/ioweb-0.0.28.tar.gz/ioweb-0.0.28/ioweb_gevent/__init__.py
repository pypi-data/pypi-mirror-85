from gevent.monkey import patch_all
patch_all()

try:
    import grpc
except ImportError:
    pass
else:
    if grpc.__version__ != '1.18.0':
        raise Exception('grpcio version must be 1.18.0')
    from grpc.experimental import gevent
    gevent.init_gevent()
