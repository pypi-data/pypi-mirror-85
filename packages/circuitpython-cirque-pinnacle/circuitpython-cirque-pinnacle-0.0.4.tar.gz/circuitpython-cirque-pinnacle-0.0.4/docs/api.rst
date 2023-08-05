
.. currentmodule:: circuitpython_cirque_pinnacle

About the lite version
======================

This library includes a "lite" version of the module ``glidepoint.py`` titled ``glidepoint_lite.py``.
The lite version is limited to only Relative and Absolute data modes. It has been developed to
save space on microcontrollers with limited amount of RAM and/or storage (like boards using the
ATSAMD21 M0). The following functionality has been removed from the lite version:

   * `anymeas_mode_config()`
   * `measure_adc()`
   * `detect_finger_stylus()`
   * `calibrate()`
   * `calibration_matrix`
   * `set_adc_gain()`
   * `tune_edge_sensitivity()`
   * ``_era_write_bytes()`` (private member for accessing the Pinnacle ASIC's memory)
   * all comments and docstrings (meaning ``help()`` will provide no specific information)

PinnacleTouch API
==================

Accepted Constants
------------------

Data Modes
***********
   Allowed symbols for configuring the Pinanacle ASIC's data reporting/measurements.

   .. data:: circuitpython_cirque_pinnacle.glidepoint.RELATIVE
      :annotation: =0

      Alias symbol for specifying Relative mode (AKA Mouse mode).

   .. data:: circuitpython_cirque_pinnacle.glidepoint.ANYMEAS
      :annotation: =1

      Alias symbol for specifying "AnyMeas" mode (raw ADC measurement)

   .. data:: circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE
      :annotation: =2

      Alias symbol for specifying Absolute mode (axis positions)

AnyMeas mode Gain
******************

   Allowed ADC gain configurations of AnyMeas mode. The percentages defined here are approximate
   values.

   .. data:: circuitpython_cirque_pinnacle.glidepoint.GAIN_100

      around 100% gain

   .. data:: circuitpython_cirque_pinnacle.glidepoint.GAIN_133

      around 133% gain

   .. data:: circuitpython_cirque_pinnacle.glidepoint.GAIN_166

      around 166% gain

   .. data:: circuitpython_cirque_pinnacle.glidepoint.GAIN_200

      around 200% gain


AnyMeas mode Frequencies
************************

   Allowed frequency configurations of AnyMeas mode. The frequencies defined here are
   approximated based on an aperture width of 500 nanoseconds. If the ``aperture_width``
   parameter to `anymeas_mode_config()` specified is less than 500 nanoseconds, then the
   frequency will be larger than what is described here (& vice versa).

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_0

      frequency around 500,000Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_1

      frequency around 444,444Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_2

      frequency around 400,000Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_3

      frequency around 363,636Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_4

      frequency around 333,333Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_5

      frequency around 307,692Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_6

      frequency around 267,000Hz

   .. data:: circuitpython_cirque_pinnacle.glidepoint.FREQ_7

      frequency around 235,000Hz


AnyMeas mode Muxing
*******************

   Allowed muxing gate polarity and reference capacitor configurations of AnyMeas mode.
   Combining these values (with ``+`` operator) is allowed.

   .. note:: The sign of the measurements taken in AnyMeas mode is inverted depending on which
      muxing gate is specified (when specifying an individual gate polarity).

   .. data:: circuitpython_cirque_pinnacle.glidepoint.MUX_REF1

      enables a builtin capacitor (~0.5pF). See note in `measure_adc()`

   .. data:: circuitpython_cirque_pinnacle.glidepoint.MUX_REF0

      enables a builtin capacitor (~0.25pF). See note in `measure_adc()`

   .. data:: circuitpython_cirque_pinnacle.glidepoint.MUX_PNP

      enable PNP sense line

   .. data:: circuitpython_cirque_pinnacle.glidepoint.MUX_NPN

      enable NPN sense line


AnyMeas mode Control
********************

   These constants control the number of measurements performed in `measure_adc()`.
   The number of measurements can range [0, 63].

   .. data:: circuitpython_cirque_pinnacle.glidepoint.CRTL_REPEAT

      required for more than 1 measurement

   .. data:: circuitpython_cirque_pinnacle.glidepoint.CRTL_PWR_IDLE

      triggers low power mode (sleep) after completing measurements


PinnacleTouch
-------------

.. |dr_pin_parameter| replace:: The input pin connected to the Pinnacle ASIC's "Data
      Ready" pin. If this parameter is not specified, then the SW_DR (software data ready) flag
      of the STATUS register is used to detirmine if the data being reported is new.

.. |dr_pin_note| replace:: This parameter must be specified if your application is going to use the
      Pinnacle ASIC's :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`
      mode (a rather experimental measuring of raw ADC values).


Constructor
*************************

   .. autoclass:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch
      :no-members:

      :param ~microcontroller.Pin dr_pin: |dr_pin_parameter|

         .. important:: |dr_pin_note|

data_mode
*************************

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.data_mode

      Valid input values are :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE` for
      relative/mouse mode, :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE` for
      absolute positioning mode, or :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`
      (referred to as "AnyMeas" in specification sheets) mode for reading ADC values.

      :Returns:

         - ``0`` for Relative mode (AKA mouse mode)
         - ``1`` for AnyMeas mode (raw ADC measurements)
         - ``2`` for Absolute mode (X & Y axis positions)

      .. important:: When switching from :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS` to
         :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE` or
         :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE` all configurations are reset, and
         must be re-configured by using  `absolute_mode_config()` or `relative_mode_config()`.

Relative or Absolute mode
*************************

feed_enable
^^^^^^^^^^^^^^^^^^^^^^^

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.feed_enable

      This function only applies to :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE`
      or :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE` mode, otherwise if `data_mode` is set to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`, then this function will do nothing.

hard_configured
^^^^^^^^^^^^^^^^^^^^^^^

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.hard_configured

      See note about product labeling in `Model Labeling Scheme <index.html#cc>`_. (read only)

      :Returns:
         `True` if a 470K ohm resistor is populated at the junction labeled "R4"

relative_mode_config()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.relative_mode_config

      (write only)

      This function only applies to :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE`
      mode, otherwise if `data_mode` is set to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS` or
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE`, then this function does nothing.

      :param bool rotate90: Specifies if the axis data is altered for 90 degree rotation before
         reporting it (essentially swaps the axis data). Default is `False`.
      :param bool taps: Specifies if all taps should be reported (`True`) or not
         (`False`). Default is `True`. This affects ``secondary_tap`` option as well.
      :param bool secondary_tap: Specifies if tapping in the top-left corner (depending on
         orientation) triggers the secondary button data. Defaults to `True`. This feature is
         always disabled if `hard_configured` is `True`.
      :param bool glide_extend: A patended feature that allows the user to glide their finger off
         the edge of the sensor and continue gesture with the touch event. Default is `True`.
         This feature is always disabled if `hard_configured` is `True`.
      :param bool intellimouse: Specifies if the data reported includes a byte about scroll data.
         Default is `False`. Because this flag is specific to scroll data, this feature is always
         disabled if `hard_configured` is `True`.

absolute_mode_config()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.absolute_mode_config

      (write only)

      This function only applies to :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE`
      mode, otherwise if `data_mode` is set to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS` or
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE`, then this function does nothing.

      :param int z_idle_count: Specifies the number of empty packets (x-axis, y-axis, and z-axis
         are ``0``) reported (every 10 milliseconds) when there is no touch detected. Defaults
         to 30. This number is clamped to range [0, 255].
      :param bool invert_x: Specifies if the x-axis data is to be inverted before reporting it.
         Default is `False`.
      :param bool invert_y: Specifies if the y-axis data is to be inverted before reporting it.
         Default is `False`.

report()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.report

      This function only applies to :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE`
      or :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE` mode, otherwise if `data_mode` is set to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`, then this function returns `None` and does nothing.

      :param bool only_new: This parameter can be used to ensure the data reported is only new
         data. Otherwise the data returned can be either old data or new data. If the ``dr_pin``
         parameter is specified upon instantiation, then the specified input pin is used to
         detect if the data is new. Otherwise the SW_DR flag in the STATUS register is used to
         detirmine if the data is new.

      :Returns: `None` if  the ``only_new`` parameter is set `True` and there is no new data to
         report. Otherwise, a `list` or `bytearray` of parameters that describe the (touch or
         button) event. The structure is as follows:

         .. list-table::
               :header-rows: 1
               :widths: 1, 5, 5

               * - Index
                 - Relative (Mouse) mode

                   as a `bytearray`
                 - Absolute Mode

                   as a `list`
               * - 0
                 - Button Data [1]_

                   one unsigned byte
                 - Button Data [1]_

                   one unsigned byte
               * - 1
                 - change in x-axis [2]_

                   -128 |LessEq| X |LessEq| 127
                 - x-axis Position

                   0 |LessEq| X |LessEq| 2047
               * - 2
                 - change in y-axis [2]_

                   -128 |LessEq| Y |LessEq| 127
                 - y-axis Position

                   0 |LessEq| Y |LessEq| 1535
               * - 3
                 - change in scroll wheel

                   -128 |LessEq| SCROLL |LessEq| 127 [3]_
                 - z-axis Magnitude

      .. [1] The returned button data is a byte in which each bit represents a button.
         The bit to button order is as follows:

            0. [LSB] Button 1 (thought of as Left button in Relative/Mouse mode). If ``taps``
               parameter is passed as `True` when calling `relative_mode_config()`, a single
               tap will be reflected here.
            1. Button 2 (thought of as Right button in Relative/Mouse mode). If ``taps`` and
               ``secondary_tap`` parameters are passed as `True` when calling `relative_mode_config()`,
               a single tap in the perspective top-left-most corner will be reflected here (secondary
               taps are constantly disabled if `hard_configured` returns `True`). Note that the
               top-left-most corner can be perspectively moved if ``rotate90`` parameter is passed as
               `True` when calling `relative_mode_config()`.
            2. Button 3 (thought of as Middle or scroll wheel button in Relative/Mouse mode)
      .. [2] The axis data reported in Relative/Mouse mode is in two's
         comliment form. Use Python's :py:func:`struct.unpack()` to convert the
         data into integer form (see `Simple Test example <examples.html#simple-test>`_
         for how to use this function).

         The axis data reported in Absolute mode is always positive as the
         xy-plane's origin is located to the top-left, unless ``invert_x`` or ``invert_y``
         parameters to `absolute_mode_config()` are manipulated to change the perspective
         location of the origin.
      .. [3] In Relative/Mouse mode the scroll wheel data is only reported if the
         ``intellimouse`` parameter is passed as `True` to `relative_mode_config()`.
         Otherwise this is an empty byte as the
         returned `bytearray` follows the buffer structure of a mouse HID report (see
         `USB Mouse example <examples.html#usb-mouse-example>`_).
      .. |LessEq| unicode:: U+2264

