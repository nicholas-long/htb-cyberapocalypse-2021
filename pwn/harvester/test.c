#include <stdio.h>
#include <unistd.h>

int main(){
    char buf[1000];
    char buf2[1000];
    setvbuf(stdin, (char*)0, 2, 0);
    setvbuf(stdout, (char*)0, 2, 0);


    scanf("%s", buf);
    printf("%s\n", buf);

    read(0, buf2, 4);
    printf("%s\n", buf2);

    return 0;
}