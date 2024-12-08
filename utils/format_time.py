def convertToTimeFormat(seconds: int) -> str:

  hours = seconds // 3600
  minutes = (seconds - hours * 60) // 60
  seconds = seconds - hours * 3600 - minutes * 60

  return f"{hours:02d}:{minutes:02d}:{seconds:02d}"