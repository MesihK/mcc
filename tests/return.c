#include"sys.h"

int test2(){
	print_int(1);
	print_int(2);
	print_int(3);
	return 0;
	print_int(4);
	print_int(5);
	return 1;
}
void test(){
	print_int(1);
	print_int(2);
	print_int(3);
	return;
	print_int(4);
	print_int(5);
	return;
}
int main(){
	test();
	print_int(test2());
}
