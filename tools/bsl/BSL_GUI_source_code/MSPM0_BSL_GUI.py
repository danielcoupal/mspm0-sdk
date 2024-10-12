"""
 * Copyright (c) 2024, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import argparse
import os
import platform
import subprocess
import threading
import time
import tkinter
from subprocess import run
from tkinter import *
from tkinter.filedialog import *

from BSL_pack import *
from crc_dialog import *
from get_file import *
from serial_spec import SerialSpec
from txt_to_h import *
from UART_send import *

icon_root = "."

class Tkinter_app:
    def __init__(self, master):
        self.passwordfile = b""
        self.count = 0
        self.firmwaredfile = ""

        menubar = Menu(master, tearoff=0)
        menufile = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="MoreOption", menu=menufile)
        menufile.add_command(label="TXT_to_H", command=txt_to_h_dialog.show)
        menufile.add_command(label="Update XDS110 firmware", command=self.update_xds110)
        menufile.add_command(label="Get CRC", command=lambda: CRC_h(root))
        master["menu"] = menubar

        frame_fw_input = Frame(master)
        frame_fw_input.pack(padx=50, pady=20, anchor=E)
        frame_pw_input = Frame(master)
        frame_pw_input.pack(padx=50, anchor=E)
        frame_serial = Frame(master)
        frame_serial.pack(pady=10, fill=X)
        frame_log = Frame(master)
        frame_log.pack()
        frame_clear = Frame(master)
        frame_clear.pack()
        frame_logo = Frame(master)
        frame_logo.pack(side="bottom")

        self.fw_input_label = Label(frame_fw_input, text="Application firmware file:")
        self.fw_input_label.pack(side="left")
        global input_name
        input_name = StringVar()
        self.fw_entry = Entry(frame_fw_input, width=50, textvariable=input_name)
        self.fw_entry.pack(side="left")
        self.fw_browse_button = Button(frame_fw_input, text="Choose .txt file", command=self.choose_app_file)
        self.fw_browse_button.pack(side="left")

        self.pw_input_label = Label(frame_pw_input, text="Password file:")
        self.pw_input_label.pack(side="left")
        global input_pw
        input_pw = StringVar()
        self.pw_entry = Entry(frame_pw_input, width=50, textvariable=input_pw)
        self.pw_entry.pack(side="left")
        self.pw_browse_button = Button(frame_pw_input, text="Choose .txt file", command=self.choose_pw_file)
        self.pw_browse_button.pack(side="left")

        global photo
        #        photo = PhotoImage(file=SETUP_DIR + "\imag\oi.GIF")
        photo = PhotoImage(file=f"{icon_root}/imag/oi.GIF")
        self.logo = Label(frame_logo, image=photo)
        self.logo.pack()

        self.download_button = Button(frame_serial, text="Download", command=self.download_thread)
        self.download_button.pack()

        self.download_button_label = Label(frame_serial, text="(Download: Just support UART with XDS110)")
        self.download_button_label.pack()

        self.serial_spec_idx = IntVar()
        self.xds_lp_radio = Radiobutton(
            frame_serial,
            text="XDS110 on Launchpad",
            variable=self.serial_spec_idx,
            value=0,
            command=self.xds110_LP,
        )
        self.xds_lp_radio.place(relx=0.7, rely=0)
        self.xds_sa_radio = Radiobutton(
            frame_serial,
            text="Standalone XDS110",
            variable=self.serial_spec_idx,
            value=1,
            command=self.xds110_S,
        )
        self.xds_sa_radio.place(relx=0.7, rely=0.5)

        self.log_scrollbar = Scrollbar(frame_log)
        self.log_scrollbar.pack(side=RIGHT, fill=Y)
        self.textlog = Text(
            frame_log, yscrollcommand=self.log_scrollbar.set, width=70, height=15, bg="white"
        )
        self.log_scrollbar.config(command=self.textlog.yview)
        self.textlog.pack()

        self.textlog.insert(INSERT, "Default hardware is XDS110 on Launchpad.\n")
        self.textlog.tag_config("error", foreground="red")
        self.textlog.tag_config("pass", foreground="green")
        self.textlog.tag_config("normal", foreground="black")
        self.textlog.config(state=DISABLED)

        self.clear_button = Button(frame_clear, text="Clear", command=self.clear_text)
        self.clear_button.pack()

        self.connection_pack = BSL_pack.connection_pack()
        self.get_ID_pack = BSL_pack.get_ID_pack()
        self.password_pack = b""
        self.mass_erase_pack = BSL_pack.mass_erase_pack()
        self.firmware_pack = b""
        self.start_app_pack = BSL_pack.start_app_pack()
        self.path = os.getcwd()

    def xds110_LP(self):
        self.serial_spec = SerialSpec(0, "XDS110 Class Application/User UART")
        self.textlog.config(state=NORMAL)
        self.textlog.insert(
            INSERT, "Changed the hardware bridge to XDS110 on Launchpad.\n", "normal"
        )
        self.textlog.config(state=DISABLED)

    def xds110_S(self):
        self.serial_spec = SerialSpec(1, "XDS110 Class Application/User UART")
        self.textlog.config(state=NORMAL)
        self.textlog.insert(
            INSERT, "Changed the hardware bridge to standalone XDS110.\n", "normal"
        )
        self.textlog.config(state=DISABLED)

    def xds110_BR(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(INSERT, "Changed reset type to boot reset.\n", "normal")
        self.textlog.config(state=DISABLED)

    def xds110_PR(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(INSERT, "Changed reset type to power on reset.\n", "normal")
        self.textlog.config(state=DISABLED)

    def choose_app_file(self):
        f = askopenfilename(
            title="Choose a firmware file",
            initialdir="c:",
            filetypes=[("textfile", ".txt")],
        )
        input_name.set(f)
        self.textlog.config(state=NORMAL)
        if f:
            self.textlog.insert(
                INSERT, "Choose a firmware file at:" + f + "\n", "normal"
            )
            self.firmwaredfile = file_d.get_firmware(f)
            self.firmware_pack = BSL_pack.firmware_pack(self.firmwaredfile)
        else:
            self.textlog.insert(
                INSERT, "Error: Please choose a firmware file.\n", "error"
            )
            self.firmwaredfile = ""
            self.firmware_pack = b""
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)

    def choose_pw_file(self):
        f1 = askopenfilename(
            title="Choose a password file",
            initialdir="c:",
            filetypes=[("textfile", ".txt")],
        )
        input_pw.set(f1)
        self.textlog.config(state=NORMAL)
        if f1:
            self.textlog.insert(
                INSERT, "Choose a password file at:" + f1 + "\n", "normal"
            )
            self.passwordfile = b""
            self.passwordfile = file_d.get_password(f1)
            if self.passwordfile == b"":
                self.textlog.insert(
                    INSERT, "Error: Password format is not correct!\n", "error"
                )
            else:
                self.password_pack = BSL_pack.password_pack(self.passwordfile)
        else:
            self.passwordfile = b""
            self.textlog.insert(
                INSERT, "Error: Please choose a password file.\n", "error"
            )

        # else:
        #     print(self.passwordfile)
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)
    def download_thread(self):
        T = threading.Thread(target=self.download, args=())
        T.start()

    def download(self):
        self.textlog.config(state=NORMAL)
        self.download_button.config(state='disabled')
        if self.passwordfile != b"" and self.firmwaredfile != "":
            find_flag = self.serial_spec.connect(UART_S)
            if find_flag:
                self.textlog.insert(
                    INSERT, "Find MSP COM port:" + find_flag + "\n", "normal"
                )
                self.textlog.see(END)
                ser_port = UART_S.config_uart(find_flag)
                self.textlog.insert(
                    INSERT,
                    "Configure UART: 9600 baudrate, 8 data bits (LSB first), no parity, and 1 stop bit.\n",
                    "normal",
                )
                self.textlog.see(END)
                UART_S.send_data(ser_port, self.connection_pack)
                response_ = UART_S.read_data(ser_port, 1)
                self.serial_spec.on_connect()
                UART_S.send_data(ser_port, b"\xbb")
                response01 = UART_S.read_data(ser_port, 1)
                if response01 == "51":
                    self.textlog.insert(
                        INSERT, "MSPM0 is in BSL mode.\nGet device ID...\n", "normal"
                    )
                    self.textlog.see(END)
                    UART_S.send_data(ser_port, self.get_ID_pack)
                    response1 = UART_S.read_data(ser_port, 33)
                    self.textlog.insert(INSERT, "Send the password...\n", "normal")
                    self.textlog.see(END)
                    UART_S.send_data(ser_port, self.password_pack)
                    response2 = UART_S.read_data(ser_port, 1)
                    check = self.check_pack(response2)
                    if check:
                        response2 = UART_S.read_data(ser_port, 9)
                        check2 = self.check_reponse(response2[8:10])
                        # print(response2[8:10])
                        if check2:
                            self.textlog.insert(INSERT, "Mass erase...\n", "normal")
                            self.textlog.see(END)
                            UART_S.send_data(ser_port, self.mass_erase_pack)
                            response2 = UART_S.read_data(ser_port, 1)
                            response2 = UART_S.read_data(ser_port, 9)
                            self.textlog.insert(
                                INSERT, "Send the firmware...\n", "normal"
                            )
                            self.textlog.see(END)
                            # print(type(firmware_pack))
                            # print(firmware_pack)
                            for list_code in self.firmware_pack:
                                UART_S.send_data(ser_port, list_code)
                                response3 = UART_S.read_data(ser_port, 1)
                                self.count = self.count + 1
                                check = self.check_pack(response3)
                                if check:
                                    response3 = UART_S.read_data(ser_port, 9)
                                    check3 = self.check_reponse(response3[8:10])
                                    if check3:
                                        pass
                                    else:
                                        break
                                else:
                                    break
                            if check:
                                self.textlog.insert(
                                    INSERT, "Send firmware successfully!\n", "normal"
                                )
                                self.textlog.insert(
                                    INSERT,
                                    "Boot reset the device to start application ...\n",
                                    "normal",
                                )
                                self.textlog.insert(
                                    INSERT,
                                    "-----------Download finished!----------\n",
                                    "pass",
                                )
                                self.textlog.see(END)
                                UART_S.send_data(ser_port, self.start_app_pack)
                                response3 = UART_S.read_data(ser_port, 1)
                    else:
                        self.textlog.insert(INSERT, "Error: No response！\n", "error")
                        self.textlog.see(END)
                else:
                    self.textlog.insert(INSERT, "Error: No response！\n", "error")
                    self.textlog.see(END)
            else:
                self.textlog.insert(
                    INSERT, "Error: Can not find MSP COM port!\n", "error"
                )
                self.textlog.see(END)
        else:
            self.textlog.insert(
                INSERT, "Error: please choose all files above!\n", "error"
            )
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)
        self.download_button.config(state='normal')

    def clear_text(self):
        self.textlog.config(state=NORMAL)
        self.textlog.delete("2.0", "end")
        self.textlog.insert(INSERT, "\n")
        self.textlog.config(state=DISABLED)

    def check_pack(self, pack_ack):
        flagg = 0
        #        self.textlog.config(state=NORMAL)
        if pack_ack == "00":
            flagg = 1
            self.textlog.insert(INSERT, '[Firmware update on going...] Send firmware package ' + str(self.count) + ' successfully!\n', "normal")
        elif pack_ack == "51":
            self.textlog.insert(INSERT, "Error: Header incorrect!\n", "error")
        elif pack_ack == "52":
            self.textlog.insert(INSERT, "Error: Checksum incorrect!\n", "error")
        elif pack_ack == "53":
            self.textlog.insert(INSERT, "Error: Packet size zero!\n", "error")
        elif pack_ack == "54":
            self.textlog.insert(INSERT, "Error: Packet size too big!\n", "error")
        elif pack_ack == "55":
            self.textlog.insert(INSERT, "Error: Unknown error!\n", "error")
        elif pack_ack == "56":
            self.textlog.insert(INSERT, "Error: Unknown baud rate!\n", "error")
        else:
            self.textlog.insert(INSERT, "Error: Unknow else error!\n", "error")
        #       self.textlog.config(state=DISABLED)
        self.textlog.see(END)
        return flagg

    def check_reponse(self, pack_res):
        flagg = 0
        #       self.textlog.config(state=NORMAL)
        if pack_res == "00":
            flagg = 1
            self.textlog.insert(INSERT, "Operation success!\n", "normal")
        elif pack_res == "01":
            self.textlog.insert(INSERT, "Error: flash program failed!\n", "error")
        elif pack_res == "02":
            self.textlog.insert(INSERT, "Error: Mass Erase failed!\n", "error")
        elif pack_res == "04":
            self.textlog.insert(INSERT, "Error: BSL locked!!\n", "error")
        elif pack_res == "05":
            self.textlog.insert(INSERT, "Error: BSL password error!\n", "error")
        elif pack_res == "06":
            self.textlog.insert(
                INSERT, "Error: Multiple BSL password error!\n", "error"
            )
        elif pack_res == "07":
            self.textlog.insert(INSERT, "Error: Unknown Command!\n", "error")
        elif pack_res == "08":
            self.textlog.insert(INSERT, "Error: Invalid memory range!\n", "error")
        elif pack_res == "0B":
            self.textlog.insert(INSERT, "Error: Factory reset disabled!\n", "error")
        elif pack_res == "0C":
            self.textlog.insert(
                INSERT, "Error: Factory reset password error!\n", "error"
            )
        else:
            self.textlog.insert(INSERT, "Error: Unknow else error!\n", "error")
        self.textlog.see(END)
        return flagg

    #        self.textlog.config(state=DISABLED)

    def update_xds110(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(
            INSERT, "Update the XDS110 firmware to version firmware_3.0.0.28...\n"
        )
        path = os.getcwd()
        print(path)
        # os.system(path + "/common/uscif/xds110/xdsdfu.exe -m")
        subprocess.run(
            path
            + "/common/uscif/xds110/xdsdfu.exe -m",
            shell=True,
            capture_output=True,
            encoding='utf-8')
        time.sleep(0.5)
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # os.system(
        #     path
        #     + "/common/uscif/xds110/xdsdfu.exe -f "
        #     + path
        #     + "/common/uscif/xds110/firmware_3.0.0.28.bin -r"
        # )
        subprocess.run(
            path
            + "/common/uscif/xds110/xdsdfu.exe -f "
            + path
            + "/common/uscif/xds110/firmware_3.0.0.28.bin -r",
            shell=True,
            capture_output=True,
            encoding='utf-8')
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(2)
        self.textlog.insert(INSERT, "XDS110 firmware update finished.\n", "pass")
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MSPM0 Bootloader GUI")
    parser.add_argument('--icon-root', type=str, default=".", help='Root directory for runtime files')
    args = parser.parse_args()
    icon_root = args.icon_root

    file_d = Get_files()
    BSL_pack = BSL_Pack()
    UART_S = UART_send()
    root = Tk()
    root.iconbitmap(f"{icon_root}/imag/Capture.ico")
    root.geometry("700x520+500+500")
    root.title("MSPM0 Bootloader GUI  v1.2")
    txt_to_h_dialog = TXT_to_h(root)
    app = Tkinter_app(root)
    root.mainloop()
