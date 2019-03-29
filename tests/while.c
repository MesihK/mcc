#include"sys.h"


int main(){
	int i = 9;
	while(i < 5){
		print_int(i);
		i = i+1;
	}
	i = 5;
	while( i > 0){
		print_int(i);
		i = i-1;
	}
}
