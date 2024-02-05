def get_mode(x):
    mode_values = x.mode()
    if len(mode_values) > 0:
        return mode_values.iloc[0]
    else:
        return None