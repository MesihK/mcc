#!/bin/sh
mars=~/Downloads/Mars4_5.jar

rm asm_* 2>/dev/null

for f in *.c
do
	gcc -I inc $f 
	cp $f "asm_$f"
	cat inc/sys_mips.h >> "asm_$f"
	python ../mcc "asm_$f" out.asm
	rm ast
	asm=$(java -jar $mars out.asm | tail -n +3 )
	ccom=$(./a.out)
	rm a.out
	rm out.asm
	rm "asm_$f"
	if [ "$asm" == "$ccom" ]; then
		echo $f Succesfull!
	else
		echo $f Failed!
		echo asm:
		echo "$asm"
		echo c:
		echo "$ccom"
		echo ---------
	fi
done
