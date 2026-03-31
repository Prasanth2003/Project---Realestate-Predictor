def predict_purchase(price: float, location: str, size: float, income: float, amenities: str) -> dict:
    """
    A simple heuristic 'model' to calculate the likelihood of purchasing a property.
    """
    score = 0
    max_score = 100

    # 1. Affordability: Income vs Price
    # Let's say we expect the property price to be at most 5x the annual income.
    affordability_ratio = price / (income if income > 0 else 1)
    if affordability_ratio < 3:
        score += 40
    elif affordability_ratio < 5:
        score += 20
    elif affordability_ratio < 7:
        score += 5

    # 2. Location preference
    location = location.lower()
    if location in ['downtown', 'suburbs', 'city center']:
        score += 20
    elif location in ['rural', 'countryside']:
        score += 10
    else:
        score += 15
        
    # 3. Size preference
    if size > 1500:
        score += 20
    elif size > 800:
        score += 10

    # 4. Amenities
    amenities = amenities.lower()
    if 'pool' in amenities:
        score += 10
    if 'garage' in amenities:
        score += 10
        
    probability = min(score, 99) # Cap at 99%
    likelihood = "Yes" if probability >= 50 else "No"
    
    return {
        "likelihood": likelihood,
        "probability": probability
    }
