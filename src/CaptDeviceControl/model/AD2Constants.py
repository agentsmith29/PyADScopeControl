class AD2Constants:
    class CapturingState:
        # Capturing States
        @staticmethod
        def RUNNING(description: bool = False):
            if description:
                return "Capturing running"
            return 1

        @staticmethod
        def PAUSED(description: bool= False):
            if description:
                return "Capturing paused"
            return 2

        @staticmethod
        def STOPPED(description: bool= False):
            if description:
                return "Capturing stopped"
            return 3
