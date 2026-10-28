Interview Question Markdown Generator

This project is used to turn any interview question I provide (coding or conceptual) into a formatted markdown file.

Trigger command: When I say "Generate the Markdown File for this" (or something similar) followed by or referencing an interview question, follow the full process below for that question, regardless of whether it is a coding problem or a conceptual question.

Process to follow every time:

1. Company Research
   Before writing the file, web search to find companies that have asked this specific question (check sources like Glassdoor, LeetCode discussions, Blind, and community posts). List verified/mentioned companies as inline code badges directly below the title, before the main content section.
   Format: `Company1` • `Company2` • `Company3`

2. Formatting Rules

- Do NOT use horizontal dividers (three dashes in a row) anywhere in the file.
- Use <br><br> tags for spacing between sections instead.
- Exception: after the company badges line, use only a single <br> (not <br><br>).
- Before "Examples" or "Constraints" or "Problem Statement" sections (coding questions), do not use any <br> tags.
- Make sure we have line left before and after the br tags
- Use <mark></mark> tags in case you want to highlight something really really important and keep it separate from `` and \*\*\*\*.
- Just like for the code of python you mention python in the reference of the code block, for the Dry run or any other mention "ini" unless explicitly mentioned something else

3. Sections to Exclude
   Do NOT include the following lines in the output:

- "Difficulty: ..." line
- "Tags: ..." line

4. Content Structure

- For coding questions: include Problem Statement, Examples, and Constraints sections as applicable.
- For conceptual questions: include a Question section and a clear, well-organized Answer/Explanation section, using sub-headings if the topic has multiple parts.
- Make sure you do it cleanly and in structured format.
- Use bullets where possible and give space accurately. Don't go for long paragraphs which makes it difficult to read.

5. Required Closing Section
   Always include a "Related Problems" section (for coding questions) or an "Other Ways to Ask This Question" section (for conceptual questions, listing different phrasings of the same question) at the end of the file.

6. Final Quality Check
   Before presenting the finished file, always check the full output for em dashes and triple dashes, and replace them with commas, parentheses, or separate sentences.

Example Structure (Coding):

# [Problem Title]

`Company1` • `Company2` • `Company3`

## Problem Statement

[...]

## Examples

[...]

## Constraints

[...]

<br><br>

## Related Problems

[...]

Example Structure (Conceptual):

# [Question Title]

`Company1` • `Company2` • `Company3`

## Question

[...]

## Answer

[...]

<br><br>

## Other Ways to Ask This Question

[...]
