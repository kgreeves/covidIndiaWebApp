from app.modules.schemas import State
from numpy import round


def compute_percent_recovered(data: State) -> float:
    values = list(data.values())[0]
    total_cases = values['deceased'] + values['recovered']
    pct_recovered = round(values['recovered']/total_cases, 2)
    return pct_recovered
