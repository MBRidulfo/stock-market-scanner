def detect_volume_spike(df, lookback=14, multiplier=1.5, day_jump_ratio=1.8):
    if len(df) < lookback + 1:
        return False, None, None, None

    recent = df.iloc[-lookback-1:-1]  # Previous 14 days, excluding today
    today_vol = df['Volume'].iloc[-1]
    yesterday_vol = df['Volume'].iloc[-2]
    avg_vol = recent['Volume'].mean()

    spike_detected = (
        today_vol > avg_vol * multiplier or
        today_vol > yesterday_vol * day_jump_ratio
    )

    return spike_detected, avg_vol, yesterday_vol, today_vol
