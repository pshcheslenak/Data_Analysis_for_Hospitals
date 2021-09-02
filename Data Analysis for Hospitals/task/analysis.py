import pandas as pd

pd.set_option('display.max_columns', 8)

df_general = pd.read_csv('test/general.csv')
df_prenatal = pd.read_csv('test/prenatal.csv')
df_sports = pd.read_csv('test/sports.csv')

df_general.dropna(how='all', inplace=True)

df_prenatal.dropna(how='all', inplace=True)
df_prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'}, inplace=True)
df_prenatal['gender'] = ['f' for gender in df_prenatal.gender]

df_sports.dropna(how='all', inplace=True)
df_sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'}, inplace=True)

df_hospitals = pd.concat([df_general, df_prenatal, df_sports], ignore_index=True)
df_hospitals.dropna(subset=['hospital'], inplace=True)
df_hospitals.drop(columns='Unnamed: 0', inplace=True)
df_hospitals['gender'] = ['f' if gender in ('female', 'woman') else gender for gender in df_hospitals.gender]
df_hospitals['gender'] = ['m' if gender in ('male', 'man') else gender for gender in df_hospitals.gender]
df_hospitals.fillna(value={'bmi': 0, 'diagnosis': 0, 'blood_test': 0, 'ecg': 0, 'ultrasound': 0, 'mri': 0, 'xray': 0,
                           'children': 0, 'months': 0}, inplace=True)
df_hospitals.reset_index()

# print(df_hospitals.shape)
# print(df_hospitals.sample(n=20, random_state=30))

hospitals = df_hospitals.hospital.unique()
statistics = []  # results

# Hospital has the highest number of patients
hospital_patients = {}
for hospital in hospitals:
    hospital_patients[hospital] = df_hospitals[df_hospitals['hospital'] == hospital].hospital.count()

statistics.append(max(hospital_patients, key=hospital_patients.get))

# Share of the patients in the general hospital suffers from stomach-related issues
hospital_general_stomach_issues = df_general[df_general['diagnosis'] == 'stomach'].diagnosis.count()
statistics.append(round(hospital_general_stomach_issues / hospital_patients['general'], 3))

# Share of the patients in the sports hospital suffers from dislocation-related issues
hospital_sports_dislocation_issues = df_sports[df_sports['diagnosis'] == 'dislocation'].diagnosis.count()
statistics.append(round(hospital_sports_dislocation_issues / hospital_patients['sports'], 3))

# The difference in the median ages of the patients in the general and sports hospitals
hospital_median_ages = {}
for hospital in hospitals:
    hospital_median_ages[hospital] = \
        df_hospitals[df_hospitals['hospital'] == hospital].age.sum() / hospital_patients[hospital]

statistics.append(hospital_median_ages['general'] - hospital_median_ages['sports'])

# In hospital the blood test was taken the most often and how many blood tests
hospital_blood_test = {}
for hospital in hospitals:
    hospital_blood_test[hospital] = \
        df_hospitals[(df_hospitals['hospital'] == hospital) & (df_hospitals['blood_test'] == 't')].hospital.count()

# In hospital the blood test was taken the most often
statistics.append(max(hospital_blood_test, key=hospital_blood_test.get))
statistics.append(max(hospital_blood_test.values()))
# Report
print(f'The answer to the 1st question is {statistics[0]}')
print(f'The answer to the 2nd question is {statistics[1]}')
print(f'The answer to the 3rd question is {statistics[2]}')
print(f'The answer to the 4th question is {statistics[3]}')
print(f'The answer to the 5th question is {statistics[4]}, {statistics[5]} blood tests')
