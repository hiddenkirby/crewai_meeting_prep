import os
from exa_py import Exa
from langchain.agents import tool

class ExaSearchTool:
    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return ExaSearchTool._exa().search(f"{query}", use_autoprompt=True, num_results=3)

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return ExaSearchTool._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(ids: list[str]):
        """
        Get the contents of webpages.
        The `ids` parameter must be a list of IDs (or URLs) returned from `search`.
        """
        contents = str(ExaSearchTool._exa().get_contents(ids))
        print(contents)
        # Split the returned contents on "URL:" for demonstration/truncation
        contents_parts = contents.split("URL:")
        # Truncate each chunk to 1000 chars for brevity
        truncated_parts = [part[:1000] for part in contents_parts]
        return "\n\n".join(truncated_parts)

    def tools():
        return [
            ExaSearchTool.search,
            ExaSearchTool.find_similar,
            ExaSearchTool.get_contents,
        ]

    def _exa():
        return Exa(api_key=os.environ["EXA_API_KEY"])
