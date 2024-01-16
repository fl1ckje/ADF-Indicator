import math
import sys
import glob
from serial import Serial, SerialException
from dearpygui import dearpygui as dpg
import threading
import trio
import constants
import data

constants.init()
data.init()


class ArduinoRxThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        trio.run(self.rx)

    async def rx(self):
        while data.rx_is_on:
            try:
                data.rx_data = await self.arduino_readline()
            except SerialException as e:
                show_alert_window('Connection has been interrupted!')
                print(e)
                self.stop_thread()
                data.rx_is_on = False
                update_rx_button_label()
                break
        data.arduino.close()

    async def arduino_readline(self):
        data.rx_data = data.arduino.readline().decode().strip()
        if data.rx_data != '':
            data.dir = float(data.rx_data)
            print(data.rx_data)

    def start_thread(self):
        self.running = True
        super().start()

    def stop_thread(self):
        self.running = False


rx_thread: ArduinoRxThread = None


def show_alert_window(text: str) -> None:
    dpg.set_value(item=constants.ALERT_TXT_TAG, value=text)
    dpg.show_item(item=constants.ALERT_WIN_TAG)


def update_rx_button_label():
    dpg.configure_item(item=constants.SWITCH_RX_BTN_TAG,
                       label='Stop RX' if data.rx_is_on else 'Start RX')


def get_serial_ports() -> list:
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []

    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (BaseException):
            pass

    return result


def rx_button_pressed() -> None:
    global rx_thread

    try:
        if data.rx_is_on:
            if rx_thread.running:
                rx_thread.stop_thread()

            data.rx_is_on = False
            show_alert_window('Disconnected successfully!')
        else:
            data.arduino = Serial(port=dpg.get_value(item=constants.SERIAL_COMBO_TAG),
                                  baudrate=constants.BAUDRATE, timeout=0.1)
            data.rx_is_on = True

            if rx_thread is None or type(rx_thread) is ArduinoRxThread and not rx_thread.running:
                rx_thread = ArduinoRxThread(
                    port=dpg.get_value(item=constants.SERIAL_COMBO_TAG))
                rx_thread.start_thread()
            show_alert_window('Connected successfully!')

        update_rx_button_label()

    except SerialException as e:
        show_alert_window('Error! Check console log.')
        print(e)


def refresh_serial_combo_items() -> None:

    data.serial_ports = get_serial_ports()

    if len(data.serial_ports) == 0:
        data.serial_ports.append(constants.NONE_STR)

    dpg.configure_item(constants.SERIAL_COMBO_TAG, items=data.serial_ports)
    dpg.set_value(constants.SERIAL_COMBO_TAG, data.serial_ports[0])


dpg.create_context()
dpg.create_viewport(title='Automatic direction finder indicator', width=440,
                    height=490, resizable=False)


with dpg.window(tag=constants.PRIMARY_WIN_TAG):
    with dpg.group(horizontal=True):
        dpg.add_text(default_value='COM port:')
        dpg.add_combo(tag=constants.SERIAL_COMBO_TAG,
                      width=100,
                      items=[constants.NONE_STR],
                      default_value=constants.NONE_STR)
        dpg.add_button(label='Refresh',
                       width=100,
                       callback=refresh_serial_combo_items)
        dpg.add_button(tag=constants.SWITCH_RX_BTN_TAG,
                       label='Start RX',
                       width=100,
                       callback=rx_button_pressed)

    dpg.add_separator()

    with dpg.draw_layer():
        dpg.draw_circle(center=[200, 200], radius=150, color=[255, 255, 255])

        with dpg.draw_node():
            dpg.apply_transform(dpg.last_item(),
                                dpg.create_translation_matrix([200, 200]))

            # degrees lines
            for i in range(0, 360, 60):
                with dpg.draw_node():
                    dpg.draw_line(p1=[0, -150], p2=[0, 0])

                dpg.apply_transform(dpg.last_container(),
                                    dpg.create_rotation_matrix(
                                        angle=math.pi*i/180.0, axis=[0, 0, 1]))
            # degrees labels
            for i, (k, v) in enumerate(constants.DEGREES.items()):
                dpg.draw_text(v, k, size=20)

            # direction arrow
            with dpg.draw_node(tag=constants.DIR_ARROW_TAG):
                dpg.draw_arrow(p1=[0, -150], p2=[0, 0], thickness=4.0)


# alert window
with dpg.window(label='Alert',
                tag=constants.ALERT_WIN_TAG,
                modal=True,
                autosize=True,
                show=False):
    dpg.add_text(default_value='', tag=constants.ALERT_TXT_TAG)


dpg.set_viewport_vsync(value=True)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window(window=constants.PRIMARY_WIN_TAG, value=True)

while dpg.is_dearpygui_running():
    if data.rx_is_on:
        dpg.apply_transform(constants.DIR_ARROW_TAG, dpg.create_rotation_matrix(
            math.pi*data.dir/180.0, [0, 0, 1]))

    dpg.render_dearpygui_frame()

dpg.destroy_context()
