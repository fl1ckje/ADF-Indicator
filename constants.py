def init():
    global PRIMARY_WIN_TAG
    PRIMARY_WIN_TAG = 'primary-win'

    global ALERT_WIN_TAG
    ALERT_WIN_TAG = 'alert-win'

    global ALERT_TXT_TAG
    ALERT_TXT_TAG = 'alert-txt'

    global SERIAL_COMBO_TAG
    SERIAL_COMBO_TAG = 'serial-combo'

    global SWITCH_RX_BTN_TAG
    SWITCH_RX_BTN_TAG = 'rx-btn'

    global DIR_ARROW_TAG
    DIR_ARROW_TAG = 'dir-arrow'

    global DEGREES
    DEGREES = {
        '0': [-5, -175],
        '60': [135, -95],
        '120': [135, 75],
        '180': [-15, 155],
        '240': [-165, 75],
        '300': [-165, -95]
    }

    global NONE_STR
    NONE_STR = 'None'

    global BAUDRATE
    BAUDRATE = 9600
