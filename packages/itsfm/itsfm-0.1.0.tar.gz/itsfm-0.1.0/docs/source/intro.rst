The `itsfm` package identifies regions of sound with and without frequency modulation, 
and allows custom measurements to be made on them. It's all in the name. Each of the 
task behind the identification, tracking and segmenting of a sound can be done independently.

The sounds could be bird, bat, whale, artifical sounds - it should hopefully work,
however be aware that this is an alpha version package at the moment. 

The basic workflow involves the tracking of a sounds frequency over time, and then calculating the 
rate of frequency modulation (FM), which is then used to decide which parts of a sound are frequency
modulated, and which are not. Here are some examples to show the capabilities of the package. 

The broad idea of this package is to achieve a loose coupling between the I,T, S in the package name. 
`itsfm` can do all or one of the below.

* I : Identify sounds by frequency modulation. An input audio can have multiple sounds in it, separated by silence or fainter regions. 
* T : Track the sound's frequency over time. The PWVD method allows tracking a sound's frequency with high temporal resolution. 
* S : Segment according to the frequency modulation. Calculates the local rate of frequency modulation over a sound and classifies parts of it 
  as frequency modulated (FM) or constant frequency (CF)

*Warning : The docs are constantly under construction, and is likely to change fairly regularly like the stairs in Hogwarts.
Do not be surprised by dramatic changes, but do come back regularly to see improvements!*
