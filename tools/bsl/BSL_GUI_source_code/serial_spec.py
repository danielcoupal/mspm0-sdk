'''
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
'''

from tkinter import INSERT

import UART_send

class SerialSpec():
    def __init__(self, textlog, id, serial_desc: str):
        self.textlog = textlog
        self.id = id
        self.serial_desc = serial_desc # For when generic serial gets added. It will become a UART_S parameter.

    def connect(self, UART_S) -> str:
        if self.id == "a":
            try:
                subprocess.run(
                    self.path
                    + "/common/uscif/dbgjtag.exe  -f @xds110 -Y gpiopins, config=0x1, write=0x1",
                    shell=True,
                    capture_output=True,
                    encoding='utf-8')
                subprocess.run(
                    self.path
                    + "/common/uscif/xds110/xds110reset.exe -d 1400",
                    shell=True,
                    capture_output=True,
                    encoding='utf-8')
            except:
                self.textlog.insert(
                    INSERT,
                    "Error: please make sure the folder path not include !\n",
                    "error",
                )
        else:
            if self.id == "b":
                subprocess.run(
                    self.path
                    + "/common/uscif/dbgjtag.exe -f @xds110 -Y power,supply=on,voltage=3.2",
                    shell=True,
                    capture_output=True,
                    encoding='utf-8')
                subprocess.run(
                    self.path
                    + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x02",
                    shell=True,
                    capture_output=True,
                    encoding='utf-8')
                time.sleep(1.4)
                subprocess.run(
                    self.path
                    + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x03",
                    shell=True,
                    capture_output=True,
                    encoding='utf-8')
            else:
                # print(self.id)
                self.textlog.insert(
                    INSERT, "No correct hardware bridge selected.\n", "error"
                )
        return UART_S.find_MSP_COM()

    def on_connect(self):
        if self.id == "a":
            subprocess.run(
                self.path
                + "/common/uscif/dbgjtag.exe  -f @xds110 -Y gpiopins, config=0x1, write=0x0",
                shell=True,
                capture_output=True,
                encoding='utf-8')
        else:
            if self.id == "b":
                subprocess.run(
                    self.path
                    + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x01",
                    shell=True,
                    capture_output=True,
                    encoding='utf-8')
