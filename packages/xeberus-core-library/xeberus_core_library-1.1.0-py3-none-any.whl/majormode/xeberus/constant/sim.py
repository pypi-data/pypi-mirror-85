# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.model.enum import Enum


# Billing frequency for the data service used by a SIM card.
BillingFrequency = Enum(
    'monthly',
    'yearly',
)

# Indicate the billing method of a SIM card.
BillingMethod = Enum(
    # Billing method for which credit is purchased in advance of service
    # use. The purchased credit is used to pay for mobile phone services at
    # the point the service is accessed or consumed.  If there is no
    # available credit, then access to the requested service is denied by
    # the mobile network operaton.  Users are able to top up their credit
    # at any time.
    'prepaid',

    # Service is provided by a prior arrangement with a mobile network
    # operator.  The customer is billed after the fact according to their
    # use of mobile services at the end of each month.  Typically, the
    # customer's contract specifies a limit or "allowance" of data, and the
    # customer will be billed at a flat rate for any usage equal to or less
    # than that allowance.  Any usage above that limit may incur extra
    # charges.
    'postpaid',
)

# Owner of a SIM card is, and therefore who is responsible for paying
# the SIM card fee to the carrier.
Ownership = Enum(
    # The customer is the owner.
    'customer',

    # The service provider is the owner.
    'service',
)

# Payment method to be used to increase the remaining balance of a SIM
# card.
PaymentMethod = Enum(
    # A "top-up" or "refill" card at retail. Such a card is stamped with a
    # unique code (often under a scratch-off panel) which must be sent by
    # the device in order to add the credit onto the balance.
    'topup',
)

SimCardNotification = Enum(
    # Indicate that the alert state of a vehicle has changed as reported
    # by the a device mounted on this vehicle.
    'on_card_sim_inserted',
)
