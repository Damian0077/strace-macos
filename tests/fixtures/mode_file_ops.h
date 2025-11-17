/*
 * File operations modes
 */

#ifndef MODE_FILE_OPS_H
#define MODE_FILE_OPS_H

#include <fcntl.h>
#include <signal.h>
#include <sys/stat.h>
#include <unistd.h>

static volatile int keep_running = 1;

static void sigterm_handler(int sig) {
  (void)sig;
  keep_running = 0;
}

int mode_file_ops(int argc, char *argv[]) {
  const char *path = argc > 2 ? argv[2] : "/tmp/test.txt";

  /* Open, write, close */
  int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
  if (fd >= 0) {
    write(fd, "hello world\n", 12);
    close(fd);
  }

  /* Open, read, close */
  fd = open(path, O_RDONLY);
  if (fd >= 0) {
    char buf[100];
    read(fd, buf, sizeof(buf));
    close(fd);
  }

  /* Unlink */
  unlink(path);

  return 0;
}

int mode_file_ops_loop(int argc, char *argv[]) {
  const char *path = argc > 2 ? argv[2] : "/tmp/test.txt";

  /* Setup signal handler */
  signal(SIGTERM, sigterm_handler);

  /* Write ready marker */
  write(STDOUT_FILENO, "READY\n", 6);

  while (keep_running) {
    /* Open, write, close */
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd >= 0) {
      write(fd, "hello world\n", 12);
      close(fd);
    }

    /* Open, read, close */
    fd = open(path, O_RDONLY);
    if (fd >= 0) {
      char buf[100];
      read(fd, buf, sizeof(buf));
      close(fd);
    }

    /* Unlink */
    unlink(path);

    /* Small sleep */
    usleep(100000); /* 0.1 seconds */
  }

  return 0;
}

#endif /* MODE_FILE_OPS_H */
