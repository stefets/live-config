
#
# Pre-buit filters for patches
#

mpk_a = PortFilter(mpk_port_a)
mpk_b = PortFilter(mpk_port_b)
pk5   = PortFilter(mpk_midi) >> ChannelFilter(3)
pk5_filter = pk5
q49   = PortFilter(q49_midi)

# -------------------------------
