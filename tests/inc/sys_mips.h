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
