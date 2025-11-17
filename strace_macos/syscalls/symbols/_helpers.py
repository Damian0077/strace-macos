"""Helper functions for creating decoders."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def make_flag_decoder(flag_map: dict[int, str]) -> Callable[[int], str]:
    def decoder(value: int) -> str:
        if value == 0:
            return "0"
        flags = [name for val, name in flag_map.items() if value & val]
        return "|".join(flags) if flags else hex(value)

    return decoder


def make_const_decoder(const_map: dict[int, str]) -> Callable[[int], str]:
    def decoder(value: int) -> str:
        return const_map.get(value, str(value))

    return decoder
