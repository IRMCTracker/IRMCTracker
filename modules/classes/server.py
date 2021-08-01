from typing import Dict


class Server():
    """Represents a Server.

    Parameters
    ------------
    name: :class:`str`
        the name representing the server
    address: :class:`str`
        the ip-address of the server
    current_players: :class:`int`
        the live number of players on currently on the server
    top_players: :class:`int`
        the highest number of players on the server ever recorded
    latest_version: :class:`str`
        latest recorded the version of the server
    latest_latency: :class:`str`
        latest recorded latency (ping) of the server
    favicon_path: :class:`str`
        path to the favicon of the server
    motd_path: Optional[:class:`str`]
        path to the image of the server's motd
    info_path: Optional[:class:`str`]
        path to the info of the server
    discord: :class:`str`
        link to the server's discord server
    diamond_name: @propery -> :class: `str`
        returns the name of the server with a diamond as a prefix
    """

    def __init__(self, data) -> None:
        self.data: Dict[str, str] = data
        self.name: str = self.get_if_exists_or_none("name") or "  --  "
        self.address: str = self.get_if_exists_or_none("address") or "Not Set"
        self.current_players: int = self.get_if_exists_or_none(
            "current_players") or 0
        self.top_players: int = self.get_if_exists_or_none("top_players") or 0
        self.latest_version: str = self.get_if_exists_or_none(
            "latest_version") or "Not Set"
        self.latest_latency: str = self.get_if_exists_or_none(
            "latest_latency") or "  --  "
        self.favicon_path: str = self.get_if_exists_or_none("favicon_path")
        self.motd_path: str = self.get_if_exists_or_none(
            "motd_path") or "storage/static/banner.png"
        self.info_path: str = self.get_if_exists_or_none(
            "info_path") or "Not Set"
        self.discord: str = self.get_if_exists_or_none("discord") or "Not Set"

    def get_if_exists_or_none(self, name: str):
        return self.data[name] if name in self.data else None

    @property
    def diamond_name(self):
        return f"💎 {self.name}"
