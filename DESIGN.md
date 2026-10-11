---
name: Footnote
description: A daylight editorial reference desk for reading sources and preserving judgments.
colors:
  paper: "#f5f3ec"
  ink: "#24382e"
  muted: "#58665c"
  rule: "#d8dcd2"
  green: "#315c45"
  wash: "#e5eddf"
  red: "#813b32"
  ochre: "#715a19"
  white: "#fffefa"
typography:
  display:
    fontFamily: "Libre Baskerville, serif"
    fontSize: "clamp(30px, 3.1vw, 46px)"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Libre Baskerville, serif"
    fontSize: "28px"
    fontWeight: 400
    lineHeight: 1.5
  title:
    fontFamily: "Libre Baskerville, serif"
    fontSize: "22px"
    fontWeight: 400
  body:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
  post:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.6
  quote:
    fontFamily: "Libre Baskerville, serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.9
  label:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "12px"
    fontWeight: 500
  section-label:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "14px"
    fontWeight: 600
rounded:
  field: "4px"
  primary: "5px"
  wallet: "6px"
spacing:
  tight: "8px"
  compact: "10px"
  small: "12px"
  label: "14px"
  medium: "16px"
  large: "20px"
  section: "24px"
  generous: "28px"
components:
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "white"
    rounded: "{rounded.primary}"
    padding: "13px 19px"
  button-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "8px 12px"
  button-wallet:
    textColor: "{colors.ink}"
    rounded: "{rounded.wallet}"
    padding: "10px 15px"
  input:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "11px 12px"
    width: "100%"
  navigation:
    textColor: "{colors.muted}"
    padding: "10px 0"
  status-supported:
    textColor: "{colors.green}"
  case-file:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    padding: "28px 36px 38px"
  evidence-supported:
    backgroundColor: "{colors.wash}"
    textColor: "{colors.green}"
    padding: "14px 15px"
  source-row:
    textColor: "{colors.ink}"
    padding: "16px 0"
  history-selected:
    backgroundColor: "{colors.wash}"
    textColor: "{colors.ink}"
    padding: "12px 9px"
---

# Design System: Footnote

## Overview

**Creative North Star: "The Editorial Reference Desk"**

Footnote feels like a daylight reference desk: warm paper, forest ink, a brighter case file, and fine rules that organize a careful reading sequence. The visual emphasis belongs to the post, its judgment, and the quoted source. Libre Baskerville brings an editorial voice to headings and quotations; DM Sans keeps controls and dense records readable.

The system is quiet, flat, and text-led. Small metadata supplies provenance without competing with the claim. Evidence and tone occupy separate surfaces, while restrained green wash marks supported evidence and the selected record. Plain, careful language is a durable part of the identity: appearance must not imply more certainty than the sources establish.

**Key Characteristics:**

- Warm paper surrounding a bright reading surface.
- Editorial serif headings and quotations paired with practical sans-serif controls.
- Fine ruled divisions and tonal selection instead of lifted cards.
- Independent evidence and tone labels.
- Compact mobile controls that preserve the central reading sequence.

## Colors

The palette is a low-saturation paper-and-forest system; frontmatter values come directly from the root stylesheet.

### Primary

- **Forest Green** (`green`): primary actions, supported evidence, network markers, caret and keyboard focus.
- **Sage Wash** (`wash`): selected notes and history rows, supported evidence panels, receipts and the circular post symbol background.

### Secondary

- **Brick Red** (`red`): contradicted evidence text. Its evidence surface uses the stylesheet's pale clay fill.
- **Dry Ochre** (`ochre`): unsupported evidence and unavailable-state text. Its evidence surface uses the stylesheet's pale straw fill.

### Neutral

- **Warm Paper** (`paper`): the page, margins and outer shell.
- **Forest Ink** (`ink`): primary text and current navigation.
- **Quiet Moss** (`muted`): explanatory copy, provenance and secondary controls.
- **Pencil Rule** (`rule`): hairline borders, form strokes and section divisions.
- **Reading White** (`white`): the case file, input fields and secondary actions.

The misleading state uses an observed brown text and pale tan surface; tone uses its own pale neutral surface. These are component state treatments, retained in the sidecar rather than promoted into additional global palette primitives.

**The Separate Judgments Rule.** Evidence carries the verdict color; tone remains on a neutral surface and is labeled separately.

## Typography

**Display Font:** Libre Baskerville, with serif fallback.

**Body Font:** DM Sans, with sans-serif fallback.

**Character:** The serif voice supplies thoughtful editorial hierarchy and distinguishes source quotations. Sans-serif text handles posts, labels, controls and the record without adding decorative weight.

### Hierarchy

- **Display:** regular weight, responsive size and slightly tightened tracking; the main introduction. At the compact breakpoint it becomes 26px.
- **Headline:** regular serif; form and proof headings, reduced to 24px on mobile.
- **Title:** regular serif; the footnote heading, reduced to 21px on mobile. Supporting margin headings use 19px.
- **Body:** regular sans-serif; the base reading and control style. Explanatory judgment text uses 13px with generous 1.8 line height, then 12px and 1.65 on mobile.
- **Post:** larger sans-serif; the original claim, reduced to 16px on mobile while retaining 1.6 line height.
- **Quote:** small serif with generous line height; exact source passages, reduced to 12px on mobile.
- **Label:** modest sans-serif with medium weight; fields and small controls. Section labels use semibold weight. Provenance is smaller (10–12px) and muted.

