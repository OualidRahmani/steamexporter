from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Game:
    appid: int
    name: str
    playtime_minutes: int
    last_played: Optional[datetime]
    has_community_stats: bool
    is_free: bool = False
    release_date: Optional[str] = None
    developers: List[str] = field(default_factory=list)
    publishers: List[str] = field(default_factory=list)
    genres: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    price: Optional[str] = None
    discount: Optional[int] = None
    header_image: Optional[str] = None
    
    @property
    def playtime_hours(self) -> float:
        return self.playtime_minutes / 60