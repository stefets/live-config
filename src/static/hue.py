
#
# Philips Hue Patches
#

# HueScene(ZoneId, SceneName)
# HueBlackout(ZoneId)

studio=2
HueNormal=Call(HueScene(studio, "Normal"))
HueGalaxie=Call(HueScene(studio, "Galaxie"))
HueGalaxieMax=Call(HueScene(studio, "GalaxieMax"))
HueDemon=Call(HueScene(studio, "Demon"))
HueDetente=Call(HueScene(studio, "Détente"))
HueVeilleuse=Call(HueScene(studio, "Veilleuse"))
HueLecture=Call(HueScene(studio, "Lecture"))
HueSsFullBlanc=Call(HueScene(studio, "SsFullBlanc"))
HueSoloRed=Call(HueScene(studio, "SoloRed"))

cuisine=4
HueCuisine=Call(HueScene(cuisine, "Minimal"))

chambre=1
HueChambreMaitre=Ctrl(3, 100) >> Call(HueScene(chambre, "Normal"))

HueStudioOff=[
    Call(HueBlackout(2))
]

HueAllOff=[
    Call(HueBlackout(1)),
    Call(HueBlackout(2)),
    Call(HueBlackout(4)),
]

p_hue = Filter(NOTEON) >> [
    KeyFilter(notes=[101]) >> HueNormal,
    KeyFilter(notes=[102]) >> HueDetente,
    KeyFilter(notes=[103]) >> HueLecture,
    KeyFilter(notes=[104]) >> HueVeilleuse,
    KeyFilter(notes=[105]) >> HueGalaxie,
    KeyFilter(notes=[106]) >> HueGalaxieMax,
    KeyFilter(notes=[107]) >> HueDemon,
    KeyFilter(notes=[108]) >> HueStudioOff,
    KeyFilter(notes=[109]) >> Ctrl(3, 50) >> HueLecture,
    KeyFilter(notes=[116]) >> HueCuisine
]
