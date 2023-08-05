import inspect
import traceback
import sys
from datetime import datetime

__version__ = '0.7'

class Exterminator:


    def __init__(self, frames: int = None, callback: callable = None, raise_error: bool = True):

        self.frames = frames
        self.callback = callback
        self.raise_error = raise_error


    def exterminate(self, exception: Exception = None, traceback_obj: 'traceback' = None):
        error_info = ''
        if not traceback_obj:
            traceback_obj = sys.exc_info()[2]
            skip = 1
        else:
            skip = 0
        error_info += traceback.format_exc() + '\n'
        error_info += f'Log time:\n\t{datetime.now()}\n'
        frames_info = inspect.getinnerframes(traceback_obj)[skip:]
        frames_number = len(frames_info)
        error_info += f'Total number of frames:\n\t{frames_number}\n'

        if self.frames:
            if self.frames < frames_number:
                do_not_include = frames_number - self.frames
                frames_info = frames_info[do_not_include:]
                error_info += f'Number of frames displayed:\n\t{self.frames}\n'

        for frame_number, frame_info in enumerate(frames_info, start= 1):
            frame_obj = frame_info.frame
            name = frame_info.function
            filename = frame_info.filename
            local_vars = frame_obj.f_locals
            error_info += f'Frame number: {frame_number}\n\tFunction name:\n\t\t{name}\n\tFilename:\n\t\t{filename}\n\tLocal variables:\n\t\t{local_vars}\n\n'
        
        error_info += ('-' * 95) + '\n'
        if self.callback:
            self.callback(error_info)
        else:
            with open('exterminator.log', 'a') as f:
                f.write(error_info)
        
        if self.raise_error and exception:
            raise exception


    def __call__(self, func):


        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                self.exterminate(e)


        return wrapper


    def __enter__(self):
        return None


    def __exit__(self, exception_type, exception_value, traceback):
        self.exterminate(traceback_obj= traceback)
