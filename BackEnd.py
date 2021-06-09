from srcgen.statechart_v2 import Statechart_v2
from src.yakindu.rx import Observer
from timer.timer_service import TimerService
import time


class BackEnd:

    class EngineStandByEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("EngineStandBy Triggered")
            # Main.engineStarted = True
            self.main_class.engineStarted = False
            self.main_class.gear = None
            self.main_class.status = None
            self.main_class.speed_change_status = None

    class StartEngineEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Start EngineEvent Triggered")
            # Main.engineStarted = True
            self.main_class.engineStarted = True
            self.main_class.gear = 0
            self.main_class.status = "Ok"

    class FirstGearEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("First GearEvent Triggered")
            self.main_class.gear = 1

    class SecondGearEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Second GearEvent Triggered")
            self.main_class.gear = 2

    class ThirdGearEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("ThirdGearEvent Triggered")
            self.main_class.gear = 3

    class FourthGearEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Fourth GearEvent Triggered")
            self.main_class.gear = 4

    class FifthGearEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Fifth GearEvent Triggered")
            self.main_class.gear = 5

    class StaticEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Static Event Triggered")
            self.main_class.speed_change_status = "Static"

    class AccelleratingEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Accellerating Event Triggered")
            self.main_class.speed_change_status = "Accellerating"

    class SlowingEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Slowing Event Triggered")
            self.main_class.speed_change_status = "Slowing"

    class OkEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Ok Event Triggered")
            self.main_class.status = "Ok"

    class EmergencyBrakeEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("Emergency Brake Triggered")
            self.main_class.status = "EmergencyBrake"

    class InOverLoadingProccessEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("InOverLoadingProccess_ Event Triggered")
            self.main_class.status = "InOverLoading"

    class OverLoadedEventObserver(Observer):
        def __init__(self, outer):
            self.main_class = outer

        def next(self, value=None):
            print("OverLoaded")
            self.main_class.status = "OverLoaded"

    def __init__(self):
        # Instantiates the state machine
        self.sm = Statechart_v2()
        # Instantiates observer for the out events
        self.startEngineEventO = self.StartEngineEventObserver(self)
        self.engineStandByEventO = self.EngineStandByEventObserver(self)
        self.firstGearEventO = self.FirstGearEventObserver(self)
        self.secondGearEventO = self.SecondGearEventObserver(self)
        self.thirdGearEventO = self.ThirdGearEventObserver(self)
        self.fourthGearEventO = self.FourthGearEventObserver(self)
        self.fifthGearEventO = self.FifthGearEventObserver(self)
        self.accelleratingEventO = self.AccelleratingEventObserver(self)
        self.staticEventO = self.StaticEventObserver(self)
        self.slowingEventO = self.SlowingEventObserver(self)
        self.okEventO = self.OkEventObserver(self)
        self.emergencyBrakeEventO = self.EmergencyBrakeEventObserver(self)
        self.inOverLoadingProccessEventO = self.InOverLoadingProccessEventObserver(self)
        self.overLoadedEventO = self.OverLoadedEventObserver(self)
        self.gear = None
        self.engineStarted = None
        self.status = None
        self.speed_change_status = None

    def setup(self):
        # Set the timer service
        self.sm.timer_service = TimerService()
        # Subscribes observers to the state machine's observables
        self.sm.system.start_engine_event_observable.subscribe(self.startEngineEventO)
        self.sm.system.engine_standby_event_observable.subscribe(self.engineStandByEventO)
        self.sm.system.first_gear_event_observable.subscribe(self.firstGearEventO)
        self.sm.system.second_gear_event_observable.subscribe(self.secondGearEventO)
        self.sm.system.third_gear_event_observable.subscribe(self.thirdGearEventO)
        self.sm.system.fourth_gear_event_observable.subscribe(self.fourthGearEventO)
        self.sm.system.fifth_gear_event_observable.subscribe(self.fifthGearEventO)
        self.sm.system.accellerating_event_observable.subscribe(self.accelleratingEventO)
        self.sm.system.static_event_observable.subscribe(self.staticEventO)
        self.sm.system.slowing_event_observable.subscribe(self.slowingEventO)
        self.sm.system.ok_event_observable.subscribe(self.okEventO)
        self.sm.system.emergency_brake_event_observable.subscribe(self.emergencyBrakeEventO)
        self.sm.system.in_over_loading_proccess_event_observable.subscribe(self.inOverLoadingProccessEventO)
        self.sm.system.over_loaded_event_observable.subscribe(self.overLoadedEventO)
        # Enters the state machine; from this point on the state machine is ready to react on incoming event
        self.sm.enter()

    # def run(self):
    #     print("start/gas/brake.")
    #     while not self.sm.is_final():
    #         self.input = input()
    #         if self.input == 'start':
    #             print("start input is" + self.input)
    #             # Raises the On event in the state machine which causes the corresponding transition to be taken
    #             self.sm.user.raise_start_engine_button()
    #         elif self.input == 'gas':
    #             print("gas input is" + self.input)
    #             # Raises the Off event in the state machine
    #             self.sm.user.raise_gas_pressed_button()
    #             # self.print_status()
    #         elif self.input == 'brake':
    #             print("brake input is" + self.input)
    #             # Raises the Off event in the state machine
    #             self.sm.user.raise_brake_pressed_button()
    #             # self.print_status()
    #     self.shutdown()

    def shutdown(self):
        self.sm.exit()

    def print_status(self):
        # Gets the value of the brightness variable
        while True:
            speed = self.sm.system.speed
            print(speed)
            time.sleep(1)

if __name__ == '__main__':
    m = BackEnd()
    m.setup()
    m.run()

