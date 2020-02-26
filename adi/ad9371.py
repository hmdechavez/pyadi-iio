# Copyright (C) 2019 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from adi.context_manager import context_manager
from adi.obs import obs
from adi.rx_tx import rx_tx


class ad9371(rx_tx, context_manager):
    """ AD9371 Transceiver """

    _complex_data = True
    _rx_channel_names = ["voltage0_i", "voltage0_q", "voltage1_i", "voltage1_q"]
    _tx_channel_names = ["voltage0", "voltage1", "voltage2", "voltage3"]
    _obs_channel_names = ["voltage0_i", "voltage0_q"]
    _device_name = ""

    def __init__(self, uri=""):

        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = self._ctx.find_device("ad9371-phy")
        self._rxadc = self._ctx.find_device("axi-ad9371-rx-hpc")
        self._rxobs = self._ctx.find_device("axi-ad9371-rx-obs-hpc")
        self._txdac = self._ctx.find_device("axi-ad9371-tx-hpc")

        rx_tx.__init__(self)

        self.obs = obs(
            self._ctx, self._rxobs, self._obs_channel_names, self._complex_data
        )

    @property
    def gain_control_mode(self):
        """gain_control_mode: Mode of receive path AGC. Options are:
        automatic, hybrid, manual"""
        return self._get_iio_attr_str("voltage0", "gain_control_mode", False)

    @gain_control_mode.setter
    def gain_control_mode(self, value):
        self._set_iio_attr("voltage0", "gain_control_mode", False, value)

    @property
    def rx_hardwaregain(self):
        """rx_hardwaregain: Gain applied to RX path. Only applicable when
        gain_control_mode is set to 'manual'"""
        return self._get_iio_attr("voltage0", "hardwaregain", False)

    @rx_hardwaregain.setter
    def rx_hardwaregain(self, value):
        if self.gain_control_mode == "manual":
            self._set_iio_attr("voltage0", "hardwaregain", False, value)

    @property
    def tx_hardwaregain(self):
        """tx_hardwaregain: Attenuation applied to TX path"""
        return self._get_iio_attr("voltage0", "hardwaregain", True)

    @tx_hardwaregain.setter
    def tx_hardwaregain(self, value):
        self._set_iio_attr("voltage0", "hardwaregain", True, value)

    @property
    def rx_rf_bandwidth(self):
        """rx_rf_bandwidth: Bandwidth of front-end analog filter of RX path"""
        return self._get_iio_attr("voltage0", "rf_bandwidth", False)

    @property
    def tx_rf_bandwidth(self):
        """tx_rf_bandwidth: Bandwidth of front-end analog filter of TX path"""
        return self._get_iio_attr("voltage0", "rf_bandwidth", True)

    @property
    def rx_sample_rate(self):
        """rx_sample_rate: Sample rate RX path in samples per second"""
        return self._get_iio_attr("voltage0", "sampling_frequency", False)

    @property
    def tx_sample_rate(self):
        """tx_sample_rate: Sample rate TX path in samples per second"""
        return self._get_iio_attr("voltage0", "sampling_frequency", True)

    @property
    def rx_lo(self):
        """rx_lo: Carrier frequency of RX path"""
        return self._get_iio_attr("altvoltage0", "RX_LO_frequency", True)

    @rx_lo.setter
    def rx_lo(self, value):
        self._set_iio_attr("altvoltage0", "RX_LO_frequency", True, value)

    @property
    def tx_lo(self):
        """tx_lo: Carrier frequency of TX path"""
        return self._get_iio_attr("altvoltage1", "TX_LO_frequency", True)

    @tx_lo.setter
    def tx_lo(self, value):
        self._set_iio_attr("altvoltage1", "TX_LO_frequency", True, value)

    @property
    def sn_lo(self):
        """sn_lo: Carrier frequency of Sniffer/ORx path"""
        return self._get_iio_attr("altvoltage2", "RX_SN_LO_frequency", True)

    @sn_lo.setter
    def sn_lo(self, value):
        self._set_iio_attr("altvoltage2", "RX_SN_LO_frequency", True, value)

    @property
    def obs_rf_port_select(self):
        """obs_rf_port_select: Observation path source. Options are:
            OFF - SnRx path is disabled
            ORX1_TX_LO – SnRx operates in observation mode on ORx1 with Tx LO synthesizer
            ORX2_TX_LO – SnRx operates in observation mode on ORx2 with Tx LO synthesizer
            INTERNALCALS – enables scheduled Tx calibrations while using SnRx path. The enableTrackingCals function needs to be called in RADIO_OFF state. It sets the calibration mask, which the scheduler will later use to schedule the desired calibrations. This command is issued in RADIO_OFF. Once the AD9371 moves to RADIO_ON state, the internal scheduler will use the enabled calibration mask to schedule calibrations whenever possible, based on the state of the transceiver. The Tx calibrations will not be scheduled until INTERNALCALS is selected and the Tx calibrations are enabled in the cal mask.
            OBS_SNIFFER – SnRx operates in sniffer mode with latest selected Sniffer Input – for hardware pin control operation. In pin mode, the GPIO pins designated for ORX_MODE would select SNIFFER mode. Then MYKONOS_setSnifferChannel function would choose the channel.
            ORX1_SN_LO – SnRx operates in observation mode on ORx1 with SNIFFER LO synthesizer
            ORX2_SN_LO – SnRx operates in observation mode on ORx2 with SNIFFER LO synthesizer
            SN_A – SnRx operates in sniffer mode on SnRxA with SNIFFER LO synthesizer
            SN_B – SnRx operates in sniffer mode on SnRxB with SNIFFER LO synthesizer
            SN_C – SnRx operates in sniffer mode on SnRxC with SNIFFER LO synthesizer
        """
        return self._get_iio_attr_str("voltage2", "rf_port_select", False)

    @obs_rf_port_select.setter
    def obs_rf_port_select(self, value):
        self._set_iio_attr("voltage2", "rf_port_select", False, value)
