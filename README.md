pySimpleGraphx
==============

Minimalist graphics engine written in python
The engine intends to provide a very simple way to start developping
3D games and simulations using pygame and pyopengl. It features:
	* a Graphx object, that manage the context window and the lights
	* a Camera object which is a "Fly Cam", written thanks to Will McGugan
	  (http://www.willmcgugan.com/blog/tech/2007/6/4/opengl-sample-code-for-pygame/)
	  
## Usage

The easiest way to use the graphx engine is to use the following code:
```
graphx = Graphx()

while True:
	# draw something...
	self.graphx.update()
```

More examples and documentations will come...
