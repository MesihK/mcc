#include"sys.h"

int topla(int a, int b){
	return a+b;
}
int carp(int a, int b){
	return a*b;
}
int bol(int a, int b){
	return a/b;
}
int cikar(int a, int b){
	return a-b;
}
int main(){
	int a = 3;
	int b = 5;

	print_int(topla(a,b));
	print_int(carp(a,b));
	print_int(bol(a,b));
	print_int(cikar(a,b));
	print_int(topla(a,carp(a,b)));
	print_int(bol(topla(a,a),a));
}
