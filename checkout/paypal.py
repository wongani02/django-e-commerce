import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AfDx3yQgVBzG5LfDvijqX53CGeGf2cdxY8tCsf9xS-vgkcT3yJUPJ_e3uKbnfMHUr6yH-SgnXZ2N4rEi"
        self.client_secret = "ED144Nuf2a4o7Y6rr98NttNsN6xvFKi8pNur2EhlnEnxvYZHABptrkbyQVumdbg9K2lukoMOLcadIxkF"
        # self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
        