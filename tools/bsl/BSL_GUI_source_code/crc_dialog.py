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
import tkinter
from tkinter import *
from tkinter.filedialog import *

def CRC_h(tkinter_root: tkinter.Tk):
    sub_win2 = Toplevel(tkinter_root)
    sub_win2.title("Get CRC")
    #        sub_win1.attributes("-topmost", True)
    sub_win2.geometry("700x350+300+200")
    sub_win2.grab_set()
    frames_CRC_0 = Frame(sub_win2)
    frames_CRC_0.pack(padx=50, pady=20, anchor=W)
    frames_CRC_1 = Frame(sub_win2)
    frames_CRC_1.pack(padx=50, anchor=W)
    frames_CRC_3 = Frame(sub_win2)
    frames_CRC_3.pack(pady=10)
    frames_CRC_4 = Frame(sub_win2)
    frames_CRC_4.pack()

    labelss_CRC_0 = Label(frames_CRC_0, text="Choose a firmware .txt file")
    labelss_CRC_0.pack(side="left")
    global input_name_ss_CRC
    input_name_ss_CRC = StringVar()
    global entryss_crc
    entryss_CRC = Entry(frames_CRC_0, width=50, textvariable=input_name_ss_CRC)
    entryss_CRC.pack(side="left")
    buttonss_CRC = Button(
        frames_CRC_0, text="Choose .txt file", command=choosetxtfile_crc
    )
    buttonss_CRC.pack(side="left")

    labelss3_CRC = Label(frames_CRC_1, text="CRC Start Address:")
    labelss3_CRC.pack(side="left")
    global out_crc_star
    out_crc_star = StringVar()
    out_crc_star = ""

    global entryss3_crc
    entryss3_crc = Entry(frames_CRC_1, width=20)
    entryss3_crc.pack(side="left")
    entryss3_crc.delete(0, "end")
    entryss3_crc.insert(INSERT, out_crc_star)
    entryss3_crc["state"] = "readonly"

    labelss1_CRC = Label(frames_CRC_1, text="CRC Length:")
    labelss1_CRC.pack(side="left")
    global out_crc_len
    out_crc_len = StringVar()
    out_crc_len = ""

    global entryss1_crc
    entryss1_crc = Entry(frames_CRC_1, width=20)
    entryss1_crc.pack(side="left")
    entryss1_crc.delete(0, "end")
    entryss1_crc.insert(INSERT, out_crc_len)
    entryss1_crc["state"] = "readonly"

    labelss2_CRC = Label(frames_CRC_1, text="CRC Result:")
    labelss2_CRC.pack(side="left")
    global out_crc_result
    out_crc_result = StringVar()
    out_crc_result = ""

    global entryss2_crc
    entryss2_crc = Entry(frames_CRC_1, width=20)
    entryss2_crc.pack(side="left")
    entryss2_crc.delete(0, "end")
    entryss2_crc.insert(INSERT, out_crc_result)
    entryss2_crc["state"] = "readonly"

    buttonss2_c = Button(frames_CRC_3, text="Generate", command=gen_crc)
    buttonss2_c.pack()

    s3_crc = Scrollbar(frames_CRC_4)
    s3_crc.pack(side=RIGHT, fill=Y)

    global textlogsubs_crc
    textlogsubs_crc = Text(
        frames_CRC_4,
        yscrollcommand=s3_crc.set,
        width=70,
        height=10,
        bg="white",
    )
    s3_crc.config(command=textlogsubs_crc.yview)
    textlogsubs_crc.pack()
    textlogsubs_crc.tag_config("errors_", foreground="red")
    textlogsubs_crc.tag_config("pass_s_", foreground="green")
    textlogsubs_crc.insert(
        INSERT, "This function is used for generate the CRC results.\n"
    )
    textlogsubs_crc.insert(
        INSERT,
        "Note: it just can calculate the CRC at first section that the contents under first @address\n",
    )
    textlogsubs_crc.config(state=DISABLED)

    sub_win2.focus_set()

def gen_crc():
    textlogsubs_crc.config(state=NORMAL)
    input_names_crc = input_name_ss_CRC.get()
    if input_names_crc:
        textlogsubs_crc.insert(INSERT, "Generating...\n")
        gen_crc_fun(input_names_crc)
        textlogsubs_crc.insert(
            INSERT, "-----Generate the CRC -----\n ", "pass_s_"
        )
    else:
        textlogsubs_crc.insert(
            INSERT, "Error: Please choose a .txt firmware.\n", "errors_"
        )
    textlogsubs_crc.see(END)
    textlogsubs_crc.config(state=DISABLED)

def choosetxtfile_crc():
    fs_c = askopenfilename(
        title="Choose a firmware file",
        initialdir="c:",
        filetypes=[("textfile", ".txt")],
    )
    input_name_ss_CRC.set(fs_c)
    textlogsubs_crc.config(state=NORMAL)
    if fs_c:
        textlogsubs_crc.insert(
            INSERT, "Choose a firmware file at:" + fs_c + "\n", "normal"
        )
    else:
        textlogsubs.insert(
            INSERT, "Error: Please choose a firmware file.\n", "errors_"
        )
    textlogsubs_crc.see(END)
    textlogsubs_crc.config(state=DISABLED)

def gen_crc_fun(file430):
    data_array = []
    flag = 0
    sizecount = 0
    bytes_buf = b""
    bytes_buf1 = ""
    with open(file430) as file_object:
        lines = file_object.readlines()
    for line in lines:
        if line[0] == "@":
            flag += 1
            if flag == 1:
                line = line.rstrip()
                bytes_buf1 = "0x" + line[1:]
                # print(bytes_buf1)
        else:
            if flag == 1 and line[0] != "q":
                line2 = "0x" + line
                # 			print(isinstance(line, str))
                line2 = line.replace(" \n", "\n")
                line2 = line.replace(" ", " 0x")
                # 			print(line)
                sizecount += line2.count("0x")
                data_array2 = line2.split()
                # 			data_array2.pop()
                data_array += data_array2
                bytes_buf += bytes.fromhex(line)
    checksum = crc32_(bytes_buf)
    entryss3_crc["state"] = "normal"
    entryss3_crc.delete(0, "end")
    entryss3_crc.insert(INSERT, bytes_buf1)
    entryss3_crc["state"] = "readonly"
    entryss1_crc["state"] = "normal"
    entryss1_crc.delete(0, "end")
    entryss1_crc.insert(INSERT, hex(sizecount))
    entryss1_crc["state"] = "readonly"
    entryss2_crc["state"] = "normal"
    entryss2_crc.delete(0, "end")
    entryss2_crc.insert(INSERT, hex(checksum))
    entryss2_crc["state"] = "readonly"
    # print(hex(checksum))

def crc32_(data_B):
    crc = 0xFFFFFFFF
    crc32_POLY = 0xEDB88320
    for b in data_B:
        crc = crc ^ b
        ii = 1
        while ii <= 8:
            mask = -(crc & 1)
            crc = (crc >> 1) ^ (crc32_POLY & mask)
            ii += 1
    return crc
