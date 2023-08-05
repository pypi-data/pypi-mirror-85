def by_text(text: str) -> str:
    return f"//*[normalize-space(text())='{text}']"


def with_text(text: str) -> str:
    return f"//*[contains(text(),'{text}')]"


def by_attr(name: str, value: str) -> str:
    return f"[{name}='{value}']"


def by_value(value: str) -> str:
    return by_attr("value", value)


def by_xpath(xpath: str) -> str:
    return xpath


def by_css(css: str) -> str:
    return css


def by_title(title: str) -> str:
    return by_attr("title", title)


def by_id(id_: str) -> str:
    return f"#{id_}"


def by_name(name: str) -> str:
    return by_attr("name", name)


def by_link_text(link_text: str) -> str:
    return by_xpath(f"//a[normalize-space(text())='{link_text}']")


def by_partial_link_text(partial_link_text: str) -> str:
    return by_xpath(f"//a[contains(text(),'{partial_link_text}')]")


def by_class_name(class_name: str) -> str:
    if " " in class_name:
        class_name = class_name.replace(" ", ".")
    return f".{class_name}"


def by_tag_name(tag_name: str) -> str:
    return f"{tag_name}"
