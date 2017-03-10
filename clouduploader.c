#include <stdio.h>
#include <unistd.h>


/* Usage: clouduploader <file_path> <file_name> */
int
main(int argc, char** argv)
{
    char* args[] = {
        "./dropbox_uploader.sh",
        "upload",
        argv[1],
        argv[2],
        0
    };

    char* envp[] = {
        "HOME=/home/pi/",
        0
    };

    execve(args[0], &args[0], envp);
    return 0;
}



