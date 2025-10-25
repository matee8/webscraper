import dataclasses
from typing import Any, Dict, List, Literal, Optional

@dataclasses.dataclass(frozen=True)
class CrawlRules:
    allow: List[str] = dataclasses.field(default_factory=list)
    deny: List[str] = dataclasses.field(default_factory=list)

@dataclasses.dataclass(frozen=True)
class TaskConfig:
    mode: Literal['trafilatura', 'zotero']
    start_urls: List[str]
    name: Optional[str] = None
    javascript: bool = False
    crawl: bool = False
    handle_pdfs: bool = False
    domain: Optional[str] = None
    crawl_rules: Optional[CrawlRules] = None

    def __post_init__(self):
        if self.crawl and not self.domain:
            raise ValueError('`domain` must be set if `crawl` is true.')

        if self.crawl and not self.crawl_rules:
            raise ValueError('`crawl_rules` must be set if `crawl` is true.')


@dataclasses.dataclass(frozen=True)
class AppConfig:
    tasks: List[TaskConfig]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        tasks: List[TaskConfig] = []

        for task in data.get('tasks', []):
            rules = task.pop('crawl_rules', None)
            rules = CrawlRules(**rules) if rules else None
            tasks.append(TaskConfig(crawl_rules=rules, **task))

        return cls(tasks=tasks)
