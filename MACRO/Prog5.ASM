DEFINE:	MACRO #reg1, #reg2
	EX#reg1#reg2:	MACRO
						PUSH #reg1
						PUSH #reg2
						POP #reg1
						POP #reg2
					MEND
		MEND
INICIO:	LD A,B
		DEFINE BC, HL
		LD C, D
		EXBCHL
		HALT
		END INICIO