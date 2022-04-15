# Channel et filtre des inputs

# Instruments d'exécution et/ou controlleur
inputs=configuration["inputs"]
akai_channel=inputs["akai"]
akai = ChannelFilter(akai_channel)

pk5_channel=inputs["pk5"]
pk5 = ChannelFilter(pk5_channel)

q49_channel=inputs["q49"]
q49 = ChannelFilter(q49_channel)

fcb_channel=inputs["fcb"]
fcb = ChannelFilter(fcb_channel)

