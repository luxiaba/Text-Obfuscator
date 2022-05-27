from textobfuscator.auxiliary import DEFAULT_FORMAT_PREFIX_RULES, MAP_SIMPLE_MIX_SOURCE
from textobfuscator.obfuscator import TextObfuscator
from textobfuscator.processor import BreakWord, ObscureConfig, Replace

TEXT_OBFUSCATOR = TextObfuscator(
    replace_source_map=MAP_SIMPLE_MIX_SOURCE,
    format_prefix_rules=DEFAULT_FORMAT_PREFIX_RULES,
)
OBFUSCATOR_CONFIG = ObscureConfig(
    replaces=Replace(count=2),
    break_words=[
        BreakWord(word="hello", places=2, fill="*"),
        BreakWord(word="world", places=1, fill="-"),
    ],
)


def test_obfuscator():
    """Test Obfuscator."""
    assert OBFUSCATOR_CONFIG.is_valid()

    original = "hello world!"
    obfuscated = TEXT_OBFUSCATOR.obfuscate(original, config=OBFUSCATOR_CONFIG)
    assert obfuscated.count("*") == 2
    assert obfuscated.count("-") == 1

    original2 = "A {letter_3} {letter_2} {letter_3} {digit_2} A {symbol} {unknown}"
    obfuscated = TEXT_OBFUSCATOR.obfuscate(original2, config=OBFUSCATOR_CONFIG)
    output_list = list(obfuscated)
    assert output_list[1] == output_list[3]
    assert hasattr(output_list[4], "isdigit")
    assert not output_list[-2].isdigit()
    assert "{unknown}" in original2
