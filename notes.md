# Slime


23-Mar-2025

- Sensing and turning is working. I need to make it more directional though. 
- It's starting to look good! We have this bubble formation that we see in Sebastian's video as well.


24-Mar-2025

- Started trying to convert everything to arrays so that it's more efficient. Not working very well at this point.
- Next steps
    - Profile this to figure out which steps are actually the most costly.
    - Isolate the costrly bits and see how to vectorise them.
    - Sketch out a diagram and look at how you can calculate angles more efficiently given that the
        - (a) the velocity magnitude is always fixed
        - (b) we already work out the angle when doing the comparison.
