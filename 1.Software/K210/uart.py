#This is a example for uart on K210

from fpioa_manager import fm
from machine import UART
import utime

fm.register(34, fm.fpioa.UART1_TX, force=True)
fm.register(35, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

while(1):
    read_data = uart_A.readline()
    if read_data:
        read_str = read_data.decode('utf-8').strip()
        print("string = ", read_str)

    utime.sleep_ms(1000)
