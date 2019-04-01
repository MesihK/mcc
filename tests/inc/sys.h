#include<stdio.h>
#include<stdlib.h>

void printstr(char *str){
	printf("%s", str);
}

void print_int(int i){
	printf("%d",i);
}

void print_char(char c){
	printf("%c",c);
}

char read_char(){
	char c;
	scanf("%c",&c);
	return c;
}

int read_int(){
	int i;
	scanf("%d",&i);
	return i;
}
