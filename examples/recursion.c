
int topla(int a){
	if(a <= 0) return 0;
	else return topla(a-1)+a;
}
int main(){
	int i = 5;

	print_int(topla(i));
}
void print_char(char a){
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
