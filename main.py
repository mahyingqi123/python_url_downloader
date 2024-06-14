from UserInterface import UI
from multiprocessing import freeze_support
if __name__ == "__main__":
    freeze_support()
    ui = UI()
    ui.run()