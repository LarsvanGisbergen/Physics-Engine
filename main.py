from ui import PygameWindow

def main():
    width = 1000
    height = 800

    window = PygameWindow(width, height) 
    framerate = 20 
    window.run(framerate)

if __name__ == "__main__":
    main()