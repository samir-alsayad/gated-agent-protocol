# Starter: UI/UX Design (UX-Flow)

This starter provides the document chain for user interface and experience design.

## Tier 1: User Constraints (`constraints.md`)
*Define interface behaviors using EARS syntax.*

- **CNST-1**: WHEN the user is on a mobile device, THE navigation menu SHALL be hidden by default.
- **CNST-2**: WHILE a form is submitting, THE submit button SHALL show a loading state and be disabled.

## Tier 2: Aesthetic Invariants (`invariants.md`)
*Define properties that ensure consistency and compliance.*

- **INV-1**: For any text element, the color contrast ratio against its background shall be at least 4.5:1 (WCAG AA).
- **INV-2**: For any primary action button, the border-radius shall be exactly 8px.

## Tier 3: Asset Delivery (`delivery.md`)
*Atomic steps traced to constraints and invariants.*

- [ ] STEP-1: Create Low-Fidelity Wireframes
    - _Intent: CNST-1_
- [ ] STEP-2: Implement High-Fidelity Mockups
    - _Invariant: INV-1, INV-2_
- [ ] STEP-3: Accessibility Audit
