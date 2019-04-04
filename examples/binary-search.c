int arr[5] = { 2, 3, 4, 10, 40 }; 
int n = 5;
  
/* A iterative binary search function. It returns */
/* location of x in given array arr[l..r] if present, */
/* otherwise -1 */
int binarySearch(int l, int r, int x) 
{ 
    while (l <= r) { 
        int m = l + (r - l) / 2; 
  
        /* Check if x is present at mid */
        if (arr[m] == x) 
            return m; 
  
        /* If x greater, ignore left half */
        if (arr[m] < x) 
            l = m + 1; 
  
        /* If x is smaller, ignore right half */
        else
            r = m - 1; 
    } 
  
    /* if we reach here, then element was  not present */
    return -1; 
} 
  
int main() 
{ 
    int x = 10; 
    int result = binarySearch(0, n - 1, x); 
    if( result == -1){
	    printstr("Element is not present in array");
    } else {
	    printstr("Element is at:");
	    print_int(result);
    }
    return 0; 
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
