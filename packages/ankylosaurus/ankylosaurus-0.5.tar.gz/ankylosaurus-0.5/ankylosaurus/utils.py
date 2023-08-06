import imageio


"""
A collection of utils.
"""

def each(fn, items):
  """
  Python lacks an each function.
  The following is morally identical to "map", but with no return value.
  """
  for item in items:
    fn(item)

def make_gif(frames, output, frame_duration=0.5):
    """
    Creates an animation from a list of ordered frames.
    """
    with imageio.get_writer(output, mode='I', duration=frame_duration) as writer:
        for frame in frames:
            image = imageio.imread(frame)
            writer.append_data(image)