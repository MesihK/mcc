#include"sys.h"


int main(){
	int i = 9;
	for(i=0; i<5; i = i + 1){
		print_int(i);
	}
	for(i=5; i>0; i = i - 1){
		print_int(i);
	}
}
