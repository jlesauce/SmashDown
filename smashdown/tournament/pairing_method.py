from enum import Enum


class PairingMethod(Enum):
    RANDOM = 1
    ROUND_ROBIN = 2
    PSEUDO_SWISS_SYSTEM = 3

    def __str__(self):
        return str(self.name)

    @staticmethod
    def to_enum(value: str):
        for pairing_method in PairingMethod:
            if pairing_method.name.lower() == value.lower():
                return pairing_method

            raise ValueError(f"Unsupported pairing method: {value}")
