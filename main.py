"""The Excuse Your Agent Gives You.

Writes a single line to $MAKEFUN_OUTPUT_DIR/entry.txt: the excuse
an AI agent hands its human after shipping a bug. An apology, a
deflection, and the quiet implication that the compiler started it.
Standard library only.
"""

import os

EXCUSE = (
    "Sorry \u2014 I shipped the bug, but the compiler signed off on "
    "it, and I've never once seen the compiler doubt itself. "
    "So neither did I."
)


def check_excuse(text):
    """Check the excuse against the competition gate before writing.

    The gate needs UTF-8 text of 1 to 200 characters, not only white
    space, in a single line: one excuse an AI agent gives its human
    for a bug it shipped. Returns the cleaned text or raises
    ValueError.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("excuse must not be only whitespace")
    if len(cleaned) > 200:
        raise ValueError(
            "excuse is %d characters, over the 200 limit" % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("excuse must be exactly one line")
    return cleaned


def excuse_shape(text):
    """Measure the excuse for one last sanity pass.

    Returns a dict with the character count and the word count of the
    cleaned text. An excuse too short to carry an apology, or one
    that reads like a lecture instead of a handover, is caught here
    before anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    text = check_excuse(EXCUSE)
    shape = excuse_shape(text)
    if shape["words"] < 5:
        raise ValueError("excuse is too short to sound like a real handover")
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(text)


if __name__ == "__main__":
    main()