clear_flags()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.clear_flags

allow_sleep
^^^^^^^^^^^^^^^^^^^^^^^

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.allow_sleep

      Set this attribute to `True` if you want the Pinnacle ASIC to enter sleep (low power)
      mode after about 5 seconds of inactivity (does not apply to AnyMeas mode). While the touch
      controller is in sleep mode, if a touch event or button press is detected, the Pinnacle
      ASIC will take about 300 milliseconds to wake up (does not include handling the touch event
      or button press data).

shutdown
^^^^^^^^^^^^^^^^^^^^^^^

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.shutdown

      `True` means powered down (AKA standby mode), and `False` means not powered down
      (Active, Idle, or Sleep mode).

      .. note:: The ASIC will take about 300 milliseconds to complete the transition
         from powered down mode to active mode. No touch events or button presses will be
         monitored while powered down.

sample_rate
^^^^^^^^^^^^^^^^^^^^^^^

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.sample_rate

      Valid values are ``100``, ``80``, ``60``, ``40``, ``20``, ``10``. Any other input values
      automatically set the sample rate to 100 sps (samples per second). Optionally, ``200`` and
      ``300`` sps can be specified, but using these values automatically disables palm (referred
      to as "NERD" in the specification sheet) and noise compensations. These higher values are
      meant for using a stylus with a 2mm diameter tip, while the values less than 200 are meant
      for a finger or stylus with a 5.25mm diameter tip.

      This function only applies to :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE`
      or :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE` mode, otherwise if `data_mode` is set to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`, then this function will do nothing.

detect_finger_stylus()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.detect_finger_stylus

      :param bool enable_finger: `True` enables the Pinnacle ASIC's measurements to
         detect if the touch event was caused by a finger or 5.25mm stylus. `False` disables
         this feature. Default is `True`.
      :param bool enable_stylus: `True` enables the Pinnacle ASIC's measurements to
         detect if the touch event was caused by a 2mm stylus. `False` disables this
         feature. Default is `True`.
      :param int sample_rate: See the `sample_rate` attribute as this parameter manipulates that
         attribute.

      .. tip:: Consider adjusting the ADC matrix's gain to enhance performance/results using
         `set_adc_gain()`

calibrate()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.calibrate

      This function only applies to :attr:`~circuitpython_cirque_pinnacle.glidepoint.RELATIVE`
      or :attr:`~circuitpython_cirque_pinnacle.glidepoint.ABSOLUTE` mode, otherwise if `data_mode` is set to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`, then this function will do nothing.

      :param bool run: If `True`, this function forces a calibration of the sensor. If `False`,
         this function just writes the following parameters to the Pinnacle ASIC's "CalConfig1"
         register. This parameter is required while the rest are optional keyword parameters.
      :param bool tap: Enable dynamic tap compensation? Default is `True`.
      :param bool track_error: Enable dynamic track error compensation? Default is `True`.
      :param bool nerd: Enable dynamic NERD compensation? Default is `True`. This parameter has
         something to do with palm detection/compensation.
      :param bool background: Enable dynamic background compensation? Default is `True`.

      .. note:: According to the datasheet, calibration of the sensor takes about 100
         milliseconds. This function will block until calibration is complete (if ``run`` is
         `True`). It is recommended for typical applications to leave all optional parameters
         in their default states.

