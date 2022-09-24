1. Install label-studio by running `brew install heartexlabs/tap/label-studio`
2. Launch label studio
3. Create project for labeling images using as labeling setup `Object Detection with Bounding Boxes`
4. Upload images for labeling (in my case - cat's images) to test label-studio 
5. Label 50 files, took me 20 minutes

If we want to talk about our problem, we need to have the essay text and it's score. 
If essays are in image format we can use `Optical Character Recognition` template to create a dataset, time to label the data depends on the amount of words in the essay.
Labeling one essay (converting an image to a text) may take 40-60 minutes depending on typing speed.
We need to ensure that all the text must be typed correctly (as student wrote). The chance of a human error (i.e. making a typo when entering the text or accidentally fixing the mistake that is present in the original text) is quite high so we need to check all the data and that process will also take some time. Bad student's handwriting may additionally increase the time needed.

If we have essays in a text format we can easily convert the data to csv.