function jmp() {
	OUT="$(python3 ~/jmp.py "$@")"
	EXIT="$?"
	if [ "$EXIT" = "0" ]
	then
		cd "$OUT"
	elif [ "$EXIT" = "1" ]
	then
		if [ "$OUT" != "" ]
		then
			echo "$OUT"	
		fi
	else
		echo "$EXIT"
		echo "Unexpected error occurred."
	fi
}

function jmpa() {
	OUT="$(python3 ~/jmp.py -b / "$@")"
	EXIT="$?"
	if [ "$EXIT" = "0" ]
	then
		cd "$OUT"
	elif [ "$EXIT" = "1" ]
	then
		if [ "$OUT" != "" ]
		then
			echo "$OUT"	
		fi
	else
		echo "$EXIT"
		echo "Unexpected error occurred."
	fi
}

function jmpf() {
	OUT="$(python3 ~/jmp.py -f "$@")"
	EXIT="$?"
	if [ "$EXIT" = "0" ]
	then
		cd "$OUT"
	elif [ "$EXIT" = "1" ]
	then
		if [ "$OUT" != "" ]
		then
			echo "$OUT"	
		fi
	else
		echo "$EXIT"
		echo "Unexpected error occurred."
	fi
}

function jmpd() {
	OUT="$(python3 ~/jmp.py -d "$@")"
	EXIT="$?"
	if [ "$EXIT" = "0" ]
	then
		cd "$OUT"
	elif [ "$EXIT" = "1" ]
	then
		if [ "$OUT" != "" ]
		then
			echo "$OUT"	
		fi
	else
		echo "$EXIT"
		echo "Unexpected error occurred."
	fi
}