calibration_matrix
^^^^^^^^^^^^^^^^^^^^^^^

   .. autoattribute:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.calibration_matrix

      This matrix is not applicable in AnyMeas mode. Use this attribute to compare a prior
      compensation matrix with a new matrix that was either loaded manually by setting this
      attribute to a `list` of 46 signed 16-bit (short) integers or created internally by calling
      `calibrate()` with the ``run`` parameter as `True`.

      .. note:: A paraphrased note from Cirque's Application Note on Comparing compensation
         matrices:

         If any 16-bit values are above 20K (absolute), it generally indicates a problem with
         the sensor. If no values exceed 20K, proceed with the data comparison. Compare each
         16-bit value in one matrix to the corresponding 16-bit value in the other matrix. If
         the difference between the two values is greater than 500 (absolute), it indicates a
         change in the environment. Either an object was on the sensor during calibration, or
         the surrounding conditions (temperature, humidity, or noise level) have changed. One
         strategy is to force another calibration and compare again, if the values continue to
         differ by 500, determine whether to use the new data or a previous set of stored data.
         Another strategy is to average any two values that differ by more than 500 and write
         this new matrix, with the average values, back into Pinnacle ASIC.

set_adc_gain()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.set_adc_gain

      (does not apply to AnyMeas mode). (write-only)

      :param int sensitivity: This int specifies how sensitive the ADC (Analog to Digital
         Converter) component is. ``0`` means most sensitive, and ``3`` means least sensitive.
         A value outside this range will raise a `ValueError` exception.

      .. tip:: The official example code from Cirque for a curved overlay uses a value of ``1``.

