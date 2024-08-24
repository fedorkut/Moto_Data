# controller.py
from app.script2 import Script2
from app.script3 import Script3
from app.script4 import Script4
from app.script5 import Script5
from app.dependencies.drivermanager import get_driver_manager

class Controller:
    def __init__(self):
        self.driver_manager = get_driver_manager()

    def setup_driver(self):
        """Sets up the WebDriver using the DriverManager."""
        self.driver_manager.setup_driver()

    def run_dealer_search(self, make, postcode, radius):
        """Runs the dealer search using the DealerSearch class."""
        from app.dealersearch2 import DealerSearch  # Lazy import to avoid circular dependency
        dealer_search = DealerSearch(make, postcode, radius)
        dealer_search.run()

    def run_script2(self):
        """Runs the logic for Script2."""
        script2 = Script2()
        script2.run()

    def run_script3(self):
        """Runs the logic for Script3."""
        script3 = Script3()
        script3.run()

    def run_script4(self):
        """Runs the logic for Script4."""
        script4 = Script4()
        script4.run()

    def run_script5(self):
        """Runs the logic for Script5."""
        script5 = Script5()
        script5.run()

    def execute_all(self, make, postcode, radius):
        """Executes all scripts in sequence."""
        print("Setting up the driver...")
        self.setup_driver()

        print("Running Dealer Search...")
        self.run_dealer_search(make, postcode, radius)

        print("Running Script2...")
        self.run_script2()

        print("Running Script3...")
        self.run_script3()

        print("Running Script4...")
        self.run_script4()

        print("Running Script5...")
        self.run_script5()

        print("All scripts executed successfully. Closing the driver.")
        self.driver_manager.quit_driver()
