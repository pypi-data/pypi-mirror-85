# SafeGIF: scan GIFs for safety for people with photosensitive epilepsy


## Why SafeGIF?
The internet can be a dangerous place for some people with photosensitive epilepsy. Not only are some GIFs inadvertently dangerous due to very bright colors or fast flashes: malicious attacks have been coordinated to induce seizures online. Kurt Eichenwald, a senior writer at the New York Times, [was targeted through flashing GIFs](https://www.nytimes.com/2017/03/17/technology/social-media-attack-that-set-off-a-seizure-leads-to-an-arrest.html) private-messaged to him, intended to cause a seizure. 

SafeGIF will allow people with photosensitive epilepsy to get assurance of the safety of the content they are consuming. This library will scan GIFs for safety, and a future library will grab GIFs from Twitter.

This library is a lightweight library for analyzing GIFs in real-time for fast flashes that may trigger a seizure for people with photosensitive epilepsy. I envision this as a component of larger projects, and I will be creating a different library for grabbing Twitter GIFs in the future, to create a complete product. 

## Contributions
Please feel free to contribute by submitting a pull request or adding an issue! Here are some quick entry points:
- add suggestions for future features or papers I could read to fix this algorithm
- improve this README 
- add comments and documentation to code

## Action Items
These are the main milestones for the project! As development continues, I'll add issues and tag them for easier contribution. 
- isolate GIFs by frame
- read papers and ascertain what exactly makes a GIF dangerous on a frame-by-frame level
- translate these papers to code
- optimize algorithm to evaluate GIFs in real-time

## Note on Testing
There's no publicly available databases for GIFs that have the potential to trigger seizures. Thus, I created a "corruption" algorithm that introduces deep red frames and flashing into GIFs in order to test the detection capabilities of this library. For ethics reasons, I won't release it publicly; releasing it could allow bad actors to corrupt GIFs for coordinated attacks. If you'd like to see it for testing purposes, feel free to open an issue or DM me on Twitter @gaia_writes and we can chat!

Credits to [this amazing README checklist](https://github.com/ddbeck/readme-checklist) for the structure of this document. 

