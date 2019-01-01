    2: Scene("Mp3PianoPlayer", 
		(Filter(NOTEON) >> KeyFilter(lower=12) >> Call(Mp3PianoPlayerLoadFile)) //
		(Filter(NOTEON) >> KeyFilter(lower=0, upper=11) >> Call(Mp3PianoPlayerControl)) //
		(Filter(CTRL) >> Call(Mp3PianoPlayerHandleCTRL))
	),
