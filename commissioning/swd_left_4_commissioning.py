#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
import sys
import time

import commissioning

from smcdbusclient.communication import BlocId
from smcdbusclient.nmt import NMTCommand

from smcdbusclient.safe_motion import SafetyControlWordId, SafetyFunctionId

from smcdbusclient.srdo import SRDOId, SRDOParameters


def update_SRDO_parameters():
    # SRDO_9
    # communication parameters (RX)
    srdoParam = SRDOParameters()
    srdoParam.can_id1 = 0x109
    srdoParam.can_id2 = 0x10A
    srdoParam.valid = 1
    srdoParam.sct = 50
    srdoParam.srvt = 20
    error = commissioning.srdo_client.setSRDOParameters(SRDOId.SRDO_9, srdoParam)
    commissioning.check("setSRDOParameters(SRDOId.SRDO_9)", error)

    # mapping parameters
    scw = SafetyControlWordId.CAN_2
    scwMapping = [
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
    ]
    scwMapping[0] = SafetyFunctionId.STO
    scwMapping[1] = SafetyFunctionId.STO

    commissioning.safe_motion_client.setSafetyControlWordMapping(scw, commissioning.list_to_swm(scwMapping))
    commissioning.check("setSafetyControlWordMapping()", error)

    # SRDO_16
    # communication parameters (TX)
    srdoParam = SRDOParameters()
    srdoParam.can_id1 = 0x160
    srdoParam.can_id2 = 0x161
    srdoParam.valid = 1
    srdoParam.sct = 25
    srdoParam.srvt = 20
    error = commissioning.srdo_client.setSRDOParameters(SRDOId.SRDO_16, srdoParam)
    commissioning.check("setSRDOParameters(SRDOId.SRDO_16)", error)

    # mapping parameters
    scw = SafetyControlWordId.SAFEIN_1
    scwMapping = [
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
        SafetyFunctionId.NONE,
    ]

    scwMapping[0] = SafetyFunctionId.STO
    scwMapping[1] = SafetyFunctionId.STO
    scwMapping[2] = SafetyFunctionId.SDIN_1
    scwMapping[3] = SafetyFunctionId.SDIN_1
    scwMapping[4] = SafetyFunctionId.SLS_1
    scwMapping[5] = SafetyFunctionId.SLS_1

    commissioning.safe_motion_client.setSafetyControlWordMapping(scw, commissioning.list_to_swm(scwMapping))
    commissioning.check("setSafetyControlWordMapping()", error)

    # Update configuration validity
    error = commissioning.srdo_client.setSRDOConfigurationValidity()
    commissioning.check("setSRDOConfigurationValidity()", error)


# =======================
#      MAIN PROGRAM
# =======================


def main(argv):

    instance_id = "swd_left"
    node_id = 0x4
    polarity = True  # velocity demand value/motor revolution increments shall be multiplied by –1 if True
    vl_acc_delta_speed = 1500
    vl_dec_delta_speed = 1500
    restart_acknowledge_behavior = False
    can_alim = False
    can_io_alim = True

    # SLS parameters
    sls_1_vl_limit = 680
    sls_1_vl_time_monitoring = 1000
    sls_1_sto_error_reaction = False
    sls_2_vl_limit = 850
    sls_2_vl_time_monitoring = 1000
    sls_2_sto_error_reaction = False

    # SLSa parameters 
    slsa_1_p_vl_limit = 100
    slsa_1_n_vl_limit = 680
    slsa_1_vl_time_monitoring = 1000
    slsa_1_sto_error_reaction = False
    slsa_2_p_vl_limit = 100
    slsa_2_n_vl_limit = 680
    slsa_2_vl_time_monitoring = 1000
    slsa_2_sto_error_reaction = False

    # SMS parameters
    sms_p_vl_limit = 1400
    sms_n_vl_limit = 1400
    sms_sto_error_reaction = False 

    # Create DBus clients
    commissioning.create_dbus_clients(instance_id)

    # Restore factory parameters
    error = commissioning.communication_client.restoreDefaultParameters(BlocId.ALL)
    commissioning.check("Restore factory parameters", 1)  # error)

    # Reset to apply parameters
    error = commissioning.nmt_client.setNMTState(NMTCommand.RESET_NODE)
    commissioning.check("Reset to apply parameters", error)

    # Sleep 1000ms
    time.sleep(1.0)

    #
    # Change Network parameters
    #
    commissioning.update_network_parameters(node_id)

    #
    # Change PDO communication parameters
    #
    commissioning.update_communication_parameters(node_id)

    #
    # Change Polarity parameters
    #
    commissioning.update_polarity_parameters(polarity)

    #
    # Change SRDO parameters
    #
    commissioning.disable_SRDO_parameters()

    #
    # Update SRDO parameters
    #
    update_SRDO_parameters()

    #
    # Update Ramps
    #
    commissioning.update_ramps(vl_acc_delta_speed, vl_dec_delta_speed)

    #
    # Update STO parameters
    #
    commissioning.update_STO_parameters(restart_acknowledge_behavior)

    #
    # Update SLS parameters
    #
    commissioning.update_SLS_1_parameters(sls_1_vl_limit, sls_1_vl_time_monitoring, sls_1_sto_error_reaction)
    # commissioning.update_SLS_2_parameters(sls_2_vl_limit, sls_2_vl_time_monitoring, sls_2_sto_error_reaction)

    #
    # Update SLSa parameters
    #
    # commissioning.update_SLSa_1_parameters(slsa_1_p_vl_limit, slsa_1_n_vl_limit, slsa_1_vl_time_monitoring, slsa_1_sto_error_reaction)
    # commissioning.update_SLSa_2_parameters(slsa_2_p_vl_limit, slsa_2_n_vl_limit, slsa_2_vl_time_monitoring, slsa_2_sto_error_reaction)

    #
    # Update SMS parameters
    #
    # commissioning.update_SMS_parameters(sms_p_vl_limit, sms_n_vl_limit, sms_sto_error_reaction)

    #
    # Update PID parameters for motor speed
    #
    commissioning.update_motor_speed_PID()

    #
    # Update error behavior
    #
    commissioning.update_error_behavior()

    #
    # Update output sources
    #
    commissioning.update_output_sources(can_alim, can_io_alim)

    # Save modified parameters
    error = commissioning.communication_client.storeParameters(BlocId.ALL)
    commissioning.check("storeParameters", 1)  # error)

    # Reset to apply parameters
    error = commissioning.nmt_client.setNMTState(NMTCommand.RESET_NODE)
    commissioning.check("setNMTState", error)

    # Exit with success
    print("\nCommissioning succeeded !")


if __name__ == "__main__":
    main(sys.argv[1:])
