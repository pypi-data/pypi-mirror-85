#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""
from smbus2 import SMBusWrapper
import time

class APDS_9960():
    DEFAULT_I2C_ADDRESS = 0x39

    # Register addresses
    ENABLE_REG_ADDRESS = 0x80
    CONFIG_1_REG_ADDRESS = 0x8D
    CONFIG_2_REG_ADDRESS = 0x90
    CONFIG_3_REG_ADDRESS = 0x9F
    CONTROL_1_REG_ADDRESS = 0x8F
    INTERRUPT_PERSISTANCE_REG_ADDRESS = 0x8C
    STATUS_REG_ADDRESS = 0x93

    # Proximity Registers Addresses
    PROX_INT_LOW_THR_REG_ADDRESS = 0x89
    PROX_INT_HIGH_THR_REG_ADDRESS = 0x8B
    PROX_PULSE_COUNT_REG_ADDRESS = 0x8E
    PROX_UP_RIGHT_OFFSET_REG_ADDRESS = 0x9D
    PROX_DOWN_LEFT_OFFSET_REG_ADDRESS = 0x9E
    PROX_DATA_REG_ADDRESS = 0x9C

    # ALS Register Addresses
    ALS_ATIME_REG_ADDRESS = 0x81
    ALS_INT_LOW_THR_LOW_BYTE_REG_ADDRESS = 0x84  # This register provides the low byte of the low interrupt threshold.
    ALS_INT_LOW_THR_HIGH_BYTE_REG_ADDRESS = 0x85  # This register provides the high byte of the low interrupt threshold.
    ALS_INT_HIGH_THR_LOW_BYTE_REG_ADDRESS = 0x86  # This register provides the low byte of the high interrupt threshold.
    ALS_INT_HIGH_THR_HIGH_BYTE_REG_ADDRESS = 0x87  # This register provides the high byte of the high interrupt threshold.

    CLEAR_DATA_LOW_BYTE_REG_ADDRESS = 0x94  # Low Byte of clear channel data.
    CLEAR_DATA_HIGH_BYTE_REG_ADDRESS = 0x95  # High Byte of clear channel data.
    RED_DATA_LOW_BYTE_REG_ADDRESS = 0x96  # Low Byte of red channel data.
    RED_DATA_HIGH_BYTE_REG_ADDRESS = 0x97  # High Byte of red channel data.
    GREEN_DATA_LOW_BYTE_REG_ADDRESS = 0x98  # Low Byte of green channel data.
    GREEN_DATA_HIGH_BYTE_REG_ADDRESS = 0x99  # High Byte of green channel data.
    BLUE_DATA_LOW_BYTE_REG_ADDRESS = 0x9A  # Low Byte of blue channel data.
    BLUE_DATA_HIGH_BYTE_REG_ADDRESS = 0x9B  # High Byte of blue channel data.

    # Gesture Register Addresses
    GESTURE_PROX_ENTER_THR_REG_ADDRESS = 0xA0
    GESTURE_EXIT_THR_REG_ADDRESS = 0xA1
    GESTURE_CONFIG_1_REG_ADDRESS = 0xA2
    GESTURE_CONFIG_2_REG_ADDRESS = 0xA3
    GESTURE_CONFIG_3_REG_ADDRESS = 0xAA
    GESTURE_CONFIG_4_REG_ADDRESS = 0xAB
    GESTURE_OFFSET_REG_ADDRESSES = [0xA4, 0xA5, 0xA7, 0xA9]
    GESTURE_PULSE_COUNT_AND_LEN_REG_ADDRESS = 0xA6
    GESTURE_FIFO_LEVEL_REG_ADDRESS = 0xAE
    GESTURE_FIFO_UP_REG_ADDRESS = 0xFC
    GESTURE_FIFO_DOWN_REG_ADDRESS = 0xFD
    GESTURE_FIFO_LEFT_REG_ADDRESS = 0xFE
    GESTURE_FIFO_RIGHT_REG_ADDRESS = 0xFF
    GESTURE_STATUS_REG_ADDRESS = 0xAF

    # Wait Registers Addresses
    WAIT_TIME_REG_ADDRESS = 0x83

    # Clear interrupt regs
    FORCE_INTERRUPT_REG_ADDRESS = 0xE4
    PROXIMITY_INT_CLEAR_REG_ADDRESS = 0xE5
    ALS_INT_CLEAR_REG_ADDRESS = 0xE6
    CLEAR_ALL_NON_GEST_INT_REG_ADDRESS = 0xE7

    # Proximity pulse lengths
    PULSE_LEN_4_MICROS = 0
    PULSE_LEN_8_MICROS = 1
    PULSE_LEN_16_MICROS = 2
    PULSE_LEN_32_MICROS = 3

    # Led drive levels
    LED_DRIVE_100_mA = 0
    LED_DRIVE_50_mA = 1
    LED_DRIVE_25_mA = 2
    LED_DRIVE_12_5_mA = 3

    # Led Boost levels
    LED_BOOST_100 = 0
    LED_BOOST_150 = 1
    LED_BOOST_200 = 2
    LED_BOOST_300 = 3

    # Proximity gain
    PROXIMITY_GAIN_1X = 0
    PROXIMITY_GAIN_2X = 1
    PROXIMITY_GAIN_4X = 2
    PROXIMITY_GAIN_8X = 3

    # ALS Gain
    ALS_GAIN_1X = 0
    ALS_GAIN_4X = 1
    ALS_GAIN_16X = 2
    ALS_GAIN_64X = 3

    # Gesture FIFO interrupt levels
    FIFO_INT_AFTER_1_DATASET = 0
    FIFO_INT_AFTER_4_DATASETS = 1
    FIFO_INT_AFTER_8_DATASETS = 2
    FIFO_INT_AFTER_16_DATASETS = 3

    # Gesture exit persistences
    EXIT_AFTER_1_GESTURE_END = 0
    EXIT_AFTER_2_GESTURE_END = 1
    EXIT_AFTER_4_GESTURE_END = 2
    EXIT_AFTER_7_GESTURE_END = 3

    # Gesture wait time
    GESTURE_WAIT_0_MILLIS = 0
    GESTURE_WAIT_2_8_MILLIS = 1
    GESTURE_WAIT_5_6_MILLIS = 2
    GESTURE_WAIT_8_4_MILLIS = 3
    GESTURE_WAIT_14_MILLIS = 4
    GESTURE_WAIT_22_4_MILLIS = 5
    GESTURE_WAIT_30_8_MILLIS = 6
    GESTURE_WAIT_39_2_MILLIS = 7

    def __init__(self, i2c_address=DEFAULT_I2C_ADDRESS, i2c_bus=1):
        self.i2c_address = i2c_address
        self.i2c_bus = i2c_bus

    # =========================================================================
    #     I2C functions
    # =========================================================================

    def read_byte_data(self, register_address, amount=1):
        """Read a byte (or multiple bytes) from the device.\n
        :register_address: the adress where the read operation starts.\n
        :amount = 1: the amount of bytes to read, by default it is 1.\n
        Return value: an int if the amount is 1, a list of ints if the amount is greater than 1.\n
        """
        with SMBusWrapper(self.i2c_bus) as bus:
            data = bus.read_i2c_block_data(self.i2c_address, register_address, amount)
        if amount == 1:
            return data[0]
        else:
            return data

    def write_byte_data(self, value, register_address):
        """Write a byte (or multiple bytes) to the device.\n
        :value: The value to write to the register. Can also be a list of values.\n
        :register_address: the address where the write operation starts.\n
        """
        if type(value) != list:
            value = [value]
        with SMBusWrapper(self.i2c_bus) as bus:
            bus.write_i2c_block_data(self.i2c_address, register_address, value)

    def write_flag_data(self, flag, register_address, offset):
        """Writes a flag to a register with the given offset.\n
        :flag: A list of booleans
        :register_address: the address at which to write the flag
        :offset: the offset inside the register
        """
        if len(flag) + offset > 8:
            raise ValueError("Flag + offset exceeded 8 bit limit.")

        register_value = self.read_byte_data(register_address)
        for index, value in enumerate(flag):
            if value:
                register_value |= value << (index + offset)
            else:
                register_value &= value << (index + offset)
        self.write_byte_data(register_value, register_address)

    # =========================================================================
    #     Device Methods
    # =========================================================================

    def wake_up(self, wake_up=True):
        """Toggles between IDLE and SLEEP state. In sleep state the device can 
        still receive and process I2C messages.\n
        :power_up = True: Enter the IDLE state if True else enter SLEEP state, by default the value is True.
        """
        self.write_flag_data([wake_up], APDS_9960.ENABLE_REG_ADDRESS, 0)
        time.sleep(0.01)

    def reset(self):
        self.set_sleep_after_interrupt(False)
        self.enable_all_engines_and_power_up(False)
        self.enable_proximity_interrupts(False)
        self.enable_proximity_saturation_interrupts(False)
        self.enable_als_interrupts(False)
        self.enable_als_saturation_interrupts(False)
        self.enable_gesture_interrupts(False)

    def enable_all_engines_and_power_up(self, enable=True):
        """Note: calling this function resets also the Proximity and ALS
        interrupt settings."""
        value = 0b01001111 if enable else 0
        self.write_byte_data(value, APDS_9960.ENABLE_REG_ADDRESS)
        time.sleep(0.01)

    def set_sleep_after_interrupt(self, enable=True):
        """Sleep After Interrupt. When enabled, the device will automatically 
        enter low power mode when the INT pin is asserted. Normal operation is 
        resumed when INT pin is cleared over I2C.\n
        """
        self.write_flag_data([enable], APDS_9960.CONFIG_3_REG_ADDRESS, 4)

    def set_led_drive(self, led_drive):
        """LED drive strength.\n
        :led_drive: must be one of LED_DRIVE_N_mA.
        """
        if not (APDS_9960.LED_DRIVE_100_mA <= led_drive <= APDS_9960.LED_DRIVE_12_5_mA):
            raise ValueError("led_drive must be one of APDS_9960.LED_DRIVE_N_mA")

        self.write_flag_data([bool(led_drive & 0b01), bool(led_drive & 0b10)],
                             APDS_9960.CONTROL_1_REG_ADDRESS, 6)

    def set_led_boost(self, led_boost):
        """The LED_BOOST allows the LDR pin to sink more current above the 
        maximum setting. Additional LDR current during proximity and gesture 
        LED pulses. Current value, set by LDRIVE, is increased by the 
        percentage of LED_BOOST.\n
        :led_boost: must be one of LED_BOOST_N
        """
        if not (APDS_9960.LED_BOOST_100 <= led_boost <= APDS_9960.LED_BOOST_300):
            raise ValueError("led_boost must be one of APDS.LED_BOOST_N")

        self.write_flag_data([bool(led_boost & 0b01), bool(led_boost & 0b10)],
                             APDS_9960.CONFIG_2_REG_ADDRESS, 4)

    def get_status(self):
        "Returns a dictionary containing the status of the device."
        status = self.read_byte_data(APDS_9960.STATUS_REG_ADDRESS)
        status_dic = dict()
        status_dic["Clear Photodiode Saturation"] = bool(status & 0x80)
        status_dic["Proximity/Gesture Saturation"] = bool(status & 0x40)
        status_dic["Proximity Interrupt"] = bool(status & 0x20)
        status_dic["ALS Interrupt"] = bool(status & 0x10)
        status_dic["Gesture Interrupt"] = bool(status & 0x04)
        status_dic["Proximity Valid"] = bool(status & 0x02)
        status_dic["ALS Valid"] = bool(status & 0x01)
        return status_dic

    # =========================================================================
    #     Proximity Engine Methods
    # =========================================================================

    def enable_proximity_engine(self, enable=True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 2)

    def enable_proximity_interrupts(self, enable=True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 5)

    def enable_proximity_saturation_interrupts(self, enable=True):
        self.write_flag_data([enable], APDS_9960.CONFIG_2_REG_ADDRESS, 7)

    def clear_proximity_interrupts(self):
        # Interrupts are cleared by “address accessing” the appropriate register. This is special I2C transaction
        # consisting of only two bytes: chip address with R/W = 0, followed by a register address.
        with SMBusWrapper(self.i2c_bus) as bus:
            bus.write_byte(self.i2c_address, APDS_9960.PROXIMITY_INT_CLEAR_REG_ADDRESS)

    def set_proximity_gain(self, prox_gain):
        """Proximity Gain Control.\n
        :prox_gain: must be one of PROXIMITY_GAIN_NX.
        """
        if not (APDS_9960.PROXIMITY_GAIN_1X <= prox_gain <= APDS_9960.PROXIMITY_GAIN_8X):
            raise ValueError("prox_gain must be one of PROXIMITY_GAIN_NX.")

        self.write_flag_data([bool(prox_gain & 0b01), bool(prox_gain & 0b10)],
                             APDS_9960.CONTROL_1_REG_ADDRESS, 2)

    def set_proximity_interrupt_thresholds(self, low_thr, high_thr):
        """The Proximity Interrupt Threshold sets the high and low trigger points
        for the comparison function which generates an interrupt. If the value 
        generated by the proximity channel, crosses below the lower threshold 
        or above the higher threshold, an interrupt may be signaled to the host 
        processor. Interrupt generation is subject to the value set in 
        persistence.\n
        :low_thr: the low trigger point value.\n
        :high_thr: the high trigger point value. \n
        """
        self.write_byte_data(low_thr, APDS_9960.PROX_INT_LOW_THR_REG_ADDRESS)
        self.write_byte_data(high_thr, APDS_9960.PROX_INT_HIGH_THR_REG_ADDRESS)

    def set_proximity_interrupt_persistence(self, persistence):
        """The Interrupt Persistence sets a value which is compared with the 
        accumulated amount Proximity cycles in which results were outside 
        threshold values. Any Proximity result that is inside threshold values 
        resets the count.\n
        :persistence: int in range [0-15] \n
            0 : an interrupt is triggered every cycle.\n
            N > 0 : an interrupt is triggered after N results over the threshold.
        """
        if not (0 <= persistence <= 15):
            raise ValueError("persistance must be in range [0-15]")

        flag = []
        for i in range(4):
            flag.append(bool(persistence & (1 << i)))
        self.write_flag_data(flag, APDS_9960.INTERRUPT_PERSISTANCE_REG_ADDRESS, 4)

    def set_proximity_pulse_count_and_length(self, pulse_count,
                                             pulse_length=PULSE_LEN_8_MICROS):
        """The proximity pulse count is the number of pulses to be output on
        the LDR pin. The proximity pulse length is the amount of time the LDR 
        pin is sinking current during a proximity pulse.\n
        :pulse_count: must be in range [1-64]\n
        :pulse_length: must be one of APDS_9960.PULSE_LEN_N_MICROS.
        """
        if not (1 <= pulse_count <= 64):
            raise ValueError("pulse_count must be in range [1-64]")
        if not (APDS_9960.PULSE_LEN_4_MICROS <= pulse_length
                <= APDS_9960.PULSE_LEN_32_MICROS):
            raise ValueError("pulse_length must be one of APDS_9960.PULSE_LEN_N_MICROS")

        reg_value = pulse_length << 6
        reg_value |= pulse_count - 1
        self.write_byte_data(reg_value, APDS_9960.PROX_PULSE_COUNT_REG_ADDRESS)

    def set_proximity_offset(self, up_right_offset=0, down_left_offset=0):
        """In proximity mode, the UP and RIGHT and the DOWN and LEFT
        photodiodes are connected forming diode pairs. The offset is an 8-bit 
        value used to scale an internal offset correction factor to compensate 
        for crosstalk in the application.\n
        :up_right_offset: the up-right pair offset.\n
        :down_left_offset: the down-left pair offset.\n
        """
        if not (-127 <= up_right_offset <= 127 and -127 <= down_left_offset <= 127):
            raise ValueError("up_right_offset and down_left_offset must be in range [-127-127]")

        ur_reg_value = abs(up_right_offset)
        ur_reg_value |= 0x80 if up_right_offset < 0 else 0x00
        self.write_byte_data(ur_reg_value, APDS_9960.PROX_UP_RIGHT_OFFSET_REG_ADDRESS)
        dl_reg_value = abs(down_left_offset)
        dl_reg_value |= 0x80 if down_left_offset < 0 else 0x00
        self.write_byte_data(dl_reg_value, APDS_9960.PROX_DOWN_LEFT_OFFSET_REG_ADDRESS)

    def disable_photodiodes(self, mask_up, mask_down, mask_left, mask_right,
                            proximity_gain_compensation):
        """Select which photodiodes are used for proximity.\n
        :mask_up: if True disables the up photodiode.\n
        :mask_down: if True disables the down photodiode.\n
        :mask_left: if True disables the left photodiode.\n
        :mask_right: if True disables the right photodiode.\n
        :proximity_gain_compensation: provides gain compensation when proximity
            photodiode signal is reduced as a result of sensor masking. If only 
            one diode of the diode pair is contributing, then only half of the 
            signal is available at the ADC; this results in a maximum ADC value
            of 127. Enabling enables an additional gain of 2X, resulting in a 
            maximum ADC value of 255.
        """
        self.write_flag_data([mask_right, mask_left, mask_down, mask_up],
                             APDS_9960.CONFIG_3_REG_ADDRESS, 0)
        self.write_flag_data([proximity_gain_compensation],
                             APDS_9960.CONFIG_3_REG_ADDRESS, 5)

    def get_proximity_data(self):
        return self.read_byte_data(APDS_9960.PROX_DATA_REG_ADDRESS)

    # =========================================================================
    #     ALS Engine Methods
    # =========================================================================

    def enable_als_engine(self, enable=True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 1)

    def enable_als_interrupts(self, enable=True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 4)

    def enable_als_saturation_interrupts(self, enable=True):
        self.write_flag_data([enable], APDS_9960.CONFIG_2_REG_ADDRESS, 6)

    def clear_als_interrupts(self):
        # Interrupts are cleared by “address accessing” the appropriate register. This is special I2C transaction
        # consisting of only two bytes: chip address with R/W = 0, followed by a register address.
        with SMBusWrapper(self.i2c_bus) as bus:
            bus.write_byte(self.i2c_address, APDS_9960.ALS_INT_CLEAR_REG_ADDRESS)

    def set_als_gain(self, als_gain):
        """ALS and Color Gain Control.\n
        :als_gain: must be one of ALS_GAIN_NX.
        """
        if not (APDS_9960.ALS_GAIN_1X <= als_gain <= APDS_9960.ALS_GAIN_64X):
            raise ValueError("als_gain must be one of ALS_GAIN_NX.")

        self.write_flag_data([bool(als_gain & 0b01), bool(als_gain & 0b10)],
                             APDS_9960.CONTROL_1_REG_ADDRESS, 0)

    def set_als_thresholds(self, low_thr, high_thr):
        """ALS level detection uses data generated by the Clear Channel.
        The ALS Interrupt Threshold registers provide 16-bit values to be used 
        as the high and low thresholds for comparison to the 16-bit CDATA values.
        If AIEN is enabled and CDATA is greater than high_thr or less than
        low_thr for the number of consecutive samples specified in APERS
        an interrupt is asserted on the interrupt pin.\n
        :low_thr: the lower threshold value must be a 16 bit unsigned int\n
        :high_thr: the higher threshold value must be a 16 bit unsigned int
        """
        if not (0 <= low_thr <= 0xFFFF and 0 <= high_thr <= 0xFFFF):
            raise ValueError("low_thr and high_thr must be in range [0 - 0xFFFF]")

        ailtl = low_thr & 0xFF
        ailth = low_thr >> 8
        aihtl = high_thr & 0xFF
        aihth = high_thr >> 8
        self.write_byte_data([ailtl, ailth, aihtl, aihth], APDS_9960.ALS_INT_LOW_THR_LOW_BYTE_REG_ADDRESS)

    def set_als_interrupt_persistence(self, persistence):
        """The Interrupt Persistence sets a value which is compared with the 
        accumulated amount of ALS cycles in which results were outside threshold 
        values. Any Proximity or ALS result that is inside threshold values resets
        the count.\n
        :persistence: ALS Interrupt Persistence. Controls rate of Clear channel 
            interrupt to the host processor. Must be in range [0 - 15]:
                0 = Every ALS cycle\n
                1 = Any ALS value outside of threshold range\n
                2 = 2 consecutive ALS values out of range\n
                3 = 3 consecutive ALS values out of range\n
                N > 3 = (N - 3) * 5 consecutive ALS values out of range\n
        """
        if not (0 <= persistence <= 15):
            raise ValueError("Persistence must be in range [0 - 15]")

        flag = []
        for i in range(4):
            flag.append(bool(persistence & (1 << i)))
        self.write_flag_data(flag, APDS_9960.INTERRUPT_PERSISTANCE_REG_ADDRESS)

    def set_als_integration_time(self, wtime):
        """The ATIME register controls the internal integration time of 
        ALS/Color analog to digital converters. The maximum count (or saturation) 
        value can be retrieved with the get_saturation method.
        :wtime: the integration time in millis must be in range [2.78 - 712]
        """
        if not (2.78 <= wtime <= 712):
            raise ValueError("The integration time must be in range [2.78 - 712] millis.")

        value = 256 - int(wtime / 2.78)
        self.write_byte_data(value, APDS_9960.ALS_ATIME_REG_ADDRESS)

    def get_saturation(self):
        """Returns the saturation value. The values returned by get_color_data can not exceed
        this value."""
        cycles = 256 - self.read_byte_data(APDS_9960.ALS_ATIME_REG_ADDRESS)
        return min(65535, cycles * 1025)

    def get_color_data(self):
        """Red, green, blue, and clear data is stored as 16-bit values.\n
        Returns : The data is returned as 4 element list: [clear, red, green, blue]. 
        """
        color = []
        data = self.read_byte_data(APDS_9960.CLEAR_DATA_LOW_BYTE_REG_ADDRESS, 8)
        for i in range(4):
            channel_low = data[2 * i]
            channel_high = data[2 * i + 1]
            color.append((channel_high << 8) | channel_low)
        return color

    # =========================================================================
    #     Gestures Engine Methods
    # =========================================================================

    def enable_gestures_engine(self, enable=True):
        self.enable_proximity_engine()
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 6)

    def enter_immediately_gesture_engine(self):
        """Causes immediate entry in to the gesture state machine.
        (Sets GMODE bit to 1)."""
        self.write_flag_data([True], APDS_9960.GESTURE_CONFIG_4_REG_ADDRESS, 0)

    def exit_gesture_engine(self):
        """Causes exit of gesture when current analog conversion has finished.
        (Sets GMODE bit to 0)."""
        self.write_flag_data([False], APDS_9960.GESTURE_CONFIG_4_REG_ADDRESS, 0)

    def set_gesture_prox_enter_threshold(self, enter_thr):
        """The Gesture Proximity Enter Threshold Register value is compared 
        with Proximity value, to determine if the gesture state machine is 
        entered. The proximity persistence filter, is not used to determine 
        gesture state machine entry.\n
        :enter_thr: the enter threshold value must be an 8-bit unsigned int
        """
        if not (0 <= enter_thr <= 0xFF):
            raise ValueError("enter_thr must be in range [0-0xFF]")

        self.write_byte_data(enter_thr, APDS_9960.GESTURE_PROX_ENTER_THR_REG_ADDRESS)

    def set_gesture_exit_threshold(self, exit_thr):
        """The Gesture Proximity Exit Threshold value compares all non-masked 
        gesture detection photodiodes (UDLR). Gesture state machine exit is 
        also governed by the Gesture Exit Persistence value.\n
        :exit_thr: Gesture Exit Threshold. The value used to determine a 
            “gesture end” and subsequent exit of the gesture state machine.
        """
        if not (0 <= exit_thr <= 0xFF):
            raise ValueError("exit_thr must be in range [0-0xFF]")

        self.write_byte_data(exit_thr, APDS_9960.GESTURE_EXIT_THR_REG_ADDRESS)

    def set_gesture_exit_mask(self, mask_up, mask_down, mask_left, mask_right):
        """Gesture Exit Mask. Controls which of the gesture detector photodiodes
        (UDLR) will be included to determine a “gesture end” and subsequent 
        exit of the gesture state machine. Unmasked UDLR data will be compared 
        with the value in GTHR_OUT.\n
        :mask_up: if True do not include up photodiode in sum.\n
        :mask_down: if True do not include down photodiode in sum.\n
        :mask_left: if True do not include left photodiode in sum.\n
        :mask_right: if True do not include right photodiode in sum.\n
        """
        self.write_flag_data([mask_right, mask_left, mask_down, mask_up],
                             APDS_9960.GESTURE_CONFIG_1_REG_ADDRESS, 2)

    def set_gesture_exit_persistence(self, persistence):
        """Gesture Exit Persistence. When a number of consecutive “gesture end”
        occurrences become equal or greater to the persistence value, the 
        Gesture state machine is exited.\n
        :persistence: must be one of EXIT_AFTER_N_GESTURE_END.
        """
        if not (APDS_9960.EXIT_AFTER_1_GESTURE_END <= persistence
                <= APDS_9960.EXIT_AFTER_7_GESTURE_END):
            raise ValueError("persistence must be one of EXIT_AFTER_N_GESTURE_END.")

        flag = [bool(persistence & 0b01), bool(persistence & 0b10)]
        self.write_flag_data(flag, APDS_9960.GESTURE_CONFIG_1_REG_ADDRESS, 0)

    def set_gesture_gain(self, gesture_gain):
        """Gesture Gain Control. Sets the gain of the proximity receiver in 
        gesture mode.\n
        :gesture_gain: must be one of PROXIMITY_GAIN_NX.
        """
        if not (APDS_9960.PROXIMITY_GAIN_1X <= gesture_gain <= APDS_9960.PROXIMITY_GAIN_8X):
            raise ValueError("gesture_gain must be one of PROXIMITY_GAIN_NX.")

        self.write_flag_data([bool(gesture_gain & 0b01), bool(gesture_gain & 0b10)],
                             APDS_9960.GESTURE_CONFIG_2_REG_ADDRESS, 5)

    def set_gesture_led_drive(self, led_drive):
        """Gesture LED Drive Strength. Sets LED Drive Strength in gesture mode.\n
        :led_drive: must be one of LED_DRIVE_N_mA.
        """
        if not (APDS_9960.LED_DRIVE_100_mA <= led_drive <= APDS_9960.LED_DRIVE_12_5_mA):
            raise ValueError("led_drive must be one of APDS_9960.LED_DRIVE_N_mA")

        self.write_flag_data([bool(led_drive & 0b01), bool(led_drive & 0b10)],
                             APDS_9960.GESTURE_CONFIG_2_REG_ADDRESS, 3)

    def set_gesture_wait_time(self, wait_time):
        """Gesture Wait Time. The wait time controls the amount of time in a 
        low power mode between gesture detection cycles.\n
        :wait_time: must be one of GESTURE_WAIT_N_MILLIS.
        """
        if not (APDS_9960.GESTURE_WAIT_0_MILLIS <= wait_time
                <= APDS_9960.GESTURE_WAIT_39_2_MILLIS):
            raise ValueError("wait_time must be one of GESTURE_WAIT_N_MILLIS.")

        flag = [bool(wait_time & 0b001), bool(wait_time & 0b010), bool(wait_time & 0b100)]
        self.write_flag_data(flag, APDS_9960.GESTURE_CONFIG_2_REG_ADDRESS, 0)

    def set_gesture_offsets(self, up_offset, down_offset, left_offset, right_offset):
        """The offsets are used to scale an internal offset correction factor 
        to compensate for crosstalk in the application.\n
        :up_offset: must be in range [-127-127].\n
        :down_offset: must be in range [-127-127].\n
        :left_offset: must be in range [-127-127].\n
        :right_offset: must be in range [-127-127].\n
        """
        offsets = [up_offset, down_offset, left_offset, right_offset]
        if not all(map(lambda x: -127 <= x <= 127), offsets):
            raise ValueError("All offset must be in range [-127-127]")

        for i, offset in enumerate(offsets):
            reg_value = abs(offset)
            reg_value |= 0x80 if offset < 0 else 0
            self.write_byte_data(reg_value, APDS_9960.GESTURE_OFFSET_REG_ADDRESSES[i])

    def set_gesture_pulse_count_and_length(self, pulse_count, pulse_length):
        """The Gesture pulse count sets the number of pulses to be output on 
        the LDR pin. The Gesture Length sets the amount of time the LDR pin is 
        sinking current during a gesture pulse.\n
        :pulse_count: must be in range [1-64].\n
        :pulse_length: must be one of PULSE_LEN_N_MICROS.
        """
        if not (1 <= pulse_count <= 64):
            raise ValueError("pulse_count must be in range [1-64].")
        if not (APDS_9960.PULSE_LEN_4_MICROS <= pulse_length
                <= APDS_9960.PULSE_LEN_32_MICROS):
            raise ValueError("pulse_length must be one of PULSE_LEN_N_MICROS.")

        reg_value = (pulse_count - 1) | (pulse_length << 6)
        self.write_byte_data(reg_value, APDS_9960.GESTURE_PULSE_COUNT_AND_LEN_REG_ADDRESS)

    def set_active_photodiodes_pairs(self, up_down_active=True, right_left_active=True):
        """Which gesture photodiode pair: UP-DOWN and/or RIGHT-LEFT will be 
        enabled (have valid data in FIFO) while the gesture state machine is 
        collecting directional data. Allows the enabled pair to collect data 
        twice as fast. Data stored in the FIFO for a disabled pair is not valid.
        This feature is useful to improve reliability and accuracy of gesture 
        detection when only one-dimensional gestures are expected.\n
        :up_down_active = True:\n
        :right_left_active = True:
        """
        self.write_flag_data([up_down_active, right_left_active],
                             APDS_9960.GESTURE_CONFIG_3_REG_ADDRESS, 0)

    def enable_gesture_interrupts(self, enable_interrupts=True):
        """Enables or disables all gesture engine related interrupts."""
        self.write_flag_data([enable_interrupts], APDS_9960.GESTURE_CONFIG_4_REG_ADDRESS, 1)

    def set_gesture_fifo_threshold(self, fifo_thr):
        """Gesture FIFO Threshold. This value is compared with the FIFO Level
        (i.e. the number of UDLR datasets) to generate an interrupt
        (if enabled).\n
        :fifo_thr: must be one of FIFO_INT_AFTER_N_DATASET(S).
        """
        if not (APDS_9960.FIFO_INT_AFTER_1_DATASET <= fifo_thr
                <= APDS_9960.FIFO_INT_AFTER_16_DATASETS):
            raise ValueError("fifo_thr must be one of FIFO_INT_AFTER_N_DATASET(S)")

        flag = [bool(fifo_thr & 0b01), bool(fifo_thr & 0b10)]
        self.write_flag_data(flag, APDS_9960.GESTURE_CONFIG_1_REG_ADDRESS, 6)

    def reset_gesture_engine_interrupt_settings(self):
        """Clears GFIFO, GINT, GVALID, GFIFO_OV and GFIFO_LVL."""
        self.write_flag_data([True], APDS_9960.GESTURE_CONFIG_4_REG_ADDRESS, 2)

    def is_gesture_engine_running(self):
        return bool(self.read_byte_data(APDS_9960.GESTURE_CONFIG_4_REG_ADDRESS) & 0x01)

    def get_number_of_datasets_in_fifo(self):
        """Returns how many four byte data points - UDLR are ready for read 
        over I2C. One four-byte dataset is equivalent to a single count."""
        return self.read_byte_data(APDS_9960.GESTURE_FIFO_LEVEL_REG_ADDRESS)

    def get_gesture_status(self):
        """Returns a dictionary containing data about the gesture engine status."""
        status_dict = dict()
        status = self.read_byte_data(APDS_9960.GESTURE_STATUS_REG_ADDRESS)
        status_dict["Gesture FIFO Overflow"] = bool(status & 0x02)
        status_dict["Gesture FIFO Data"] = bool(status & 0x01)
        return status_dict

    def get_gesture_data(self):
        """Returns a dataset (list) containing one integration cycle of UP, 
        DOWN, LEFT & RIGHT gesture data. The amount of valid data can be retrieved 
        with the get_number_of_datasets_in_fifo method."""
        return self.read_byte_data(APDS_9960.GESTURE_FIFO_UP_REG_ADDRESS, 4)

    # =========================================================================
    #     Wait Engine Methods
    # =========================================================================

    def enable_wait_engine(self, enable=True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 3)

    def set_wait_time(self, wtime, long_wait=False):
        """Sets the wait time in WTIME register. This is the time that will pass
        between two cycles.The wait time should be configured before the proximity 
        and the als engines get enabled.\n
        :wtime: the time value in millisenconds. Must be between 2.78ms and 712ms\n
        :long_wait = False: If true the wait time is multiplied by 12.\n
        """
        if not (2.78 <= wtime <= 712):
            raise ValueError("The wait time must be between 2.78 ms and 712 ms")

        # long_wait
        self.write_flag_data([long_wait], APDS_9960.CONFIG_1_REG_ADDRESS, 1)
        # wtime
        reg_value = 256 - int(wtime / 2.78)
        self.write_byte_data(reg_value, APDS_9960.WAIT_TIME_REG_ADDRESS)

