// Converts a row from the CSV into features and labels.
// Each feature field is normalized within training data constants
// { xs: XSType; ys: YSType }
export function csvTransform({ xs, ys }: any) {
  // Constants from training data
  const VX0_MIN = -18.885;
  const VX0_MAX = 18.065;
  const VY0_MIN = -152.463;
  const VY0_MAX = -86.374;
  const VZ0_MIN = -15.5146078412997;
  const VZ0_MAX = 9.974;
  const AX_MIN = -48.0287647107959;
  const AX_MAX = 30.592;
  const AY_MIN = 9.397;
  const AY_MAX = 49.18;
  const AZ_MIN = -49.339;
  const AZ_MAX = 2.95522851438373;
  const START_SPEED_MIN = 59;
  const START_SPEED_MAX = 104.4;

  const values = [
    normalize(xs.vx0, VX0_MIN, VX0_MAX),
    normalize(xs.vy0, VY0_MIN, VY0_MAX),
    normalize(xs.vz0, VZ0_MIN, VZ0_MAX),
    normalize(xs.ax, AX_MIN, AX_MAX),
    normalize(xs.ay, AY_MIN, AY_MAX),
    normalize(xs.az, AZ_MIN, AZ_MAX),
    normalize(xs.start_speed, START_SPEED_MIN, START_SPEED_MAX),
    xs.left_handed_pitcher,
  ];
  return { xs: values, ys: ys.pitch_code };
}

// util function to normalize a value between a given range.
export function normalize(value: number, min: number, max: number) {
  if (min === undefined || max === undefined) {
    return value;
  }
  return (value - min) / (max - min);
}
