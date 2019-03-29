#include"sys.h"

int main(){
	int a = 42;
	int b = 94;

	print_int(a+b);
	print_int(a-b);
	print_int(a*b);
	print_int(a/b);
	print_int(a&b);
	print_int(a|b);
	print_int(a^b);
	print_int(~(a&b));
	print_int(~(a|b));
	print_int(~(a^b));
	print_int(-a);
	print_int(~b);
}
