# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging

from scrapy import signals
from scrapy.utils.boto import is_botocore
from six.moves.urllib.parse import urlparse
from twisted.internet import threads

from scrapy_warc.warcio import ScrapyWarcIo, warc_date


class WarcioMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings, crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        job_dir = self.settings["JOBDIR"] or ""
        s3_dir = self.settings["S3DIR"]
        self.log.info('trying to sync warc files to s3')
        import os
        if s3_dir:
            for root, dirs, files in os.walk(job_dir, topdown=False):
                for name in files:
                    if ".warc.gz" in name:
                        self.storage.store(name, os.path.join(root, name))
            self.log.info('synced warc files to s3')

    def __init__(self, settings, stats):
        self.warcio = ScrapyWarcIo(settings)
        self.stats = stats
        self.settings = settings
        self.job_dir = self.settings["JOBDIR"] or ""
        self.s3_dir = self.settings["S3DIR"]
        if self.s3_dir:
            self.storage = S3Storage(self.s3_dir)
        self.log = logging.getLogger(__name__)

    def process_request(self, request, spider):
        request.meta["WARC-Date"] = warc_date()
        return None

    def process_response(self, request, response, spider):
        self.warcio.write(response, request)
        return response


class S3Storage:
    def __init__(self, uri, access_key=None, secret_key=None, acl=None):
        # BEGIN Backward compatibility for initialising without keys (and
        # without using from_crawler)
        no_defaults = access_key is None and secret_key is None
        if no_defaults:
            from scrapy.utils.project import get_project_settings

            settings = get_project_settings()
            if "AWS_ACCESS_KEY_ID" in settings or "AWS_SECRET_ACCESS_KEY" in settings:
                import warnings
                from scrapy.exceptions import ScrapyDeprecationWarning

                warnings.warn(
                    "Initialising `scrapy.extensions.feedexport.S3FeedStorage` "
                    "without AWS keys is deprecated. Please supply credentials or "
                    "use the `from_crawler()` constructor.",
                    category=ScrapyDeprecationWarning,
                    stacklevel=2,
                )
                access_key = settings["AWS_ACCESS_KEY_ID"]
                secret_key = settings["AWS_SECRET_ACCESS_KEY"]
        # END Backward compatibility
        u = urlparse(uri)
        self.bucketname = u.hostname
        self.access_key = u.username or access_key
        self.secret_key = u.password or secret_key
        self.path = u.path[1:]  # remove first "/"
        self.is_botocore = is_botocore()
        self.acl = acl
        if self.is_botocore:
            import botocore.session

            session = botocore.session.get_session()
            self.s3_client = session.create_client(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )
        else:
            import boto

            self.connect_s3 = boto.connect_s3

    @classmethod
    def from_crawler(cls, crawler, uri):
        return cls(
            uri=uri,
            access_key=crawler.settings["AWS_ACCESS_KEY_ID"],
            secret_key=crawler.settings["AWS_SECRET_ACCESS_KEY"],
            acl=crawler.settings["FEED_STORAGE_S3_ACL"] or None,
        )

    def store(self, keyname, file):
        return threads.deferToThread(self._store, keyname, file)

    def _store(self, keyname, fp):
        with open(fp, mode='rb') as gz:
            kwargs = {"ACL": self.acl} if self.acl else {}
            self.s3_client.put_object(
                Bucket=self.bucketname, Key=self.path + keyname, Body=gz, **kwargs
            )
