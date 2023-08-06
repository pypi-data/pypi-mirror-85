# import asyncio
from typing import List
from eiprice.httpclient.adapters.asynchronous import gather_with_concurrency
from eiprice.httpclient.adapters.specs.http import DownloadSpec
from eiprice.httpclient.commands.action import Action
from eiprice.httpclient.core.synchronous import RequestSyncDownloader
 

class SyncDownloadSingleURL(Action):
    def __init__(self, spec: DownloadSpec):
        self.spec = spec
        self.downloader = RequestSyncDownloader()

    def execute(self):
        return self.downloader.execute(
            self.spec.method.value,
            self.spec.url,
            headers=self.spec.headers,
            params=self.spec.params,
            json=self.spec.json,
            payload=self.spec.data,
            proxies=self.spec.proxies,
        )
 