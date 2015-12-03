.. code-block:: py
   :name: context-timer-example
   :emphasize-lines: 4-13,15-17

   from contextlib import ContextDecorator
   import time
   
   class timercontext(ContextDecorator):

       def __enter__(self):
           self.start = time.clock()
           return self
   
       def __exit__(self, *args):
           self.end = time.clock()
           self.interval = self.end - self.start
           print('Duration: {0:.2e} sec'.format(self.interval))

    @timercontext
    def run_slowly():
        time.delay(1.)
    
    run_slowly()
    
    with timercontext() as t:
        time.delay(1)
    
    print('Delayed for {0:.1f}'.format(t.interval))
