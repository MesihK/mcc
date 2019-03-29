#include"sys.h"

int main(){
	int i = 3;

	if(i == 3)print_int(1);
	if(i == 2)print_int(2);

	if(i != 2)print_int(3);
	if(i != 3)print_int(4);

	if(i >= 3)print_int(5);
	if(i >= 4)print_int(6);

	if(i <= 3)print_int(7);
	if(i <= 2)print_int(8);

	if(i < 4)print_int(9);
	if(i < 3)print_int(10);

	if(i > 2)print_int(11);
	if(i > 3)print_int(12);
}
