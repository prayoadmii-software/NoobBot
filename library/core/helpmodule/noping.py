def _clean(input: str) -> str:
    cleaned = input.replace(" ", "").lower()

    return cleaned

# Check Resault Code Glide
# 0 = No Ping
# 1 = @everyone Ping
# 2 = @here Ping
# 3 = @role Ping

def check(input: str) -> int:
    cleaned = _clean(input)

    if "@everyone" in cleaned:
        return 1
    elif "@here" in cleaned:
        return 2
    elif "<@&" in cleaned:
        return 3
    else:
        return 0