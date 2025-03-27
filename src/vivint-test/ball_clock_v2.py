import json
import re
import time


class BallClock:
  """
  A simulation of a ball clock.

  This class provides methods to simulate the movement of balls through through the clock.
  """

  def __init__(self, num_balls: int, minutes: int):
    """Initialize variables for the ball clock."""
    self.num_balls: int = num_balls
    self.minutes: int = minutes
    self.main_track: list = list(range(1, num_balls + 1))
    self.minute_track: list = []
    self.five_minute_track: list = []
    self.hour_track: list = []
    self.days: int = 0

  def add_ball(self):
    """
    Add a ball to the minute_track

    When track is full, move balls on the minute_track back to main_track in reverse order
    and send the final ball to the five_minute_track.
    """
    ball: int = self.main_track.pop(0)

    if len(self.minute_track) == 4:
      while self.minute_track:
        self.main_track.append(self.minute_track.pop())
      self.add_five_minute_ball(ball)
    else:
      self.minute_track.append(ball)

  def add_five_minute_ball(self, minute_ball: int):
    """
    Add a ball to the five_minute_track

    When track is full, move balls on the five_minute_track back to main_track in reverse order
    and send the final ball to the hour_track.
    """
    if len(self.five_minute_track) == 11:
      while self.five_minute_track:
        self.main_track.append(self.five_minute_track.pop())
      self.add_hour_ball(minute_ball)
    else:
      self.five_minute_track.append(minute_ball)

  def add_hour_ball(self, five_minute_ball: int):
    """
    Add a ball to the hour_track

    When track is full, move balls on the hour_track back to main_track in reverse order
    and then send the final ball to the main_track.
    """
    if len(self.hour_track) == 11:
      while self.hour_track:
        self.main_track.append(self.hour_track.pop())
      self.days += 0.5
      self.main_track.append(five_minute_ball)
    else:
      self.hour_track.append(five_minute_ball)

  def find_cycle(self) -> str:
    """Find the days based on number of balls cycled through clock to return to original state."""
    initial_state: list = self.main_track.copy()
    self.days: int = 0

    while True:
      self.add_ball()
      if self.main_track == initial_state:
        return f"{self.num_balls} balls cycle after {self.days:.0f} days."

  def run_clock(self) -> str:
    """Run the clock for a given number of minutes and return the state of the clock."""
    for _ in range(self.minutes):
      self.add_ball()

    results: dict[str, list] = {
      "Min": self.minute_track,
      "FiveMin": self.five_minute_track,
      "Hour": self.hour_track,
      "Main": self.main_track,
    }

    return json.dumps(results)


def get_user_input(_input: int = "33") -> tuple[int, int] | tuple[int, None]:
  """Get user input for the number of balls and optional minutes."""
  user_input: str = _input
  while True:
    try:
      input_result: list[str] = re.sub(r"[^\d ]+", "", user_input).split(" ")

      if not 1 <= len(input_result) <= 2:
        raise ValueError(
          f"Invalid number of elements supplied {len(input_result)}. Please provide between 1-2 parameters seperated by a space.(ie. [30 325] or [30])"
        )

      get_tokens: list[int] = [int(x) for x in input_result if x.isdigit() and int(x) > 0]
      num_balls: None = None
      minutes: None = None

      if len(get_tokens) == 2:
        num_balls: int = get_tokens[0]
        minutes: int = get_tokens[1]

      if len(get_tokens) == 1:
        num_balls: int = get_tokens[0]

      if 27 <= num_balls <= 127:
        return num_balls, minutes

      else:
        raise ValueError(f"Invalid number of balls: {num_balls}")

    except ValueError as incorrect_user_input:
      print(incorrect_user_input)
    except Exception as e:
      print(f"Unknown Exception: {e}")
    user_input = input('Press "q" to quit program.\nEnter the number of balls (27-127): ')
    if user_input == "q":
      raise Exception("Program Terminated by user.\n")


def main():
  """Run the ball clock simulation."""
  # start_time_ms = time.time() * 1000
  try:
    # clock: object = BallClock(num_balls=30, minutes=325)
    num_balls, minutes = get_user_input(input("Enter the number of balls (27-127) and optional minutes (ie. [30] or [30 325]): "))
    clock: object = BallClock(num_balls=num_balls, minutes=minutes)

    if minutes:
      results: str = clock.run_clock()
    else:
      results: str = clock.find_cycle()

    print(results)

    # end_time_ms = time.time() * 1000
    # execution_time_ms = end_time_ms - start_time_ms
    # print(f"Execution time: {execution_time_ms:.2f} ms")
  except Exception as program_end:
    print(program_end)


if __name__ == "__main__":
  main()
