from re import match

from robot.api.deco import keyword

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import (
    EventFiringWebElement
)

from SeleniumLibrary import ElementFinder, LibraryComponent

from ._version import __version__


# From SeleniumLibrary CustomLocator
def _as_array(a):
    if hasattr(a, "__len__") and not isinstance(a, str):
        return a
    else:
        return [a]


# From SeleniumLibrary ElementFinder
def _get_parent(parent):
    if isinstance(parent, (WebElement, EventFiringWebElement)):
        return parent
    return None


def _get_xpath_function(value, criteria):
    re_match = match(r'/(.+)/([smix]*)', criteria)

    if re_match:
        regexp = re_match.group(1)
        flags = re_match.group(2)
        flags_str = f', "{flags}"' if flags else ''
        return f'matches({value}, "{regexp}"{flags_str})'

    return f'normalize-space({value})="{criteria}"'


def _filter_out_nones(a):
    return [i for i in a if i]


class TestingLibrarySelectorsPlugin(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.element_finder = ElementFinder(ctx)

        self._function_mappings = dict(
            alttext=self._get_alt_text_xpath,
            label=self._get_label_xpath,
            placeholder=self._get_placeholder_xpath,
            testid=self._get_testid_xpath,
            text=self._get_text_xpath,
            title=self._get_title_xpath,
        )

        for name, xpath_function in self._function_mappings.items():
            function = self._get_find_function(xpath_function)
            self.element_finder.register(name, function, persist=True)

    def _get_find_function(self, get_xpath_function):
        def _find_function(parent, criteria, tag, constraints):
            locator = get_xpath_function(parent, criteria, tag, constraints)

            return self.element_finder.find(
                locator, tag=tag, parent=_get_parent(parent), required=False)

        return _find_function

    def _get_attribute_xpath(self, attribute, criteria, limit_tags=None):
        if not limit_tags:
            limit_tags = ['*']

        _xfn = _get_xpath_function
        return '|'.join(
            f'//{i}[{_xfn(f"@{attribute}", criteria)}]' for i in limit_tags)

    def _get_alt_text_xpath(self, parent, criteria, tag, constraints):
        return self._get_attribute_xpath('alt', criteria, [
            'img', 'input', 'area'
        ])

    def _get_label_xpath(self, parent, criteria, tag, constraints):
        label = f'//label[{_get_xpath_function("text()", criteria)}]'
        input_in_label = f'{label}/input'
        text_in_label_child = (
            f'//label/*[{_get_xpath_function("text()", criteria)}]/'
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

        return locator

    def _get_placeholder_xpath(self, parent, criteria, tag, constraints):
        return self._get_attribute_xpath('placeholder', criteria)

    def _get_testid_xpath(self, parent, criteria, tag, constraints):
        return self._get_attribute_xpath('data-testid', criteria)

    def _get_text_xpath(self, parent, criteria, tag, constraints):
        return f'//*[{_get_xpath_function("text()", criteria)}]'

    def _get_title_xpath(self, parent, criteria, tag, constraints):
        title_attribute = f'//*[@title="{criteria}"]'
        svg_title = (
            '//*[name()="svg"]/'
            f'*[name()="title" and {_get_xpath_function("text()", criteria)}]')

        return f'{title_attribute}|{svg_title}'

    @keyword
    def get_xpath(self, locator):
        try:
            strategy, criteria = locator.split(':')
        except ValueError:
            raise ValueError(
                'Locator must be given as strategy:criteria format.')

        if strategy not in self._function_mappings:
            keys = list(self._function_mappings.keys())
            keys_str = f'{", ".join(keys[:-1])} or {keys[-1]}'
            raise ValueError(f'Strategy must be {keys_str}.')

        return self._function_mappings.get(strategy)(
            None, criteria, None, None)
