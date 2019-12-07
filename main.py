"""
The entry point of the extension.
"""

import logging
import urllib.parse

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

# Use this to log messages
LOGGER = logging.getLogger(__name__)

# URL encode
def urlencode(qp):
    return urllib.parse.urlencode(qp)


class IMDBExtension(Extension):

    def __init__(self):
        super(IMDBExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        """
        Render one item.
        """

        items = list()

        # Only add item to the list of an argument is given
        if event.get_argument():
            LOGGER.info('Showing IMDb search for "{}"'.format(event.get_argument()))
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Search on IMDb',
                description='Search for "{}".'.format(event.get_argument()),
                on_enter=OpenUrlAction(
                    'https://www.imdb.com/find?{}'.format(
                        urlencode({'q': event.get_argument(), 's': 'all'})
                    ))
                )
            )

        return RenderResultListAction(items)

if __name__ == '__main__':
    # Start the extension web socket
    IMDBExtension().run()
