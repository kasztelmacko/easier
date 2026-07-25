from easier.config import VALID_PKG_MANAGERS


class PackageManagerNotFoundError(Exception):
    def __init__(self, selected: str, available: list[str]) -> None:
        self.selected = selected
        self.available = available
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        supported = ", ".join(VALID_PKG_MANAGERS)
        if self.available:
            detected = ", ".join(self.available)
            suggestion = ", ".join(
                f"easier create <project> --pkg-manager {name}"
                for name in self.available
            )
            return (
                f"{self.selected} was not found on PATH. "
                f"Detected: {detected}. Try: {suggestion}"
            )
        return (
            f"{self.selected} was not found on PATH. "
            f"None of the supported package managers ({supported}) were detected."
        )
