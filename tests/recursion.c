#include"sys.h"

int topla(int a){
	if(a <= 0) return 0;
	else return topla(a-1)+a;
}
int main(){
	int i = 5;

	print_int(topla(i));
}
