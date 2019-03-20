int main(){
	int array[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
	int a = 5;
	int b = a;

	a = a*b;
	a++;

	if(a > 4) {
		b = 3;
	}

	switch(b){
		case 1:
			a = 1;
			break;
		case 2:
			a = 2;
			break;
		default :
			a = 0;
			break;
	}


	int i = 0;
	while(i<10){
		b++;
		array[i] = array[i]++;
		i++;
	}
}
