from faker import Faker
import pandas as pd
import numpy as np
fake = Faker()
NumRows = [1000, 10000, 100000, 250000, 500000, 1000000, 2000000] 
for num in NumRows:
    profileData = [fake.profile() for i in range(num)]
    df = pd.DataFrame(profileData)
    df.to_csv("{0}_input.csv".format(num), index=False)
    print("Saved the file {0}_input.csv".format(num))

print("All dummy data created")
print("----------------------")