import boto3
import os
import json

from enum import Enum

from properly_util_python.properly_logging import ProperLogger


class ProperlyEvents(str, Enum):
    USER_CREATED = 'userCreated'
    STAGE_CHANGED_OFFER = 'stageChangedOffer'
    USER_ENTERED_ALL_OFFER_INFO = 'userEnteredAllOfferInfo'
    SHOWING_UPDATED_OR_CREATED = 'userShowingUpdatedOrCreated'
    ACCEPTED_OFFER = 'userAcceptedOffer'
    SEARCH_RESULTS_CHANGED = 'searchResultsChanged'
    PPR_FEEDBACK = 'pprFeedback'
    FAVOURITE_ADDED = 'favouriteAdded'
    FAVOURITE_REMOVED = 'favouriteRemoved'


STREAM_BY_STAGE = {
    'staging': 'staging-events-002',
    'prod': 'prod-events-002',
}


class EventBusBase:

    def send_event(self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict):
        raise NotImplementedError


class EventBus(EventBusBase):

    def __init__(self, kinesis=None, logger=None):
        stage = os.environ.get('PROPERLY_STAGE', 'staging')
        self.kinesis = kinesis or boto3.client('kinesis')
        self.stream_name = STREAM_BY_STAGE.get(stage, STREAM_BY_STAGE['staging'])
        self.logger = logger if logger else ProperLogger("EventBus")

    def send_event(self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict):

        event_to_send = {
            'eventName': event_name,
            data_block_name: data_block
        }

        self.logger.debug("Sending event", {"event": event_to_send})

        event_as_json = json.dumps(event_to_send)

        event_as_bytes = event_as_json.encode('utf-8')
        # bytes are base64 encoded inside the put_record call

        self.logger.debug("Event as bytes", {"event_as_bytes": event_as_bytes})

        self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=event_as_bytes,
            PartitionKey=properly_user_id,
        )


class PropertyEvents(str, Enum):
    PROPERTY_VERIFIED_INFO_UPDATED = 'propertyVerifiedInfoUpdated'


class PropertyEventBus(EventBusBase):
    def __init__(self, stream_name, kinesis=None, logger=None):
        stage = os.environ.get('PROPERLY_STAGE', 'staging')
        self.kinesis = kinesis or boto3.client('kinesis')
        self.stream_name = f"{stage}-{stream_name}"
        self.logger = logger if logger else ProperLogger("PropertyEventBus")

    def send_event(self, property_id: str, event_name: PropertyEvents, data_block_name: str, data_block: dict):

        event_to_send = {
            'eventName': event_name,
            data_block_name: data_block
        }

        self.logger.debug("Sending event", {"event": event_to_send})

        event_as_json = json.dumps(event_to_send)

        event_as_bytes = event_as_json.encode('utf-8')
        # bytes are base64 encoded inside the put_record call

        self.logger.debug("Event as bytes", {"event_as_bytes": event_as_bytes})

        self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=event_as_bytes,
            PartitionKey=property_id,
        )
