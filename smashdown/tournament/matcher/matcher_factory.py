from smashdown.tournament.matcher.pseudo_swiss_matcher import PseudoSwissMatcher
from smashdown.tournament.matcher.random_matcher import RandomMatcher
from smashdown.tournament.matcher.round_robin_matcher import RoundRobinMatcher
from smashdown.tournament.pairing_method import PairingMethod


class MatcherFactory:

    @staticmethod
    def create_matcher(pairing_method=PairingMethod.RANDOM):
        match pairing_method:
            case pairing_method.RANDOM:
                return RandomMatcher()
            case pairing_method.ROUND_ROBIN:
                return RoundRobinMatcher()
            case pairing_method.PSEUDO_SWISS_SYSTEM:
                return PseudoSwissMatcher()
            case _:
                raise ValueError(f"Unsupported matching method: {pairing_method}")
