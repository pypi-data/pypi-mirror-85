# Bosta Python SDK

This repository contains the open source Python SDK for integrating Bosta's APIs into your Python application.

# Table of Contents

- [APIs Documentation](# apis-documentation)
- [Installation](#installation)
- [Usages](#usages)
- [Contribution](#contribution)
- [License](#license)

# APIs Documentation

- [Staging](https://stg-app.bosta.co/docs) APIs swagger documentation.
- [Production](https://app.bosta.co/docs) APIs swagger documentation.

# Installation

You can install the package via [pip](https://pypi.org/project/pip/). Run the following command:

```bash
pip install bostaSDK
```

# Usage

    ``` python
    import os

    from bostaSDK.apiClient import ApiClient
    from bostaSDK import delivery
    from bostaSDK import pickup
    from bostaSDK.utils import Receiver, Address, ContactPerson, DeliveryTypes


    apiKey=os.environ["BOSTA-API-KEY"]="your api key"
    baseUrl=os.environ["BOSTA-BASE-URL"]="bosta base url"


    ################ ApiClient ################# 
    # Parameters:
    #     apiKey (string): Business api key
    #     apiBase (string): Bosta host url
    apiClient=ApiClient(apiKey, baseUrl)


    ################ Deliveries ################# 
    ################# List Deliveries ################# 
    # 1. Create new instance from ListAllDeliveriesRequest
    #  Parameters:
    #     pageNumber (int): Page Number
    #     limit (int): Number of deliveries returned from api
    listAllDeliveriesRequest = delivery.list.ListAllDeliveriesRequest(3, 10) 
    
    # 2. Send list all deliveries request
    #   Parameters:
    #       listAllDeliveriesRequest (ListAllDeliveriesRequest)
    listAllDeliveriesResponse = apiClient.delivery.listAll(listAllDeliveriesRequest)
    listAllDeliveriesResponse.count
    listAllDeliveriesResponse.deliveries

    ################# Create new Delivery #################    
    # 1. Create new Receiver  
    # Parameters:
    #   firstName (str)
    #   lastName (str)
    #   email (str)
    #   phone (str)
    reciever=Receiver("firstName", "lastName", "test@example.com", "01090055000")

    # 2. Create new Address  
    #   Parameters:
    #       cityCode (str)
    #       zone (str)
    #       secondLine (str)
    #       district (str)
    #       buildingNumber (int)
    #       floor (int)
    #        apartment (int)
    dropOffAddress=Address("EG-01", "Maadi", "Maadi", "104")

    # 3. Create new instance from CreateDeliveryRequest
    #    Parameters:
    #       deliveryType (int)
    #       cod (int): Cash on delivery amount
    #       dropOffAddress (Address)
    #       cashOnDelivery (int): Cash on delivery amount
    #       receiver (Receiver)
    #       deliverySpecs (DeliverySpecs)
    #       notes (str)
    #       businessReference (str)

    createDeliveryReq=delivery.create.CreateDeliveryRequest(
        DeliveryTypes.DELIVERY_TYPES['SEND']['code'],
        100, dropOffAddress, reciever
    )

    # 4. Send Create Delivery Request
    #   Parameters:
    #       createDeliveryReq (CreateDeliveryRequest)

    createDeliveryResponse=apiClient.delivery.create(createDeliveryReq)
    deliveryId = createDeliveryResponse.get_deliveryId()


    ################# Print Airway Bill ################# 
    # 1. Create new instance from PrintAWBRequest
    #   Parameters:
    #       deliveryIds (array): List of delivery ids
    printAWBreq = delivery.printAWB.PrintAWBRequest(deliveryId)

    # 2. Send Print Airway bill request
    #   Parameters:
    #       printAWBreq (PrintAWBRequestrray)
    printAirWayBillResponse = apiClient.delivery.printAirWayBill(printAWBreq)
    printAirWayBillResponse.get_data()


    ################# Track Delivery #################
    # 1. Create new instance from TrackDeliveryRequest
    #   Parameters:
    #       deliveryId (str)
    trackDeliveryRequest = delivery.track.TrackDeliveryRequest(deliveryId)

    # 2. Send track delivery request
    #   Parameters:
    #       trackDeliveryRequest (TrackDeliveryRequest)
    trackDeliveryResponse = apiClient.delivery.track(trackDeliveryRequest)
    trackDeliveryResponse.get_message()


    ################# Get Delivery #################
    # 1. Create new instance from GetDeliveryDetailsRequest
    #   Parameters:
    #       deliveryId (str)
    getDeliveryDetailsRequest = delivery.get.GetDeliveryDetailsRequest(deliveryId)
    
    # 2. Send get delivery request
    #   Parameters:
    #       getDeliveryDetailsRequest (GetDeliveryDetailsRequest)
    getDeliveryDetailsResponse = apiClient.delivery.get(getDeliveryDetailsRequest)
    getDeliveryDetailsResponse.get_message()

    ################# Update Delivery #################
    # 1. Create new instance from UpdateDeliveryRequest
    #    Parameters:
    #       deliveryId (str): Delivery Id
    #       specs (DeliverySpecs)
    #       pickUpAddress (Address, optinal)
    #       dropOffAddress (Address, optinal)
    #       returnAddress (Address, optinal)
    #       cod (int, optinal): Cash on delivery amount
    #       receiver (Receiver, optinal)
    #       businessReference (str, optinal): Business refrence
    #       webhookUrl (str, optinal)
    newReciever=Receiver("user", "test", "test@example.com", "01090055000")
    updateDeliveryRequest = delivery.update.UpdateDeliveryRequest(
        deliveryId,
        receiver=newReciever,
        cod=120
    )
    # 2. Send update delivery request
    #   Parameters:
    #       updateDeliveryRequest (UpdateDeliveryRequest)
    updateDeliveryResponse = apiClient.delivery.update(updateDeliveryRequest)
    updateDeliveryResponse.get_message()
    
    #################  Terminate Delivery #################
    # 1. Create new instance from TerminateDeliveryRequest
    #   Parameters:
    #       deliveryId (str)
    terminateDeliveryRequest = delivery.terminate.TerminateDeliveryRequest(deliveryId)

    # 2. Send terminate delivery request
    #   Parameters:
    #       terminateDeliveryRequest (TerminateDeliveryRequest)
    terminateDeliveryResponse = apiClient.delivery.terminate(terminateDeliveryRequest)
    terminateDeliveryResponse.get_message()

    ################ Pickups ################# 
    ################ Create New Pickup #################
    # 1. Create new instance from ContactPerson
    #   Parameters:
    #       name (str)
    #       phone (str)
    #       email (str)
    contactPerson = ContactPerson("userName", "01090000000", "example@bosta.co")

    # 2. Create new instance from CreatePickupRequest
    #   Parameters:
    #       scheduledDate (str): Pickup scheduled date 
    #                            "Mon Sep 30 2019 00:00:00 GMT+0200",
    #       scheduledTimeSlot (str): "10:00 to 13:00" or "13:00 to 16:00"
    #       contactPerson (ContactPerson)
    #       businessId (str)
    #       businessLocationId (str)
    #       warehouseId (str)
    #       noOfPackages (int)
    #       notes (str) 
    createPickupRequest = pickup.create.CreatePickupRequest(
        "Mon Nov 23 2021 00:00:00 GMT+0200",
        apiClient.pickupTimeSlots[0], contactPerson
    )
    # 3. Send create pickup request
    #   Parameters:
    #       createPickupRequest (CreatePickupRequest)
    createPickupResponse=apiClient.pickup.create(createPickupRequest)
    createPickupResponse.get_message()
    # If pickup request created successfully
    newPickupId=createPickupResponse.get_pickupId()


    ################ List Pickups #################
    # 1. Create new instance from ListAllPickupsRequest
    #   Parameters:
    #     pageId (int)
    #     sortBy (str)
    #     sortValue (str)
    listAllPickupsRequest = pickup.list.ListAllPickupsRequest(2)

    # 2. Send list all pickups request
    #   Parameters:
    #       listAllPickupsRequest (ListAllPickupsRequest)
    listAllPickupsResponse=apiClient.pickup.listAll(listAllPickupsRequest)
    listAllPickupsResponse.get_message()
    listAllPickupsResponse.pickups

    ################ Get Pickup #################
    # 1. Create new instance from GetPickupDetailsRequest
    #   Parameters:
    #     pickupId (str): Pickup Id
    getPickupDetailsRequest = pickup.get.GetPickupDetailsRequest(newPickupId)
    
    # 2. Send get pickup request
    #   Parameters:
    #       getPickupDetailsRequest (GetPickupDetailsRequest)
    getPickupDetailsResponse = apiClient.pickup.get(getPickupDetailsRequest)
    getPickupDetailsResponse.state

    ################ Update Pickup #################
    # 1. Create new instance from UpdatePickupRequest
    #   Parameters:
    #     _id (str): Pickup Id
    #     businessId (str)
    #     scheduledDate (str)
    #     scheduledTimeSlot (str)
    #     contactPerson (ContactPerson)
    #     businessLocationId (str)
    #     warehouseId (str)
    #     noOfPackages (str)
    #     notes (str)

    updatePickupRequest = pickup.update.UpdatePickupRequest(
        newPickupId, 
        contactPerson=ContactPerson("newUser", "010193155922", "user2@bosta.co"),
        noOfPackages="200"
    )
      
    # 2. Send update pickup request
    #   Parameters:
    #       updatePickupRequest (UpdatePickupRequest)
    updatePickupResponse =apiClient.pickup.update(updatePickupRequest)
    updatePickupResponse.get_message()
    
    ################ Delete Pickup #################
    # 1. Create new instance from DeletePickupRequest
    #   Parameters:
    #     pickupId (str): Pickup Id
    deletePickupRequest = pickup.delete.DeletePickupRequest(newPickupId)

    # 2. Send delete pickup request
    #   Parameters:
    #       deletePickupRequest (UpdatePickupRequest)
    apiClient.pickup.delete(deletePickupRequest)

    ```

## Contribution

We are open to, and grateful for, any contributions made by the community.
By contributing to Bosta, you agree to abide by the code of conduct.
- [Contributing Guide](CONTRIBUTING.md) 
- [Code of Conduct](CODE_OF_CONDUCT.md)

## License

The MIT License (MIT) [License](LICENSE).
