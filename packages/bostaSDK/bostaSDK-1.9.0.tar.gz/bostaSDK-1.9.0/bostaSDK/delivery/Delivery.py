
import os
import json
import logging

from bostaSDK.utils.Address import Address
from bostaSDK.utils.Receiver import Receiver
from bostaSDK.utils.DeliverySpecs import DeliverySpecs


from .list.ListAllDeliveriesRequest import ListAllDeliveriesRequest
from .list.ListAllDeliveriesResponse import ListAllDeliveriesResponse
from .get.GetDeliveryDetailsRequest import GetDeliveryDetailsRequest
from .get.GetDeliveryDetailsResponse import GetDeliveryDetailsResponse
from .update.UpdateDeliveryRequest import UpdateDeliveryRequest
from .update.UpdateDeliveryResponse import UpdateDeliveryResponse
from .printAWB.PrintAWBRequest import PrintAWBRequest
from .printAWB.PrintAWBResponse import PrintAWBResponse
from .terminate.TerminateDeliveryRequest import TerminateDeliveryRequest
from .terminate.TerminateDeliveryResponse import TerminateDeliveryResponse
from .create.CreateDeliveryRequest import CreateDeliveryRequest
from .create.CreateDeliveryResponse import CreateDeliveryResponse
from .track.TrackDeliveryRequest import TrackDeliveryRequest
from .track.TrackDeliveryResponse import TrackDeliveryResponse


class Delivery:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def listAll(self, listAllDeliveriesRequest: ListAllDeliveriesRequest) -> ListAllDeliveriesResponse:
        """
        List All Deliveries.

        Parameters:
        listAllDeliveriesRequest (ListAllDeliveriesRequest)

        Returns: New instance from ListAllDeliveriesResponse.
        """
        try:
            logging.info("list all business deliveries")
            url = "/deliveries"
            params = listAllDeliveriesRequest.toUrlQueryParamters()
            response = self.apiClient.send('get', url, params=params)
            if (response.status_code) != 200:
                return ListAllDeliveriesResponse(response.text)
            instance = ListAllDeliveriesResponse(response.json())
            return instance
        except Exception as exp:
            logging.error(exp)
            raise exp

    def get(self, getDeliveryDetailsRequest: GetDeliveryDetailsRequest) -> GetDeliveryDetailsResponse:
        """
        Get Delivery.

        Parameters:
        getDeliveryDetailsRequest (GetDeliveryDetailsRequest)

        Returns: New instance from GetDeliveryDetailsResponse.
        """
        try:
            logging.info('Get Delivery')
            url = "/deliveries/" + \
                str(getDeliveryDetailsRequest.get_deliveryId())
            response = self.apiClient.send('get', url)
            if (response.status_code) != 200:
                return GetDeliveryDetailsResponse(response.text)
            return GetDeliveryDetailsResponse(response.json())
        except Exception as exp:
            logging.error(exp)
            raise exp

    def printAirWayBill(self, printAWBRequest: PrintAWBRequest) -> PrintAWBResponse:
        """
        Print Delivery Airway Bill.

        Parameters:
        printAWBRequest (PrintAWBRequest)

        Returns: New instance from PrintAWBResponse.
        """
        try:
            logging.info("Print airway bill")
            url = "/deliveries/awb" +  str(printAWBRequest.get_deliveryId())
            response = self.apiClient.send('get', url)
            if (response.status_code) != 200:
                return PrintAWBResponse(response.text)
            return PrintAWBResponse(response.json())
        except Exception as exp:
            logging.error(exp)
            raise exp

    def create(self, createDeliveryRequest: CreateDeliveryRequest) -> CreateDeliveryResponse:
        """
        Create New Delivery.

        Parameters:
        createDeliveryRequest (CreateDeliveryRequest)

        Returns: New instance from CreateDeliveryResponse.
        """
        try:
            payload = createDeliveryRequest.toJSONPayload()
            logging.info('Create New Delivery: Payload ' + str(payload))
            url = "/deliveries"
            headers = {
                "content-type": "application/json"
            }
            response = self.apiClient.send(
                'post', url, headers=headers, data=payload)
            if (response.status_code) != 201 or (response.status_code) != 200:
                return CreateDeliveryResponse(response.text)
            return CreateDeliveryResponse(response.json())
        except Exception as exp:
            logging.error(exp)
            raise exp

    def update(self, updateDeliveryRequest: UpdateDeliveryRequest) -> UpdateDeliveryResponse:
        """
        Update Delivery.

        Parameters:
        updateDeliveryRequest (UpdateDeliveryRequest)

        Returns: New instance from UpdateDeliveryResponse.
        """
        try:
            logging.info('Update Delivery')
            url = "/deliveries/" + str(updateDeliveryRequest.get_deliveryId())
            payload = updateDeliveryRequest.toJSONPayload()
            response = self.apiClient.send('patch', url, data=payload)
            if (response.status_code) != 200:
                return UpdateDeliveryResponse(response.text)
            return UpdateDeliveryResponse(response.json())
        except Exception as exp:
            logging.error(exp)
            raise exp

    def terminate(self, terminateDeliveryRequest: TerminateDeliveryRequest) -> TerminateDeliveryResponse:
        """
        Terminate Delivery.

        Parameters:
        terminateDeliveryRequest (TerminateDeliveryRequest)

        Returns: New instance from TerminateDeliveryResponse.
        """
        try:
            logging.info("Terminate Delivery")
            url = "/deliveries/" + \
                str(terminateDeliveryRequest.get_deliveryId())
            response = self.apiClient.send('delete', url)
            if (response.status_code) != 200:
                return TerminateDeliveryResponse(response.text)
            return TerminateDeliveryResponse(response.json())
        except Exception as exp:
            logging.error(exp)
            raise exp

    def track(self, trackDeliveryRequest: TrackDeliveryRequest) -> TrackDeliveryResponse:
        """
        Track Delivery.

        Parameters:
        trackDeliveryRequest (TrackDeliveryRequest)

        Returns: New instance from TrackDeliveryResponse.
        """
        try:
            logging.info('Track Delivery')
            url = "/deliveries/" + \
                str(trackDeliveryRequest.get_deliveryId()) + "/tracking"
            response = self.apiClient.send('get', url)
            if (response.status_code) != 200:
                return TrackDeliveryResponse(response.text)
            return TrackDeliveryResponse(response.json())
        except Exception as exp:
            logging.error(exp)
            raise exp
