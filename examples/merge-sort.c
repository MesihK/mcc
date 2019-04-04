int arr[6] = {12, 11, 13, 5, 6, 7}; 
int arr_size = 6;
  
/* Merges two subarrays of arr[]. */
/* First subarray is arr[l..m] */
/* Second subarray is arr[m+1..r] */
void merge(int l, int m, int r) 
{ 
    int i;
    int j;
    int k;
    int n1 = m - l + 1; 
    int n2 = r - m; 
  
    /* create temp arrays */
    int L[10];
    int R[10]; 
  
    /* Copy data to temp arrays L[] and R[] */
    for (i = 0; i < n1; i = i+1) 
        L[i] = arr[l + i]; 
    for (j = 0; j < n2; j = j+1) 
        R[j] = arr[m + 1+ j]; 
  
    /* Merge the temp arrays back into arr[l..r]*/
    i = 0; /* Initial index of first subarray */
    j = 0; /* Initial index of second subarray */
    k = l; /* Initial index of merged subarray */
    while (i < n1)
    { 
	if(j >= n2) break;
        if (L[i] <= R[j]) 
        { 
            arr[k] = L[i]; 
            i=i+1; 
        } 
        else
        { 
            arr[k] = R[j]; 
            j=j+1; 
        } 
        k=k+1; 
    } 
  
    /* Copy the remaining elements of L[], if there 
       are any */
    while (i < n1) 
    { 
        arr[k] = L[i]; 
        i=i+1; 
        k=k+1; 
    } 
  
    /* Copy the remaining elements of R[], if there 
       are any */
    while (j < n2) 
    { 
        arr[k] = R[j]; 
        j=j+1; 
        k=k+1; 
    } 
} 
  
/* l is for left index and r is right index of the 
   sub-array of arr to be sorted */
void mergeSort(int l, int r) 
{ 
    if (l < r) 
    { 
        /* Same as (l+r)/2, but avoids overflow for */
        /* large l and h */
        int m = l+(r-l)/2; 
  
        /* Sort first and second halves */
        mergeSort(l, m); 
        mergeSort(m+1, r); 
  
        merge(l, m, r); 
    } 
} 
  
/* UTILITY FUNCTIONS */
/* Function to print an array */
void printArray()
{ 
    int i; 
    for (i=0; i < arr_size; i = i+1) {
        print_int(arr[i]); 
	printstr(" "); 
    }
    printstr("\n"); 
} 
  
/* Driver program to test above functions */
int main() 
{ 
    printstr("Given array is \n"); 
    printArray();
  
    mergeSort(0, arr_size - 1); 
  
    printstr("\nSorted array is \n"); 
    printArray();
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
