from enum import Enum, auto
from time import sleep


class Criticality(Enum):
    D = auto()
    C = auto()
    B = auto()
    A = auto()


class EncoderBlock:
    def __init__(self, name, criticality, error_resilience=None):
        self.name = name
        self.criticality = criticality
        self.error_resilience = error_resilience  

    def run(self):

        if self.error_resilience:
            print(f"{self.name} running")
            self.error_resilience()
        else:
            print(f"{self.name} running")

        print(f"{self.name} finished")


def sanity_check():
    print("Performing Sanity Check")
    sleep(0.1)


def instruction_retry():
    print("Retrying instruction")
    sleep(0.05)


def ecc():
    print("Applying ECC")
    sleep(0.5)


def tmr():
    print("Using TMR")
    sleep(1)


def checkpoint_restart():
    print("Creating checkpoints for Entropy coding")
    sleep(0.1)


def h264_encode():
    setup = [
        EncoderBlock("Coder control", Criticality.B, error_resilience=sanity_check),
        EncoderBlock("Transform and Quantisation", Criticality.B, error_resilience=instruction_retry),
    ]

    loop = [
        EncoderBlock("Inverse Quantisation and Inverse Transform", Criticality.B, error_resilience=instruction_retry),
        EncoderBlock("Intraprediction", Criticality.C, error_resilience=ecc),
        EncoderBlock("Deblocking filtering", Criticality.A, error_resilience=None),  # None
        EncoderBlock("Frame buffer", Criticality.A, error_resilience=None),  # None
        EncoderBlock("Motion estimation", Criticality.C, error_resilience=ecc),
        EncoderBlock("Motion compensation", Criticality.C, error_resilience=ecc),
        EncoderBlock("Intra-/Intermode decision", Criticality.D, error_resilience=tmr),
        EncoderBlock("Transform and Quantisation", Criticality.B, error_resilience=instruction_retry),
        EncoderBlock("Entropy coding", Criticality.B, error_resilience=checkpoint_restart),
    ]

    for block in setup:
        block.run()

    while True:
        for block in loop:
            block.run()


h264_encode()
