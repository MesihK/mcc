#include"sys.h"

int arr[6] = {1, 3, 5, 7, 9, 11};
int arr_size = 6;
void printArray(){
	int i = 0;
	for ( i = 0; i < arr_size; i = i + 1){
		print_int(arr[i]);
		printstr(" ");
	}

}
int main(){
	printArray();
}
