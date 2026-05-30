
hook(
    OSCInterface(),
    MemorizeScene("/tmp/hook.memorize_scene"),
    AutoRestart(filenames=["includes/scenes.py",
                           "includes/functions/hook.py",
                           "includes/functions/run.py"])
)