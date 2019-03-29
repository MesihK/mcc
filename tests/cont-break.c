#include"sys.h"

int main (){
	int a = 0;
	int i = 0;
	/* do while test */
	do{
		a = a+1;
		if(a < 2) continue;
		print_int(a);
		if(a > 3) break;
	}while(a<5);
	i = 9;
}
