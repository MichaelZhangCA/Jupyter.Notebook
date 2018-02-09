from logger import Logger

def main():
    with Logger("test service") as log:
        log.loginfo("run testing", "test successfully")
        print("done!!!")

if (__name__ == "__main__"):
    main()
