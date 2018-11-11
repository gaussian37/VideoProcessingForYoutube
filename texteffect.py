import numpy as np
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

class TextEffect():
    
    clips = VideoClip()
    
    def __init__(self, text = None, screensize = (1280, 720), fontsize=50):        
        txtClip = TextClip(text, color='white', font="Amiri-Bold", kerning = 5, fontsize=fontsize)
        
        cvc = CompositeVideoClip( [txtClip.set_pos('center')],
                                    size=screensize)
        
        letters = findObjects(cvc) # a list of ImageClips
        
        self.clips = [CompositeVideoClip(self.moveLetters(letters, funcpos), 
                                    size = screensize).subclip(0,5) for funcpos in [self.vortex] ]
        
        self.clips = concatenate_videoclips(self.clips)
        
    def rotMatrix(self,a):
        return np.array([[np.cos(a),np.sin(a)],
                         [-np.sin(a),np.cos(a)]])
    
    def vortex(self, screenpos,i,nletters):
        d = lambda t : 1.0/(0.3+t**8) #damping
        a = i*np.pi/ nletters # angle of the movement
        v = self.rotMatrix(a).dot([-1,0])
        if i%2 : v[1] = -v[1]
        return lambda t: screenpos+400*d(t)*self.rotMatrix(0.5*d(t)*a).dot(v)
    
    def cascade(self, screenpos,i,nletters):
        v = np.array([0,-1])
        d = lambda t : 1 if t<0 else abs(np.sinc(t)/(1+t**4))
        return lambda t: screenpos+v*400*d(t-0.15*i)

    def arrive(self, screenpos,i,nletters):
        v = np.array([-1,0])
        d = lambda t : max(0, 3-3*t)
        return lambda t: screenpos-400*v*d(t-0.2*i)
    
    def moveLetters(self, letters, funcpos):
        return [ letter.set_pos(funcpos(letter.screenpos,i,len(letters)))
                  for i,letter in enumerate(letters)]