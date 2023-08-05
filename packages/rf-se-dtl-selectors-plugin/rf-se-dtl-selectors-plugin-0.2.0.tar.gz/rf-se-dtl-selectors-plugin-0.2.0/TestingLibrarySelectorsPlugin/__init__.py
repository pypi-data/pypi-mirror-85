from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import (
    EventFiringWebElement
)

from SeleniumLibrary import ElementFinder, LibraryComponent
from SeleniumLibrary.errors import ElementNotFound

from ._version import __version__


# From SeleniumLibrary ElementFinder
def _get_parent(parent):
    if isinstance(parent, (WebElement, EventFiringWebElement)):
        return parent
    return None


# From SeleniumLibrary CustomLocator
def _as_array(a):
    if hasattr(a, "__len__") and not isinstance(a, str):
        return a
    else:
        return [a]


def _filter_out_nones(a):
    return [i for i in a if i]


class TestingLibrarySelectorsPlugin(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.element_finder = ElementFinder(ctx)

        for name, function in [
            ('alttext', self._find_by_alt_text,),
            ('label', self._find_by_label,),
            ('placeholder', self._find_by_placeholder,),
            ('testid', self._find_by_testid,),
            ('text', self._find_by_text,),
            ('title', self._find_by_title,),
        ]:
            self.element_finder.register(name, function, persist=True)

    def _find_by_attribute(
            self,
            attribute,
            parent,
            criteria,
            tag,
            constraints,
            limit_tags=None):
        if not limit_tags:
            limit_tags = ['*']

        locator = '|'.join(
            f'//{i}[@{attribute}="{criteria}"]' for i in limit_tags)
        return self.element_finder.find(
            locator, tag=tag, parent=_get_parent(parent), required=False)

    def _find_by_alt_text(self, parent, criteria, tag, constraints):
        return self._find_by_attribute(
            'alt', parent, criteria, tag, constraints, limit_tags=[
                'img', 'input', 'area'])

    def _find_by_label(self, parent, criteria, tag, constraints):
        label = f'//label[normalize-space(text())="{criteria}"]'
        input_in_label = f'{label}/input'
        text_in_label_child = (
            f'//label/*[normalize-space(text())="{criteria}"]/'
            'following-sibling::input')
        aria_label = f'//input[@aria-label="{criteria}"]'

        locator = f'{input_in_label}|{text_in_label_child}|{aria_label}'

        elements = self.element_finder.find(
            label, tag=tag, parent=_get_parent(parent), required=False)

        if elements:
            for_l = _filter_out_nones(
                e.get_attribute('for') for e in _as_array(elements))
            if for_l:
                input_id = f'//input[@id="{" or ".join(for_l)}"]'
                locator = f'{input_id}|{locator}'

            id_l = _filter_out_nones(
                e.get_attribute('id') for e in _as_array(elements))
            if id_l:
                labelledby = f'//input[@aria-labelledby="{" or ".join(id_l)}"]'
                locator = f'{labelledby}|{locator}'

        return self.element_finder.find(
            locator, tag=tag, parent=_get_parent(parent), required=False)

    def _find_by_placeholder(self, parent, criteria, tag, constraints):
        return self._find_by_attribute(
            'placeholder', parent, criteria, tag, constraints)

    def _find_by_testid(self, parent, criteria, tag, constraints):
        return self._find_by_attribute(
            'data-testid', parent, criteria, tag, constraints)

    def _find_by_text(self, parent, criteria, tag, constraints):
        locator = f'//*[normalize-space(text())="{criteria}"]'
        return self.element_finder.find(
            locator, tag=tag, parent=_get_parent(parent), required=False)

    def _find_by_title(self, parent, criteria, tag, constraints):
        title_attribute = f'//*[@title="{criteria}"]'
        svg_title = (
            f'//*[name()="svg"]/*[name()="title" and text()="{criteria}"]')

        locator = f'{title_attribute}|{svg_title}'
        return self.element_finder.find(
            locator, tag=tag, parent=_get_parent(parent), required=False)
