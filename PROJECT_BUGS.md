# Project Bug Register

## OPEN

No open bugs currently block the corrected Phase 03 portrait module.

## RESOLVED

### BUG-06 — Portrait asset delivery / live rendering

**Severity:** CRITICAL  
**Introduced:** Phase 03 correction pass  
**Component:** `[03] MORPHING CYBER PORTRAIT`  
**Description:** The corrected GIF and PNG required live GitHub desktop verification with no broken image or fallback alt-text state.  
**Resolution:** Verified the published portrait on the live GitHub desktop profile after the correction commit. The particle portrait rendered in the left hero module with no broken image or alt-text placeholder. The controlled 390px Chromium render also loaded the portrait.  
**Resolved in phase:** Phase 03 correction pass.

### BUG-07 — Portrait behaves like a filter carousel

**Severity:** CRITICAL  
**Introduced:** Phase 03 correction pass  
**Component:** `[03] MORPHING CYBER PORTRAIT`  
**Description:** The earlier animation changed the style of the same image between clean, ASCII, particle, and wireframe treatments, creating a filter-carousel feeling.  
**Resolution:** Replaced the separate photo/filter states with a single particle field whose points jitter, drift, breathe, disperse, and reform. The representative-frame contact sheet confirms that the visual is one portrait field changing state rather than a clean/ASCII/wireframe carousel.  
**Resolved in phase:** Phase 03 correction pass.

### BUG-08 — Particle field lacks continuous living motion

**Severity:** HIGH  
**Introduced:** Phase 03 correction pass  
**Component:** `[03] MORPHING CYBER PORTRAIT`  
**Description:** The earlier stable portrait state did not continuously jitter, drift, breathe, or vary density as a living particle field.  
**Resolution:** Added deterministic per-frame local jitter, drift, breathing scale, density variation, and persistence bias while preserving the Loki silhouette.  
**Resolved in phase:** Phase 03 correction pass.

### BUG-09 — No meaningful dispersal/reconstruction event

**Severity:** HIGH  
**Introduced:** Phase 03 correction pass  
**Component:** `[03] MORPHING CYBER PORTRAIT`  
**Description:** The earlier sequence did not provide a meaningful wave, dispersal, convergence, and reformation event.  
**Resolution:** Added a traveling radial wave, controlled outward dispersal, partial silhouette retention during disturbance, and a timed return to the recognizable particle portrait. The contact sheet visibly shows disturbance at frames 11–15 and reformation from frames 17–23.  
**Resolved in phase:** Phase 03 correction pass.

### BUG-10 — Portrait creates product-advertisement feeling

**Severity:** HIGH  
**Introduced:** Phase 03 correction pass  
**Component:** `[03] MORPHING CYBER PORTRAIT`  
**Description:** The earlier filter-carousel presentation read like a product advertisement instead of a living cyber identity system.  
**Resolution:** Removed scanline-dominated photo treatment, ASCII filter transitions, and major wireframe states. The output is now primarily cyan/soft-cyan/ghost-white particles on a void-black field, with only quiet technical labels and field markers.  
**Resolved in phase:** Phase 03 correction pass.

### BUG-11 — Literal hover interaction unavailable in GitHub README runtime

**Severity:** MEDIUM  
**Introduced:** Phase 03 correction pass  
**Component:** `[03] MORPHING CYBER PORTRAIT`  
**Description:** A literal mouse-hover particle reaction is not implemented because the GitHub README environment must not rely on runtime JavaScript, Canvas, WebGL, or event handlers.  
**Resolution:** The intended reactive feeling is simulated through pre-rendered periodic wave reactions, subtle particle pulses, timed dispersal, and reconstruction events in the committed GIF.  
**Resolved in phase:** Phase 03 correction pass.

### BUG-05 — Mobile rendering not validated

**Severity:** MEDIUM  
**Introduced:** Phase 01  
**Component:** `[01] IDENTITY / HERO CONTAINER` and `[03] MORPHING CYBER PORTRAIT`  
**Description:** Phase 01 was visually checked at desktop width, but narrow/mobile GitHub rendering was not validated with live GitHub evidence.  
**Resolution:** Performed controlled Chromium renders of the live GitHub profile at 390px wide after the hero and portrait assets were integrated. The title wrapped, the portrait remained within the hero card, SYSTEM.INFO remained readable, and no horizontal page overflow was observed. Physical-device and Firefox rendering remain explicitly unverified limitations.  
**Resolved in phase:** Phase 03.

### BUG-01 — Default HTML table border

**Severity:** MEDIUM  
**Introduced:** Phase 01  
**Component:** `[01] IDENTITY / HERO CONTAINER`  
**Description:** The initial hero used `border="1"`, which produced a generic browser/GitHub table border instead of deliberate terminal framing.  
**Resolution:** Removed the `border="1"` dependency and replaced it with text-based box-drawing and terminal framing markers inside the hero content.  
**Resolved in phase:** Phase 02.

### BUG-02 — Hero feels visually empty

**Severity:** MEDIUM  
**Introduced:** Phase 01  
**Component:** `[01] IDENTITY / HERO CONTAINER`  
**Description:** The initial hero contained two generic placeholder columns with excessive unused space.  
**Resolution:** Made the SYSTEM.INFO column substantive with approved real identity and technology information, while preserving the portrait column as an intentional reserved module.  
**Resolved in phase:** Phase 02.

### BUG-03 — Generic placeholder presentation

**Severity:** LOW/MEDIUM  
**Introduced:** Phase 01  
**Component:** `[03] MORPHING CYBER PORTRAIT` reserved slot  
**Description:** The initial `PLACEHOLDER` wording read as unfinished implementation.  
**Resolution:** Replaced it with explicit system-state wording and later activated the approved portrait module.  
**Resolved in phase:** Phase 02/03.

### BUG-04 — Temporary footer

**Severity:** LOW  
**Introduced:** Phase 01  
**Component:** `[16] SOCIAL / CONTACT / FOOTER` not yet implemented  
**Description:** The temporary footer did not belong to the locked architecture because the social/contact/footer component had not been implemented.  
**Resolution:** Removed the temporary footer from `README.md`.  
**Resolved in phase:** Phase 02.
