
#
# Pre-buit filters for patches
#

mpk_a_filter = [PortFilter(mpk249_port_a), PortFilter(mpk261_port_a)]
mpk_b_filter = [PortFilter(mpk249_port_b), PortFilter(mpk261_port_b)]
pk5_filter   = [PortFilter(mpk249_midi), PortFilter(mpk261_midi)] >> ChannelFilter(3)

# -------------------------------
