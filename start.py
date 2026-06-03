import glob
import os
import time
import serial

SERIAL_PORT = "/dev/serial0"
BAUDRATE = 9600
ROWS = 7
COLS = 28
FRAME_DIR = "frames"
FRAME_DELAY = 1 / 15.27

CMD_START = 0x80
CMD_WRITE = 0x83
CMD_END = 0x8F


def print_matrix(matrix):
    for row in matrix:
        print("".join("■" if col == "1" else "□" for col in row))
    print()


def send_to_flipdot(ser, matrix):
    data_bytes = bytearray()
    for col in range(COLS):
        col_data = 0
        for row in range(ROWS):
            if matrix[row][col] == "1":
                col_data |= 1 << row
        data_bytes.append(col_data)

    transmission = (
        bytearray([CMD_START, CMD_WRITE, 0xFF]) + data_bytes + bytearray([CMD_END])
    )
    ser.write(transmission)


def main():
    frame_files = sorted(glob.glob(os.path.join(FRAME_DIR, "frame_*.txt")))

    with serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1) as ser:
        for frame_file in frame_files:
            with open(frame_file, "r") as file:
                matrix = [line.strip() for line in file]

            print_matrix(matrix)
            send_to_flipdot(ser, matrix)
            time.sleep(FRAME_DELAY)


if __name__ == "__main__":
    main()