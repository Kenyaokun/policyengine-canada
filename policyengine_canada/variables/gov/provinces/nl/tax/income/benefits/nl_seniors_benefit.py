from policyengine_canada.model_api import *


class nl_seniors_benefit(Variable):
    value_type = float
    entity = Person
    label = "Newfoundland and Labrador Seniors Benefit"
    definition_period = YEAR
    defined_for = ProvinceCode.NL

    def formula(person, period, parameters):
        p = parameters(period).gov.provinces.nl.tax.income.benefits

        senior_eligibility = person("age", period) >= p.age_eligibility

        # Calculate the senior's income & their spouses' income
        spouse_income = person("spouse_income", period) * person(
            "is_spouse", period
        )
        personal_income = person("individual_net_income", period)
        total_family_income = spouse_income + personal_income

        income_eligibility = total_family_income < p.upper_income_threshold

        senior_benefit = income_eligibility * (
            p.max_amount
            - income_eligibility
            * p.rate
            * (total_family_income - p.lower_income_threshold)
        )

        return min_(senior_eligibility * senior_benefit, p.max_amount)
