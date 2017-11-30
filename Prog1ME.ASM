INICIO:	LD A, (10H)
		INC A
			LD E, A
			LD H, B
			LD L, C
		ADD A, E
		SLA B
			PUSH AF
			PUSH BC
			POP AF
			POP BC
		DEC C
			LD (200H), A
			LD (IX), B
			LD (HL), C
			PUSH HL
			PUSH DE
			POP HL
			POP DE
		HALT
		END INICIO