import pytest
from blockkit import (
    Actions,
    Context,
    Divider,
    Header,
    ImageBlock,
    Input,
    PlainText,
    PlainTextInput,
    Section,
    UsersSelect,
)
from blockkit.elements import Button, Image
from blockkit.objects import MarkdownText
from pydantic import ValidationError


def test_builds_actions():
    assert Actions(
        elements=[
            Button(text=PlainText(text="text"), action_id="action_id_button"),
            UsersSelect(
                placeholder=PlainText(text="placeholder"), action_id="action_id_select"
            ),
        ],
        block_id="block_id",
    ).build() == {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "text"},
                "action_id": "action_id_button",
            },
            {
                "type": "users_select",
                "placeholder": {"type": "plain_text", "text": "placeholder"},
                "action_id": "action_id_select",
            },
        ],
        "block_id": "block_id",
    }


def test_actions_excessive_block_id_raises_exception():
    with pytest.raises(ValidationError):
        Actions(
            elements=[Button(text=PlainText(text="text"), action_id="action_id")],
            block_id="b" * 256,
        )


def test_actions_empty_elements_raise_exception():
    with pytest.raises(ValidationError):
        Actions(elements=[])


def test_actions_excessive_elements_raise_exception():
    with pytest.raises(ValidationError):
        Actions(
            elements=[
                Button(text=PlainText(text=f"text"), action_id=f"action_id")
                for _ in range(6)
            ]
        )


def test_builds_context():
    assert Context(
        elements=[
            Image(image_url="http://placekitten.com/100/100", alt_text="kitten"),
            MarkdownText(text="*markdown* text"),
        ],
        block_id="block_id",
    ).build() == {
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "http://placekitten.com/100/100",
                "alt_text": "kitten",
            },
            {"type": "mrkdwn", "text": "*markdown* text"},
        ],
        "block_id": "block_id",
    }


def test_context_excessive_block_id_raises_exception():
    with pytest.raises(ValidationError):
        Context(
            elements=[MarkdownText(text="*markdown* text")],
            block_id="b" * 256,
        )


def test_context_empty_elements_raise_exception():
    with pytest.raises(ValidationError):
        Context(elements=[])


def test_context_excessive_elements_raise_exception():
    with pytest.raises(ValidationError):
        Context(elements=[MarkdownText(text="*markdown* text") for _ in range(11)])


def test_builds_divider():
    assert Divider(block_id="block_id").build() == {
        "type": "divider",
        "block_id": "block_id",
    }


def test_builds_header():
    assert Header(text=PlainText(text="text"), block_id="block_id").build() == {
        "type": "header",
        "text": {"type": "plain_text", "text": "text"},
        "block_id": "block_id",
    }


def test_header_excessive_block_id_raises_exception():
    with pytest.raises(ValidationError):
        Header(
            text=PlainText(text="text"),
            block_id="b" * 256,
        )


def test_header_excessive_text_raises_exception():
    with pytest.raises(ValidationError):
        Header(text=PlainText(text="t" * 151))


def test_builds_image_block():
    assert ImageBlock(
        image_url="http://placekitten.com/300/200",
        alt_text=PlainText(text="kitten"),
        title=PlainText(text="kitten"),
        block_id="block_id",
    ).build() == {
        "type": "image",
        "image_url": "http://placekitten.com/300/200",
        "alt_text": {"type": "plain_text", "text": "kitten"},
        "title": {"type": "plain_text", "text": "kitten"},
        "block_id": "block_id",
    }


def test_image_block_excessive_block_id_raises_exception():
    with pytest.raises(ValidationError):
        ImageBlock(
            image_url="http://placekitten.com/300/200",
            alt_text=PlainText(text="kitten"),
            block_id="b" * 256,
        )


def test_image_block_excessive_alt_text_raises_exception():
    with pytest.raises(ValidationError):
        ImageBlock(
            image_url="http://placekitten.com/300/200",
            alt_text=PlainText(text="k" * 2001),
        )


def test_image_block_excessive_alt_text_raises_exception():
    with pytest.raises(ValidationError):
        ImageBlock(
            image_url="http://placekitten.com/300/200",
            alt_text=PlainText(text="kitten"),
            title=PlainText(text="k" * 2001),
        )


def test_builds_input():
    assert Input(
        label=PlainText(text="label"),
        element=PlainTextInput(action_id="action_id"),
        dispatch_action=True,
        block_id="block_id",
        hint=PlainText(text="hint"),
        optional=True,
    ).build() == {
        "type": "input",
        "label": {"type": "plain_text", "text": "label"},
        "element": {"type": "plain_text_input", "action_id": "action_id"},
        "dispatch_action": True,
        "block_id": "block_id",
        "hint": {"type": "plain_text", "text": "hint"},
        "optional": True,
    }


def test_input_excessive_block_id_raises_exception():
    with pytest.raises(ValidationError):
        Input(
            label=PlainText(text="label"),
            element=PlainTextInput(action_id="action_id"),
            block_id="b" * 256,
        )


def test_input_excessive_label_raises_exception():
    with pytest.raises(ValidationError):
        Input(
            label=PlainText(text="l" * 2001),
            element=PlainTextInput(action_id="action_id"),
        )


def test_input_excessive_hint_raises_exception():
    with pytest.raises(ValidationError):
        Input(
            label=PlainText(text="label"),
            element=PlainTextInput(action_id="action_id"),
            hint=PlainText(text="h" * 2001),
        )


def test_builds_section():
    assert Section(
        text=MarkdownText(text="*markdown* text"),
        block_id="block_id",
        fields=[MarkdownText(text="field 1"), MarkdownText(text="field 2")],
        accessory=Button(text=PlainText(text="button"), action_id="action_id"),
    ).build() == {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*markdown* text"},
        "block_id": "block_id",
        "fields": [
            {"type": "mrkdwn", "text": "field 1"},
            {"type": "mrkdwn", "text": "field 2"},
        ],
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": "button"},
            "action_id": "action_id",
        },
    }


def test_empty_section_raises_exception():
    with pytest.raises(ValidationError):
        Section()


def test_section_excessive_block_id_raises_exception():
    with pytest.raises(ValidationError):
        Section(text=MarkdownText(text="*markdown* text"), block_id="b" * 256)


def test_section_excessive_text_raises_exception():
    with pytest.raises(ValidationError):
        Section(text=MarkdownText(text="t" * 3001))


def test_section_empty_fields_raises_exception():
    with pytest.raises(ValidationError):
        Section(fields=[])


def test_section_excessive_fields_raises_exception():
    with pytest.raises(ValidationError):
        Section(fields=[MarkdownText(text=f"field {f}") for f in range(11)])


def test_section_excessive_fields_text_raises_exception():
    with pytest.raises(ValidationError):
        Section(
            fields=[MarkdownText(text="field 1"), MarkdownText(text="f" * 2001)],
        )
