import abc
import time

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class BaseEvent(ABC):
    def __init__(self, user_id):
        self.timestamp = self._get_time()
        self.userId = user_id

    def _get_time(self):
        return int(round(time.time() * 1000))


class ExposureEvent(BaseEvent):
    def __init__(self, user_id, experiment_id, experiment_key, variation_id, variation_key):
        super(ExposureEvent, self).__init__(user_id)
        self.experimentId = experiment_id
        self.experimentKey = experiment_key
        self.variationId = variation_id
        self.variationKey = variation_key


class TrackEvent(BaseEvent):
    def __init__(self, user_id, event_id, event_key, value):
        super(TrackEvent, self).__init__(user_id)
        self.eventTypeId = event_id
        self.eventTypeKey = event_key
        self.value = value
