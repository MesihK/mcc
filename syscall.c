int main (){
	printstr("Please input a number:");
	int i = read_int();
	printstr("Recursive addition result:");
	print_int(recursive_add(i));
}
int recursive_add(int a){
	if( a==0) return 0;
	else return recursive_add(a-1)+a;
	int b = 4;
}
void print_char(int a){
	asm("li $v0 11");
	asm("syscall");
}
void print_int(int a){
	asm("li $v0 1");
	asm("syscall");
}
int read_char(){
	asm("li $v0 12");
	asm("syscall");
}
int read_int(){
	asm("li $v0 5");
	asm("syscall");
}
