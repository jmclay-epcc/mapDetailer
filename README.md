This is a very rough, simple, very chatGPT-influenced ISR project that is designed to upscale rough "sketches" of maps into more realistic, satellite image like projections (in this context, a "sketch" is a low-detail image made up of blobs with blocky colours).  

The scripts function as follows:- 

##imageSplitter.py

This script creates the database files and file structure for model trainer (localTrainer.py).  It does this by taking currently just two inputs; a high resolution texture and a low resolution sketch,  chopping them up into 1,152 squares, and then places 75% of them into a training folder and 25% of them into evaluation.  Currently, as i mentioned, this works with only two images.  One texture and one sketch.  This isn't ideal as it limits traning data.  In the future, this will be upgrades to be flexible to any number of input images.  Another thing to note is that this version of the script currently reduces the resolution of the sketch by half.  This is very simply because the sketch image is just the texture after having been run through some image manipulation, and i forgot to reduce its resolution.  This could be easily fixes in the future.  

##localTrainer.py

This script takes the database created by imageSpliter.py and uses it to train an EDSR model.  This is a pretty simple script, as long as the database is set up and populated right it should run without issue.  One thing that is worth pointing out is that the scale factor in this script is set to 2x.  This means that the training data ALSO NEEDS TO BE 2X SCALE.  The EDSR model does support 3x and 4x, but I found they produced odd visual artifacts that i could never get rid of.  

##mapUpscaler.py

This is where the magic happens.  This script import the sketch we want to upscale (again currently reducing its reosltiuon by half because i forgot to change the actual file whop whop), and outputs an upscaled version using the model we trained earlier.  This script is probably close to its final state because there is really very little that this script needs to do.  Maybe some UI for selecting the sketch file would be nice?  

##Does it work?

Currently... no not really.  I have had very negative results so far.  
- Currently the model training seems to cap out at a loss of around 0.02, which isn't ideal.  This point is normally reached after around 20 epochs, after which no appreciable improvement is ever made.  
- As a result of this, the detailed output isn't that good.  Effectively all it can manage to do is correct colours, blur the sketch a bit, and sharpen up the coasts of the blobs.  It does not add any detail to the coastlines or geological features.  
- Part of this is undoubtedly due to training data issues.  Currently, as was mentioned earlier, the training data is limited to one image.  The image is cut up into dozen of little pieces, but it still produces a relatively small number of training images.  Another issue is that like 50% of them are just blue squares.  The model is undoubtedly very good at the colour blue - it always figures out how to colour correct the oceans within just a couple epochs, but thats not very helpful for making interesting land masses.  

There are a couple possible avenues of improvement here:-  
- More training data.  It had occured to me that i could pull the Kerbin texture from KSP2; this would double the size of the training data pool and would be very easy to do.  There are also probably other photo-realistic style earthlike planet maps on the internet.  
- Training time.  So far, the furthest i've run the training is 70 epochs.  However, as mentioned before, the loss caps out at around 0.02, 0.019 at best.  However i will admit that i might be able to push this further with longer training - the default model that this python package came with was trained for 1000 epochs.  It could just be that what it needs is the brute-force approach of just letting it go wild training for a week (its also worth mentioning that the 70 epoch training cycle was using greater than 2x scale, which as i mentioned before was producing all sorts of weird artifacts that weren't present in 2x, so that whole training session was FUBAR anyway).  
- Improve the script itself.  A lot of ISR python projects are focused, infuriating, on upscaling anime.  Another good chunk of them just don't seem to work anymore.  As such i am under no illusions that the method im using is the best possible.  
- Generative AI.  What im asking the this AI method to do is perhaps a bit outside of its ballpark to start with.  Image Super-Resolution is intended to take a low-resolution image and pick out details.  I am asking it to take a high resolution, low detail image, and plaster in brand new details.  This might be a better task for generative AI.  
- Other types of AI.  I recall watching a video on youtube once where someone created a model that would take in a drawing of a letter, and make it "more capital" or "more lower-case".  This is very interesting to me, as it is taking in an image with some resolution and using it to create a new image with the same resolution, but which better meets a certain trained criteria.  This very well might be a better way of approaching thsi problem than image super-resolution.  We train a model to take in sketches, and transform them until they meet the criteria of being satellite image-like.  

##Future goals.  
- More planets.  The true motivation behind this project is a 8-ish year old desire to create custom planets in KSP.  As such, only being able to generate Earthlike planets is limiting - i would want the model to be able to create all sorts of grey and red rocks, with all sorts of geological features.  Once i am happy with the models ability to generate earthlike worlds, i can expand the training database.  
- Heightmaps.  To further than custom KSP planet goal, it would also be good to be able to create heightmaps.  However i have come to realise this is a very large ask - it is one thing to expect a model to be able to take a low-detail image and make it high-detail, but its another thing entire to ask it to take a high-detail image, and transform it into a different high-detail image.  
- Mercator to Equirectangular projection transformation.  When people hand-draw maps, 90% of the time they draw something that is more akin to a mercator projection than a equirectangular projection.  For making game assets we really want equirecangular, so having the program automatically squish the input into the right shape before transforming it would be handy.  
- Edge alignment.  As a texture becomes more detailed, it becomes harder to ensure that the edge details line up right.  The current model of course makes no effort to correct or maintain edge alignment, so adding in this ability would be handy.  I suspect the easiest way to do this would be a second model that is trained specifically to fix edge alignment.  There are a couple ways to appoach this issue and i am certain each one has its ups and downs.  

