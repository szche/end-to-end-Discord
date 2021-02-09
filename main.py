from gui import GUI


if __name__ == "__main__":
    #Check if the token is already stored in dcToken.txt
    try:
        with open("dcToken.txt", "r") as f:
            token = ''.join(f.readlines()) 
    except:
        print("Could not find a dcToken file")
    window = GUI(token)
    window.configure_loginPage()
    window.configure_mainPage()
    window.showPage(window.loginPage)
    window.run()
