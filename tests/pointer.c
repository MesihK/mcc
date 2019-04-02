#include<sys.h>

int main(){
	int i[3] = {1,2,3};
	int *pi = &i[0];

	if (pi == &i[0]){
		print_int(1);
		printstr("\n");
	}
	print_int(*pi);
	printstr("\n");
	pi = pi + 1;
	print_int(*pi);
	printstr("\n");
}
