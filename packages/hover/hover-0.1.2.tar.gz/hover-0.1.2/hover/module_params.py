# constants for the abstain mechanism
ABSTAIN_DECODED = "ABSTAIN"
ABSTAIN_ENCODED = -1

# constants for label encoding mechanism
ENCODED_LABEL_KEY = "label_encoded"

# constants for annotation internal mechanism
PRODIGY_KEY_TRANSFORM_PREFIX = "___"

# generic logger
import wasabi


def default_logger():
    return wasabi.Printer()


# bokeh hovertool template
def bokeh_hover_tooltip(label=True, text=True, coords=True, index=True, custom={}):
    """
    Create a Bokeh hover tooltip from a template.
    """
    prefix = """<div>\n"""
    suffix = """</div>\n"""

    tooltip = prefix
    if label:
        tooltip += """
        <div>
            <span style="font-size: 16px; color: #966;">
                Label: @label
            </span>
        </div>
        """
    if text:
        tooltip += """
        <div style="word-wrap: break-word; width: 800px; text-overflow: ellipsis; line-height: 80%">
            <span style="font-size: 10px;">
                Text: @text
            </span>
        </div>
        """
    if coords:
        tooltip += """
        <div>
            <span style="font-size: 12px; color: #060;">
                Coordinates: ($x, $y)
            </span>
        </div>
        """
    if index:
        tooltip += """
        <div>
            <span style="font-size: 12px; color: #066;">
                Index: [$index]
            </span>
        </div>
        """
    for _key, _field in custom.items():
        assert _field.startswith("@")
        tooltip += f"""
        <div>
            <span style="font-size: 10px; color: #066;">
                {_key}: {_field}
            </span>
        </div>
        """
    tooltip += suffix
    return tooltip
