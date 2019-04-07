#include <sys.h> 

// C recursive function to solve tower of hanoi puzzle 
void towerOfHanoi(int n, char from_rod, char to_rod, char aux_rod) 
{ 
	if (n == 1) 
	{ 
		printstr("\n Move disk 1 from rod: ");
		print_char(from_rod);
		printstr(" to rod: "); 
		print_char(to_rod);
		return; 
	} 
	towerOfHanoi(n-1, from_rod, aux_rod, to_rod); 
	printstr("\n Move disk: ");
	print_int(n);
	printstr(" from rod: ");
	print_char(from_rod);
	printstr(" to rod: "); 
	print_char(to_rod);
	towerOfHanoi(n-1, aux_rod, to_rod, from_rod); 
} 

int main() 
{ 
	int n = 4; // Number of disks 
	towerOfHanoi(n, 'A', 'C', 'B');  // A, B and C are names of rods 
	return 0; 
} 
