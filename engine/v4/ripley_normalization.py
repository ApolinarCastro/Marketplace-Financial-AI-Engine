
def normalize_ripley_reference(value):
    if value is None: return None
    s=str(value).strip()
    if s.lower() in ("nan","none",""): return None
    # 531423.0 -> 531423
    if s.endswith(".0"):
        try:
            # check if integer
            f=float(s)
            if f.is_integer():
                s=str(int(f))
        except: pass
    return s
