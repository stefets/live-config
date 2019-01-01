    2: Scene("Mp3PianoPlayer", 
		(Filter(NOTEON) >> KeyFilter(lower=12) >> Call(Mp3PianoPlayer)) //
		(KeyFilter(lower=0, upper=11) >> Call(Mp3PianoPlayerController))
	),
