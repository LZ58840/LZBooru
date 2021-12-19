def GregDaemon(local_handler):
    print("An action was performed.")
    local_handler.enter(60, 1, GregDaemon, (local_handler,))