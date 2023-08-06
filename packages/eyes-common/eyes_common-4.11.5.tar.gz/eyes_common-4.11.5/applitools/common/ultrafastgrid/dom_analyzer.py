from typing import Dict

from applitools.common import logger

from .render_request import RGridDom, VGResource
from ..utils import apply_base_url

# from ...selenium.parsers import collect_urls_from_


class DomAnalyzer(object):
    def __init__(self):
        self.resource_cache = {}

    def parse_frame_dom_resources(self, data):  # noqa
        # type: (Dict) -> RGridDom
        base_url = data["url"]
        resource_urls = data.get("resourceUrls", [])
        all_blobs = data.get("blobs", [])
        frames = data.get("frames", [])
        logger.debug(
            """
        parse_frame_dom_resources() call

        base_url: {base_url}
        count blobs: {blobs_num}
        count resource urls: {resource_urls_num}
        count frames: {frames_num}

        """.format(
                base_url=base_url,
                blobs_num=len(all_blobs),
                resource_urls_num=len(resource_urls),
                frames_num=len(frames),
            )
        )
        frame_request_resources = {}
        discovered_resources_urls = set()

        def handle_resources(content_type, content, resource_url):
            # type: (Optional[Text], bytes, Text) -> NoReturn
            logger.debug(
                "handle_resources({0}, {1}) call".format(content_type, resource_url)
            )
            if not content_type:
                logger.debug("content_type is empty. Skip handling of resources")
                return
            for url in collect_urls_from_(content_type, content):
                target_url = apply_base_url(url, base_url, resource_url)
                discovered_resources_urls.add(target_url)

        def get_resource(link):
            # type: (Text) -> VGResource
            logger.debug("get_resource({0}) call".format(link))
            response = self.eyes_connector.download_resource(link)
            return VGResource.from_response(link, response, on_created=handle_resources)

        for f_data in frames:
            f_data["url"] = apply_base_url(f_data["url"], base_url)
            frame_request_resources[f_data["url"]] = self.parse_frame_dom_resources(
                f_data
            ).resource

        for blob in all_blobs:
            resource = VGResource.from_blob(blob, on_created=handle_resources)
            if resource.url.rstrip("#") == base_url:
                continue
            frame_request_resources[resource.url] = resource

        for r_url in set(resource_urls).union(discovered_resources_urls):
            self.resource_cache.fetch_and_store(r_url, get_resource)
        self.resource_cache.process_all()

        # some discovered urls becomes available only after resources processed
        for r_url in discovered_resources_urls:
            self.resource_cache.fetch_and_store(r_url, get_resource)

        for r_url in set(resource_urls).union(discovered_resources_urls):
            val = self.resource_cache[r_url]
            if val is None:
                logger.debug("No response for {}".format(r_url))
                continue
            frame_request_resources[r_url] = val
        self.full_request_resources.update(frame_request_resources)
        return RGridDom(
            url=base_url, dom_nodes=data["cdt"], resources=frame_request_resources
        )