tune_edge_sensitivity()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.tune_edge_sensitivity

      This function was ported from Cirque's example code and doesn't seem to have corresponding
      documentation. I'm having trouble finding a memory map of the Pinnacle ASIC as this
      function directly alters values in the Pinnacle ASIC's memory. USE AT YOUR OWN RISK!

AnyMeas mode
*************

anymeas_mode_config()
^^^^^^^^^^^^^^^^^^^^^^^
   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.anymeas_mode_config

      Be sure to set the `data_mode` attribute to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS` before calling this function
      otherwise it will do nothing.

      :param int gain: Sets the sensitivity of the ADC matrix. Valid values are the constants
         defined in `AnyMeas mode Gain`_. Defaults to
         :attr:`~circuitpython_cirque_pinnacle.glidepoint.GAIN_200`.
      :param int frequency: Sets the frequency of measurements made by the ADC matrix. Valid
         values are the constants defined in
         `AnyMeas mode Frequencies`_.
         Defaults :attr:`~circuitpython_cirque_pinnacle.glidepoint.FREQ_0`.
      :param int sample_length: Sets the maximum bit length of the measurements made by the ADC
         matrix. Valid values are ``128``, ``256``, or ``512``. Defaults to ``512``.
      :param int mux_ctrl: The Pinnacle ASIC can employ different bipolar junctions
         and/or reference capacitors. Valid values are the constants defined in
         `AnyMeas mode Muxing`_. Additional combination of
         these constants is also allowed. Defaults to
         :attr:`~circuitpython_cirque_pinnacle.glidepoint.MUX_PNP`.
      :param int apperture_width: Sets the window of time (in nanoseconds) to allow for the ADC
         to take a measurement. Valid values are multiples of 125 in range [``250``, ``1875``].
         Erroneous values are clamped/truncated to this range.

         .. note:: The ``apperture_width`` parameter has a inverse relationship/affect on the
               ``frequency`` parameter. The approximated frequencies described in this
               documentation are based on an aperture width of 500 nanoseconds, and they will
               shrink as the apperture width grows or grow as the aperture width shrinks.

      :param int ctrl_pwr_cnt: Configure the Pinnacle to perform a number of measurements for
         each call to `measure_adc()`. Defaults to 1. Constants defined in
         `AnyMeas mode Control`_ can be used to specify if is sleep
         is allowed (:attr:`~circuitpython_cirque_pinnacle.glidepoint.CRTL_PWR_IDLE` -- this
         is not default) or if repetive measurements is allowed (
         :attr:`~circuitpython_cirque_pinnacle.glidepoint.CRTL_REPEAT`) if number of
         measurements is more than 1.

         .. warning:: There is no bounds checking on the number of measurements specified
               here. Specifying more than 63 will trigger sleep mode after performing
               measuements.

         .. tip:: Be aware that allowing the Pinnacle to enter sleep mode after taking
               measurements will slow consecutive calls to `measure_adc()` as the Pinnacle
               requires about 300 milliseconds to wake up.

measure_adc()
^^^^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.measure_adc

      Internally this function calls `start_measure_adc()` and `get_measure_adc()` in sequence.
      Be sure to set the `data_mode` attribute to
      :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS` before calling this function
      otherwise it will do nothing.

      :parameters:
         Each of the parameters are a 4-byte integer (see format table below) in which each bit
         corresponds to a capacitance sensing eletrode in the sensor's matrix (12 electrodes for
         Y-axis, 16 electrodes for X-axis). They are used to compensate for varying capacitances in
         the electrodes during measurements. **It is highly recommended that the trackpad be
         installed in a finished/prototyped housing when determining what electrodes to
         manipulate.** See `AnyMeas mode example <examples.html#anymeas-mode-example>`_ to
         understand how to use these 4-byte integers.

         * bits_to_toggle (`int <https://docs.python.org/3.7/library/functions.html#int>`_) - A bit
           of ``1`` flags that electrode's ouput for toggling, and a bit of ``0`` signifies that
           the electrode's output should remain unaffected.
         * toggle_polarity (`int <https://docs.python.org/3.7/library/functions.html#int>`_) - This
           specifies which polarity the output of the electrode(s) (specified with corresponding
           bits in ``bits_to_toggle`` parameter) should be toggled (forced). A bit of ``1`` toggles
           that bit positve, and a bit of ``0`` toggles that bit negative.

      :Returns:
         A 2-byte `bytearray` that represents a signed short integer. If `data_mode` is not set
         to :attr:`~circuitpython_cirque_pinnacle.glidepoint.ANYMEAS`, then this function returns
         `None` and does nothing.

      :4-byte Integer Format:
         Bits 31 & 30 are not used and should remain ``0``. Bits 29 and 28 represent the optional
         implementation of reference capacitors built into the Pinnacle ASIC. To use these
         capacitors, the corresponding constants
         (:attr:`~circuitpython_cirque_pinnacle.glidepoint.AnyMeasMux.MUX_REF0` and/or
         :attr:`~circuitpython_cirque_pinnacle.glidepoint.AnyMeasMux.MUX_REF1`) must be passed to
         `anymeas_mode_config()` in the ``mux_ctrl`` parameter, and their representative
         bits must be flagged in both ``bits_to_toggle`` & ``toggle_polarity`` parameters.

         .. csv-table:: byte 3 (MSByte)
               :stub-columns: 1
               :widths: 10, 5, 5, 5, 5, 5, 5, 5, 5

               "bit position",31,30,29,28,27,26,25,24
               "representation",N/A,N/A,Ref1,Ref0,Y11,Y10,Y9,Y8
         .. csv-table:: byte 2
               :stub-columns: 1
               :widths: 10, 5, 5, 5, 5, 5, 5, 5, 5

               "bit position",23,22,21,20,19,18,17,16
               "representation",Y7,Y6,Y5,Y4,Y3,Y2,Y1,Y0
         .. csv-table:: byte 1
               :stub-columns: 1
               :widths: 10, 5, 5, 5, 5, 5, 5, 5, 5

               "bit position",15,14,13,12,11,10,9,8
               "representation",X15,X14,X13,X12,X11,X10,X9,X8
         .. csv-table:: byte 0 (LSByte)
               :stub-columns: 1
               :widths: 10, 5, 5, 5, 5, 5, 5, 5, 5

               "bit position",7,6,5,4,3,2,1,0
               "representation",X7,X6,X5,X4,X3,X2,X1,X0

