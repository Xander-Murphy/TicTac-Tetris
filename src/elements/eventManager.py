class EventManager:
    
    onQuitGame : list = []

    @classmethod
    def quitGame(cls):
        if len(cls.onQuitGame) != 0:
            for function in cls.onQuitGame:
                function()

    # 