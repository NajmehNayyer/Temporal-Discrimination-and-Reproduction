# Temporal Discrimination and Reproduction
 
PsychoPy reproduction of the two interval-timing tasks from:
 
> Pourmohammadi, A., & Sanayei, M. (2023). Context-specific and context-invariant computations of interval timing. *Frontiers in Neuroscience*, 17:1249502. https://doi.org/10.3389/fnins.2023.1249502
 
## Deviations from the original study
 
The original study used MATLAB/Psychtoolbox-3, an EyeLink 1000 eye tracker, and both hand and saccadic-eye-movement response blocks. This reproduction:
 
- Is implemented in **PsychoPy** (Python).
- Has **no eye tracker**. Gaze-contingent fixation is replaced by a manual check: the participant presses **Space** to confirm fixation before each trial starts. There are no saccadic-response blocks (eye tracking is required for those) — only the **hand/keyboard response** version of each task is implemented.