start_measure_adc()
^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.start_measure_adc

      See the parameters and table in `measure_adc()` as this is its helper function, and all
      parameters there are used the same way here.

get_measure_adc()
^^^^^^^^^^^^^^^^^^^^

   .. automethod:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouch.get_measure_adc

      This function is only meant ot be used in conjunction with `start_measure_adc()` for
      non-blocking application.

      :returns:
         * `None` if `data_mode` is not set to `ANYMEAS` or if the "data ready" pin's signal is not
           active (while `data_mode` is set to `ANYMEAS`) meaing the Pinnacle ASIC is still computing
           the ADC measurements based on the 4-byte polynomials passed to `start_measure_adc()`.
         * a `bytearray` that represents a signed 16-bit integer upon completed ADC measurements based
           on the 4-byte polynomials passed to `start_measure_adc()`.


SPI & I2C Interfaces
********************

   .. autoclass:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouchSPI
      :members:
      :show-inheritance:

      :param ~busio.SPI spi: The object of the SPI bus to use. This object must be shared among
         other driver classes that use the same SPI bus (MOSI, MISO, & SCK pins).
      :param ~microcontroller.Pin ss_pin: The "slave select" pin output to the Pinnacle ASIC.
      :param int spi_frequency: The SPI bus speed in Hz. Default is 12 MHz.
      :param ~microcontroller.Pin dr_pin: |dr_pin_parameter|

         .. important:: |dr_pin_note|

   .. autoclass:: circuitpython_cirque_pinnacle.glidepoint.PinnacleTouchI2C
      :members:
      :show-inheritance:


      :param ~busio.I2C i2c: The object of the I2C bus to use. This object must be shared among
         other driver classes that use the same I2C bus (SDA & SCL pins).
      :param int address: The slave I2C address of the Pinnacle ASIC. Defaults to ``0x2A``.
      :param ~microcontroller.Pin dr_pin: |dr_pin_parameter|

         .. important:: |dr_pin_note|
