1. Installed label-studio by running `brew install heartexlabs/tap/label-studio`
2. Launch label studio
3. Create project for labeling images using as labeling setup `Object Detection with Bounding Boxes`
4. Upload images for labeling (in my case - cat's images) to test label-studio 
5. Label 50 files , took me 20 minutes

If to talk about our problem, we need to have essay text and it's score. 
To create dataset if essays are in image format we can user `Optical Character Recognition` template, time to label the data depends on the amount of words in essay.
Labeling one essay(converting image to text) may take 40-60 minutes(depending of typing speed).
Edge case is that all essay text must be types correctly(as student wrote) and we may have human factor so we need to check all data which also will take some time. Also bad student's handwriting will also increase time.

If we have essays in text format we can easily convert data to csv.