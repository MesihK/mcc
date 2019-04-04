int arr[6] = {10, 7, 8, 9, 1, 5}; 
int n = 6;
  
/* A utility function to swap two elements */
void swap(int* a, int* b) 
{ 
    int t = *a; 
    *a = *b; 
    *b = t; 
} 
  
/* This function takes last element as pivot, places 
   the pivot element at its correct position in sorted 
    array, and places all smaller (smaller than pivot) 
   to left of pivot and all greater elements to right 
   of pivot */
int partition (int low, int high) 
{ 
    int pivot = arr[high];    
    int i = (low - 1);  /* Index of smaller element */
  
    int j = 0;
    for (j = low; j <= high- 1; j=j+1) 
    { 
        /* If current element is smaller than or equal to pivot */
        if (arr[j] <= pivot) 
        { 
            i=i+1;    /* increment index of smaller element */
            swap(&arr[i], &arr[j]); 
        } 
    } 
    swap(&arr[i + 1], &arr[high]); 
    return (i + 1); 
} 
  
/* The main function that implements QuickSort 
 arr[] --> Array to be sorted, 
  low  --> Starting index, 
  high  --> Ending index */
void quickSort(int low, int high) 
{ 
    if (low < high) 
    { 
        /* pi is partitioning index, arr[p] is now 
           at right place */
	int pi = 0;
        pi = partition(low, high); 
  
        /* Separately sort elements before */
        /* partition and after partition */
        quickSort(low, pi - 1); 
        quickSort(pi + 1, high); 
    } 
} 
  
/* Function to print an array */
void printArray() 
{ 
    int i; 
    for (i=0; i < n; i = i+1){
        print_int( arr[i]); 
	printstr(" ");
    }
    printstr("\n");
} 
  
/* Driver program to test above functions */
int main() 
{ 
    quickSort(0, n-1); 
    printstr("Sorted array: "); 
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
