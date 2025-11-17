/*
 * Network operations modes
 */

#ifndef MODE_NETWORK_H
#define MODE_NETWORK_H

#include <arpa/inet.h>
#include <netinet/in.h>
#include <signal.h>
#include <sys/socket.h>
#include <unistd.h>

extern volatile int keep_running;
extern void sigterm_handler(int sig);

int mode_network(int argc, char *argv[]) {
  (void)argc;
  (void)argv;

  /* Create socket */
  int sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock >= 0) {
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(80);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

    /* Try to connect */
    connect(sock, (struct sockaddr *)&addr, sizeof(addr));

    close(sock);
  }

  return 0;
}

int mode_network_loop(int argc, char *argv[]) {
  (void)argc;
  (void)argv;

  /* Setup signal handler */
  signal(SIGTERM, sigterm_handler);

  /* Write ready marker */
  write(STDOUT_FILENO, "READY\n", 6);

  while (keep_running) {
    /* Create socket */
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock >= 0) {
      struct sockaddr_in addr;
      addr.sin_family = AF_INET;
      addr.sin_port = htons(80);
      inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);

      /* Try to connect */
      connect(sock, (struct sockaddr *)&addr, sizeof(addr));

      close(sock);
    }

    /* Small sleep */
    usleep(100000); /* 0.1 seconds */
  }

  return 0;
}

#endif /* MODE_NETWORK_H */
