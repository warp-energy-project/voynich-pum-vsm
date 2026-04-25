# Voynich PUM/VSM Model

## Overview

This project explores the Voynich Manuscript as a structured system rather than a conventional language.

The working hypothesis:

> The structure of the text is influenced by the geometry of the adjacent illustration.

---

## Core Idea

Instead of decoding words, we analyze patterns.

Key observation:

- Upper parts of the page tend to show different token structures than lower parts
- The vertical position (Y-axis) influences text composition

---

## Model Components

- **Y-axis (position):** Controls variation in text structure
- **b (gradient):** Influenced by image geometry (e.g., root size, leaf density)
- **Echo:** Local repetition and mutation patterns in tokens

---

## Simplified Explanation

The text behaves as if it is generated based on the structure of the drawing.

Example:

- Upper area → lighter structure (more "sh" patterns)
- Lower area → heavier structure (more "cth" and "-dy")

---

## Status

This is not a full decipherment.

However, there is strong evidence of a structured, non-random relationship between image and text.

---

## Next Steps

- Validate pattern consistency across folios
- Analyze star-marked pages (possible metadata layer)
- Develop a minimal generative model