**The Quoted Voice Rule.** Use the serif for editorial headings and source quotations; keep the post and interaction labels in the sans-serif.

## Layout

The shell centers at a maximum width of 1600px with 5% horizontal inset. The desktop desk has a 250px index, flexible case file, and 220px explanation margin. At 1500px and above the side columns widen to 280px and 250px and case-file horizontal padding grows to 44px. At 1150px and below the explanation margin disappears, the index becomes 225px, and shell inset becomes 4%.

At 700px and below, the desk becomes one column with 20px shell inset. The final mobile overrides replace the index list with a compact note selector, make the case file run to the viewport edges, and compress the masthead to 60px. The introductory section uses 12px vertical padding, the network strip 4px, and the post 12px vertical margins; the judgment section tightens to 16px above and 14px below so quoted evidence arrives earlier. Navigation, wallet, the introductory write action, the original-post link and expandable action headings have a minimum 44px interaction dimension where specified. The mobile introductory action is an icon in a 44px square. Evidence and tone retain two columns with a 10px gap.

Forms and proof surfaces share a 730px maximum reading width. Spacing follows the observed compact steps in frontmatter rather than a formal mathematical scale: close control groups use tight gaps, sections breathe around fine rules, and the central article supplies the generous reading inset. Long post text, addresses and URLs wrap within available width.

## Elevation & Depth

Content surfaces have no elevation shadows. Depth comes from the distinction between paper, reading white, and sage selection; fine borders supply structure. The current navigation uses a one-pixel ink shadow solely as an underline. Keyboard focus uses a two-pixel green outline with four-pixel offset, recorded in the sidecar as a component treatment.

**The Flat Record Rule.** Keep reading surfaces flat; use rules and tonal selection to express grouping and current state.

## Shapes

The reading file, evidence panels, note index and history rows have square corners. Form fields and secondary actions have small curves; the primary action is slightly softer and the wallet control softer again, according to the frontmatter radius roles. Circles are reserved for the post symbol and tiny network/history nodes. One-pixel borders separate records rather than boxing every paragraph. Icons are simple outline SVGs.

## Components

### Buttons

Primary actions are compact forest-green controls with white text, modest curves and paired outline icons where useful. Hover darkens the primary fill to the implemented deep forest treatment. Secondary actions use reading-white fill, a fine rule border and sage hover fill. The wallet control is transparent and outlined on desktop; mobile presents its icon within a compact target. Disabled buttons halve opacity and use the waiting cursor. Keyboard focus follows the shared green outline.

### Chips

Status tags are plain semibold text rather than pills. Supported, contradicted, unsupported and misleading inherit their semantic text treatments; do not require a background on the small index label. The larger evidence panels carry a pale semantic fill.

### Cards / Containers

The central case file is a square reading sheet with fine side rules and generous inset. It has no hover lift or shadow. Evidence and tone panels form a matched pair, using small labels above medium-weight judgments. The tone panel is neutral. Error and receipt strips reuse flat fills and a bottom rule instead of dialogs.

### Inputs / Fields

Inputs and resizable textareas use reading white, a fine rule border, forest text, muted placeholders and the field radius. Labels sit above the fields with a small gap. Focus receives the common green outline, and the caret is forest green. Evidence selectors are quieter, transparent controls with a bottom rule; the mobile note selector omits that rule.

### Navigation

The masthead is a horizontal ruled row. A serif wordmark anchors the left side; sans-serif text navigation follows, and the wallet sits at the right. Current navigation changes from muted text to ink and gains the fine underline. Mobile reduces gaps and text size while maintaining usable targets. The implementation does not define a distinct navigation hover or active-press visual; preserve the common keyboard focus treatment.

### Numbered Source Row

A small bracketed index sits beside a linked host, serif quotation and muted digest. A top rule separates each source. Links retain underlines with four-pixel offset and outline external-link arrows. This pattern gives the quotation enough space to read without turning provenance into a card title.

### Version Record

Each version is a compact button row with a green node, version number, judgment and date. The selected row uses sage wash and `aria-pressed`; the mobile row hides the optional reason metadata. Source quotations remain in the main reading area when a version is selected.

### Motion and Focus

Motion is limited to the two-second linear refresh spinner. The reduced-motion query disables animations. The system has no entrance choreography, hover movement, or transition scale. Preserve visible outlines for keyboard access and use actual state text alongside semantic color.

## Do's and Don'ts

### Do:

- **Do** reuse paper, reading white, forest ink and fine rules for new surfaces.
- **Do** preserve separate evidence and tone treatments.
- **Do** use serif headings and quotations with sans-serif posts and controls.
- **Do** mark selection with sage wash and retain the visible green keyboard focus outline.
- **Do** wrap long URLs and addresses and keep mobile reading within the available width.

### Don't:

- **Don't** introduce lifted reading cards or decorative elevation into this flat record system.
- **Don't** replace semantic state text with color alone.
- **Don't** use the evidence verdict color for the tone panel.
- **Don't** add motion that undermines the existing reduced-motion behavior.
