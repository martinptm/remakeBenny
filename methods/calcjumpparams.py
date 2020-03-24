def calc_a_and_v0(T, deltaY):
	""" calculates parameters for physical simulation of a jump
    Input: whole time of a jump 'T' when (starting from ground to 
    	   ground) in s and height of the jump 'deltaY' in px (relative
    	   to startingpoint of the jump)
    Output: acceleration a in px/s² and initial speed v0 in px/s
    """
	a = (2*(deltaY))/(T/2)**2
	v0 = a * T/2
    
	return (a,v0)
