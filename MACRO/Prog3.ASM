CARGA:	MACRO #a1, #a2, #a3
			LD #a1, A
			LD #a2, B
			LD #a3, C

CAMBIA:	MACRO #a4, #a5
			PUSH #a4
			PUSH #a5
			POP #a4
			POP #a5
		MEND

INICIO:	LD A, (10H)
		INC A
		CARGA E, H, L
		ADD A, E
		SLA B
		CAMBIA AF, BC
		DEC C
		CARGA (200H), (IX), (HL)
		CAMBIA HL, DE
		HALT
		END INICIO