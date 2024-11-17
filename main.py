from ui.gui import init_gui

if __name__ == "__main__":
    try:
        init_gui()  
    except KeyboardInterrupt:
        print("Program interrupted by user")