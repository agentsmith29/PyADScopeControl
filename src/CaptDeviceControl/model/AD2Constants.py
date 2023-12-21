class AD2Constants:
    class CapturingState:
        # Capturing States
        @staticmethod
        def RUNNING(description: bool = False):
            if description:
                return "Capturing running"
            return 1

        @staticmethod
        def PAUSED(description: bool = False):
            if description:
                return "Capturing paused"
            return 2

        @staticmethod
        def STOPPED(description: bool = False):
            if description:
                return "Capturing stopped"
            return 3

    class DeviceState():

        @staticmethod
        def ACQ_NOT_STARTED(description: bool = False):
            if description:
                return "Acquisition not started"
            return 4

        @staticmethod
        def DEV_CAPT_SETUP(description: bool = False):
            if description:
                return "Device setting up"
            return 5

        @staticmethod
        def DEV_CAPT_STREAMING(description: bool = False):
            if description:
                return "Device streaming"
            return 6

        @staticmethod
        def NO_SAMPLES_AVAILABLE(description: bool = False):
            if description:
                return "No samples available"
            return 7

        @staticmethod
        def SAMPLES_AVAILABLE(description: bool = False):
            if description:
                return "Samples streaming"
            return 8
