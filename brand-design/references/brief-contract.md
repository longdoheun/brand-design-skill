# Brand brief contract

The user can provide a few sentences. Normalize them into these fields; do not demand JSON or a full marketing questionnaire. The explicit input outranks inferred design preferences.

| Field                   | Purpose                                                                                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`, `slug`          | Exact visible spelling and safe output filename prefix.                                                                                            |
| `purpose`, `audience`   | What the brand helps people do and what the logo needs to communicate.                                                                             |
| `philosophies`          | A few `{id, statement, priority}` entries. Rank ideas when they compete; not every idea needs a literal motif.                                     |
| `rules`                 | `{id, statement, strength}` entries. Strength is `hard` or `exploratory`. Include geometry, shape relations, and constraints supplied by the user. |
| `preserve`, `avoid`     | Existing identity invariants and unwanted motifs or treatments.                                                                                    |
| `applications`          | Placement, surface, and intended pixel or print size.                                                                                              |
| `palette`, `typography` | Agreed values or preferences; leave unspecified until chosen.                                                                                      |
| `assumptions`           | Inferred decisions awaiting actual visual assessment, not invented approvals.                                                                      |

Keep immutable requirements separate from the design's adjustable parameters. A rule such as “all derived forms come from one curve” constrains the source model; a preference such as “slightly softer” guides optical exploration. Do not reduce philosophies to a universal table that always maps “trust” to circles or “progress” to arrows.

## Traceable rationale

For each philosophy, record a proposed operation, named parameters, expected perceptual result, and a check. Mark the mapping `implemented` or `pending`. An implemented geometric operation still needs visual review; it does not prove the audience reads the intended meaning.

Example: “multiple viewpoints of one process” might produce transformed views of a shared source shape. The check is that both shapes actually derive from the same parameters, followed by visual assessment of whether their combined counter remains legible. If the logo is still a single unrelated shape, this mapping stays pending.

## Example request

> Use $brand-design for a logo for a new education brand. Philosophies: curiosity, gradual discovery, and calm confidence. Rules: derive every element from one grid; make negative space meaningful; avoid a book or lightbulb. Explore open and compact forms for a 32px web header, with an outlined wordmark.

The input defines a design problem, not a preset emblem. Choose brand-specific geometry, record the choices, and compare structural variations rather than simply recoloring an existing example.
