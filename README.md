## Text Obfuscator

Obfuscate your message with [Text Obfuscator]()

[![CI](https://github.com/luxiaba/TextObfuscator/actions/workflows/ci.yaml/badge.svg)](https://github.com/luxiaba/textobfuscator/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/TextObfuscator?color=blue&label=PyPI)](https://pypi.org/project/textobfuscator/)
[![Python 3.8.7](https://img.shields.io/badge/python-3.8.7-blue.svg)](https://www.python.org/downloads/release/python-387/)
[![codecov](https://codecov.io/gh/luxiaba/TextObfuscator/branch/main/graph/badge.svg?token=WlaPtdYdpg)](https://codecov.io/gh/luxiaba/textobfuscator)


### Installation
```
pip install -U textobfuscator
```

### Usage

```python
import random
from textobfuscator.obfuscator import TextObfuscator

# 1. Replace char.
# First, now we define rules: replace chars groups.
CHARS_GROUPS_SOURCE_MAP = (
  ["😯", "🤣"],
  ["❌", "✅"],
)

# 2. Format(Optional)
# Second, let's make some rules to fill the vars that we inserted.
FORMAT_PREFIX_RULES = {
  "fake_name": lambda: random.choice(("John", "Min", "William")),
  "random_weather": lambda: random.choice(("cloudy", "rainy", "sunny", "windy"))
}

obfuscator = TextObfuscator(
   replace_source_map=CHARS_GROUPS_SOURCE_MAP,
   format_prefix_rules=FORMAT_PREFIX_RULES,
)
```

Now we have an instance of `TextObfuscator`: `obfuscator`, let's do some obfuscations.

```python
from textobfuscator.processor import BreakWord, ObfuscationConfig, Replace

# For each obfuscation, we may specify different rules, such as controls for different words or the number of substitutions, so we make rule here first.
BREAK_WORDS_RULES = [
   # We break the word `hello` twice, and put `*` into the middle, like `h*el*lo`
   BreakWord(word="hello", places=2, fill="*"),
   # We break the word `world` once, and put `-` into the middle, like `wor-ld`
   BreakWord(word="world", places=1, fill="-"),
]
OBFUSCATOR_CONFIG = ObfuscationConfig(
   # During the entire obfuscation process, we only replace 1 times.
   replaces=Replace(count=1),
   break_words=BREAK_WORDS_RULES,
)

# OK, let's do the obfuscation.

>>> original1 = "hello world!"
>>> obfuscated = obfuscator.obfuscate(original1, config=OBFUSCATOR_CONFIG)
>>> print(obfuscated)
>>> h*ell*o wor-ld!

>>> original2 = "❌ hi {fake_name}, today's weather is {random_weather} 😯"

>>> obfuscated = obfuscator.obfuscate(original2, config=OBFUSCATOR_CONFIG)
>>> print(obfuscated)
>>> ❌ hi John, today's weather is windy 🤣

# Once more.
>>> obfuscated = obfuscator.obfuscate(original2, config=OBFUSCATOR_CONFIG)
>>> print(obfuscated)
>>> ✅ hi Min, today's weather is sunny 😯
```

## Obfuscation Detail
1. Split content into segments by every args position.
2. Break words.
   1. Break words on each segment.
   2. Merge all segments and put back all key args in places.
3. Replace.
   1. Temporarily remove all key args.
   2. Replace matching chars according to the given mapping table and config.
   3. Put back all key args that removed on above in places.
4. Format.
   1. Merge the `pre-defined` key args and given key args.
      Here `pre-defined` args means we can create custom var generation rules.
      For example, we can pass config like below to let all vars stars wth `digit` to autofill in with a real digit, and all vars starts with `letter` to autofill in with a real letter.
      And the var with the same name will also be filled with the same value.
      ```python
      # config
      # {
      #     "digit": lambda: random.choice(string.digits),
      #     "letter": lambda: random.choice(string.ascii_letters),
      # }

      # before
      >>> "{digit1} {digit2} {letter2} {digit2}"
      # after
      >>> 8 6 z 6
      ```
   2. Format and return the content.
      Put all args we get to the content, and keep those unknown args in original place.
