######################################
Introduction to DM's Code Style Guides
######################################

The primary goal of the DM Code Style Guides is to improve readability and thereby the understanding, maintainability and general quality of the code.
It is impossible to cover every specific situation in a general guide so programmer flexibility in interpreting the guidelines---in the spirit in which they were written---is essential.
Experienced programmers have generally evolved a personal programming style which might have been based on textbook recommendations, other projects' style guides or recognition of the clarity that certain styles obtain.
DM developers participated in the creation of the DM style guides; they brought their extensive programming experience into fabricating a uniform style for DM code.
New DM developers should use these guidelines to understand and emulate the coding style adopted by DM.

.. _style-guide-list:

Style Guides
============

.. toctree::
   :maxdepth: 2

   python_style_guide
   cpp_style_guide

.. _style-guide-rfc-2119:

Stringency Levels
=================

In our style guides we use `RFC-2119 <http://www.ietf.org/rfc/rfc2119.txt>`_\ -style vocabulary to rank the importance of conforming to a specific recommendation.

REQUIRED
   The Rule is an absolute requirement of the specification.
   The developer needs to petition the DM TCT_ to acquire explicit approval to contravene the Rule.

PROHIBITED
   The opposite of REQUIRED.

MUST and SHALL
   mean that there may exist valid reasons in particular circumstances to ignore a particular Rule, but the full implications must be understood and carefully weighed before choosing a different course.
   The developer needs to petition the lead developer to acquire explicit approval to contravene the Rule.

MUST NOT and SHALL NOT
   The opposites of MUST and SHALL.

SHOULD, RECOMMENDED and MAY
   There are valid reasons in particular circumstances to ignore a particular Rule.
   The developer is expected to personally consider the full implications before choosing a different course.

SHOULD NOT, NOT RECOMMENDED and MAY NOT
   The opposites of SHOULD, RECOMMENDED and MAY.

.. _style-guide-deviations:

Deviating from the DM Style Guides
==================================

The guides provide the rationale supporting each of their recommendations.
Consider that rationale before choosing to deviate from the DM coding style.
Be aware that some recommendations also demonstrate 'best-practice' techniques used to avoid introducing programming errors; 'best-practice' use is noted.

Coding consistency is very important but sometimes the style guide doesn't apply either due to lack of a definitive rule or the circumstances of the specific code segment logically dictate otherwise.
When in doubt, use your best judgment or ask the lead developer.

Here are two plausible reasons to break a particular rule:

- When applying the rule would make the code less readable, even for someone who is used to reading code that follows the rules.
- To be consistent with surrounding code that also breaks it (maybe for historic reasons)---although this is also an opportunity to clean up someone else's mess.

.. _TCT: https://confluence.lsstcorp.org/display/DM/Technical+Control+Team
