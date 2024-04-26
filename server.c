#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>

// When testing locally, since you only have one ip, you need two ports
#define SERVER_PORT 4001
#define CLIENT_PORT 4002
#define SERVER_IP "127.0.0.1"

int listening = 1; //used in termination signal handler
int server_socket = 0;

struct Packet {
    double header; //header is not a double, but has the same amount of bytes
    double fsTimer; //^
    int32_t tick;
    int32_t tmp;
    double x_lin_vel;
    double y_lin_vel;
    double z_lin_vel;
    double pitch_ang_vel;
    double roll_ang_vel;
    double pitch_pos;
    double roll_pos;
    double altitude;
    double garbage; //padding
};

struct CommandMsg {
    char header[8]; //header is technically a packet structure in reality, but this was easier
    unsigned char ride_command;
    unsigned char spare[3]; //padding
};

// List of commands that can be sent as a command message
enum COMMANDS {
    NO_COMMAND,
    START_LOAD_LANGUAGE_1_COMMAND,
    DOOR_OPENED_COMMAND,
    DOOR_CLOSED_COMMAND,
    GAME_START_COMMAND,
    STOP_END_OF_GAME_COMMAND,
    STOP_AUTO_COMMAND,
    STOP_MANUAL_COMMAND,
    START_LOAD_LANGUAGE_2_COMMAND,
    START_LOAD_LANGUAGE_3_COMMAND,
    START_LOAD_DEMO_COMMAND,
    NUMBER_OF_GAME_COMMAND
};

// Interrupt handler so you can close the program and socket any time
void
handle_signal(int signo)
{
    if (signo == SIGINT)
    {
        printf("\nexiting\n");
        listening = 0;
        close(server_socket);
        exit(1);
    }
}

int
main()
{
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_len = sizeof(client_address);

    // Create UDP socket
    server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (server_socket == -1)
    {
        perror("Error creating socket");
        return 1;
    }

    // Initialize server address struct
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr(SERVER_IP);
    server_address.sin_port = htons(SERVER_PORT);

    // bind the socket
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1)
    {
        perror("Error binding socket");
        close(server_socket);
        return 1;
    }

    // Set up a port for sending the command message
    socklen_t len = sizeof(client_address);
    client_address.sin_family = AF_INET;
    client_address.sin_port = htons(CLIENT_PORT);
    client_address.sin_addr.s_addr = inet_addr(SERVER_IP);

    if (signal(SIGINT, handle_signal) == SIG_ERR)
    {
        perror("Error setting up signal handler");
        close(server_socket);
        return 1;
    }

    printf("Test server sending and recieving...\n");

    int counter = 1;
    while (listening)
    {

        // Send data (less frequently than receive data to simulate occasional message commands)
        if (counter % 10 == 0)
        {

            // 0x05 is for MC_TO_SC_HEARTBEAT, 0x0C is size of message, which is 12 bytes
            // The command being sent is arbitrary and you can choose anything in the COMMANDS enum
            struct CommandMsg command_msg = {{0x00, 0x05, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00}, DOOR_OPENED_COMMAND, {0x00, 0x00, 0x00}};

            sendto(server_socket, &command_msg, sizeof(command_msg), 0, (const struct sockaddr *)&client_address, len);
            counter = 1;
        }
        counter++;


        struct Packet packet;

        // Recieve data
        ssize_t received_bytes = recvfrom(server_socket, &packet, sizeof(packet), 0, (struct sockaddr*)&client_address, &client_address_len);

        if (received_bytes == -1)
        {
            perror("Error receiving data");
            continue;
        }

        printf("%d %d %0.2f %0.2f %0.2f %0.2f %0.2f %0.2f %0.2f %0.2f\n",
                packet.tick,
                packet.tmp,
                packet.x_lin_vel,
                packet.y_lin_vel,
                packet.z_lin_vel,
                packet.pitch_ang_vel,
                packet.roll_ang_vel,
                packet.pitch_pos,
                packet.roll_pos,
                packet.altitude);
    }

    close(server_socket);

    return 0;
}

