
pre  = ~Filter(SYSRT_CLOCK) >> ~ChannelFilter(8, 9, 11, 13, 15) 
post = Pass()

run(
    control=control_patch,
    scenes=_scenes,
    pre=pre,
    post=post,
)