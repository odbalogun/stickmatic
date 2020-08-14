def msisdn_formatter(msisdn):
    """
    Formats the number to the International format with the Nigerian prefix
    """
    # remove +
    msisdn = str(msisdn).replace('+', '')

    if msisdn[:3] == '234':
        return msisdn

    if msisdn[0] == '0':
        msisdn = msisdn[1:]
    return f"234{msisdn}"
