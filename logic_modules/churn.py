def apply(row):
    if row.get("Subscription_Level") == "Free" and row.get("Num_Sessions", 100) < 10:
        row["Churned"] = True
    elif row.get("Subscription_Level") == "Enterprise" and row.get("Pages_Visited", 0) > 40:
        row["Churned"] = False
    elif row.get("Credit_Score", 999) < 450 and row.get("Annual_Income", 0) < 40000:
        row["Churned"] = True
    else:
        from faker import Faker
        row["Churned"] = Faker().pybool()
    return row
