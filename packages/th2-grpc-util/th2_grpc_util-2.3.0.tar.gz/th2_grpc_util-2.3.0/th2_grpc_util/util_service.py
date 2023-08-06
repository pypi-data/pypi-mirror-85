from . import util_pb2_grpc as importStub

class MessageComparatorServiceService(object):

    def __init__(self, router):
        self.connector = router.get_connection(MessageComparatorServiceService, importStub.MessageComparatorServiceStub)

    def compareFilterVsMessages(self, request, timeout=None):
        return self.connector.create_request('compareFilterVsMessages', request, timeout)

    def compareMessageVsMessage(self, request, timeout=None):
        return self.connector.create_request('compareMessageVsMessage', request, timeout)
