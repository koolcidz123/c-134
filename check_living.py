import csv
import pandas
import plotly_express as px
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

rows = []

with open("Final_Final.csv","r") as f:
    csvReader = csv.reader(f)
    for row in csvReader :
        rows.append(row)
headers = rows[0]
planetData = rows[1 : ]

temp_planet_data = list(planetData)
for data in temp_planet_data:
    planetMass = data[3]
    if planetMass.lower() == "unknown":
        planetData.remove(data)
        continue
    else:
        planetMassValue = planetMass.split(" ")[0]
        planetMassRef = planetMass.split(" ")[1]
        if planetMassRef == "Jupiters":
            planetMassValue = float(planetMassValue)* 317.8
        data[3] = planetMassValue
    planetRadius = data[7]
    if planetRadius.lower() == "unknown":
        planetData.remove(data)
        continue
    else:
        planetRadiusValue= planetRadius.split(" ")[0]
        planetRadiusRef = planetRadius.split(" ")[2]
        if planetRadiusRef == "Jupiter":
            planetRadiusValue = float(planetRadiusValue)*11.2
        data[7] = planetRadiusValue

temp_planet_data_rows = list(planetData)

planet_mass = []
planet_radius = []
planet_names = []

for data in temp_planet_data_rows:
    planet_mass.append(data[3])
    planet_radius.append(data[7])
    planet_names.append(data[1])

gravity = []

for index,name in enumerate(planet_names):
    gravity_index = (float(planet_mass[index])*5.972e+24)/(float(planet_radius[index])*float(planet_radius[index])*6371000*6371000)*6.674e-11
    gravity.append(gravity_index)

low_gravity_planets = []

for index,gravity1 in enumerate(gravity):
    if gravity1 <= 100:
        low_gravity_planets.append(temp_planet_data_rows[index])
# print(len(low_gravity_planets))


very_low_gravity_planets = []
for index,gravity1 in enumerate(gravity):
    if gravity1 <= 10:
        very_low_gravity_planets.append(temp_planet_data_rows[index])
# print(len(very_low_gravity_planets))

planetTypeValues = []

for data in planetData:
    planetTypeValues.append(data[6])

# print(list(set(planetTypeValues)))
# fig = px.scatter(x=planet_radius, y= planet_mass)
# fig.show()

x = []
for index,planetmass in enumerate(planet_mass):
    tempList = [planet_radius[index],planetmass]
    x.append(tempList)

wCss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init='k-means++',random_state=42)
    kmeans.fit(x)
    wCss.append(kmeans.inertia_)

# plt.figure(figsize=(10,5))
# sns.lineplot(range(1,11),wCss,marker='o',color='red')
# plt.title('Elbow Method')
# plt.xlabel('No.of Clusters')
# plt.ylabel('WCSS')
# plt.show()

# ig = px.scatter(x=planet_radius, y=planet_mass,color=planetTypeValues)
# fig.show()

suitablePlanets =[]
for data in low_gravity_planets:
    if data[6].lower() == "terrestrial" or data[6].lower() == "super earth":
        suitablePlanets.append(data)
# print(len(suitablePlanets))

temp_suitable_plants = list(suitablePlanets)

for data in temp_suitable_plants:
    if data[8].lower() == "unknown":
        suitablePlanets.remove(data)

for data in suitablePlanets:
    if data[9].split(" ")[1].lower() == "days":
        data[9] = float(data[9].split(" ")[0])
    else:
        data[9] = float(data[9].split(" ")[0]) * 365
    data[8] = float(data[8].split(" ")[0])

orbital_period = []
orbital_radius = []

for data in suitablePlanets:
    orbital_period.append(data[9])
    orbital_radius.append(data[8])

# fig = px.scatter(x=orbital_radius, y=orbital_period)
# fig.show()

goldiLogPlanets = list(suitablePlanets)
temp_goldiLogPlanets = list(suitablePlanets)

for data in temp_goldiLogPlanets:
    if data[8] <= 0.38 or data[8] >= 2:
        goldiLogPlanets.remove(data)

# print(len(goldiLogPlanets))
# print(len(suitablePlanets))


planet_speed = []
for data in suitablePlanets:
    distance = 2*3.14*(data[8]*1.496e+9)
    time = data[9]*86400
    speed = distance/time
    planet_speed.append(speed)

speed_supporting_list = list(suitablePlanets)
temp_speed_list = list(suitablePlanets)
for index, data in enumerate(temp_speed_list):
    if planet_speed[index] > 200:
        speed_supporting_list.remove(data)

# print(len(speed_supporting_list))

finalDic = {}

for index,data in enumerate(planetData):
    features = []

    #gravity
    gravity = (float(data[3])*5.972e+24)/(float(data[7])*float(data[7])*6371000*6371000)*6.674e-11
    try:
        if gravity < 100:
            features.append("gravity")
    except:
        pass

    #planet_type
    try:
        if data[6].lower() == "terrestrial" or data[6].lower() == "super earth":
            features.append("planet_type")
    except:
        pass

    #goldiLock
    try:
        if data[8] > 0.38 or data[8] < 2:
            features.append("goldiLock")
    except:
        pass

    #Speeeed
    try:
        distance = 2 * 3.14 * (data[8] * 1.496e+9)
        time = data[9] * 86400
        speed = distance / time
        if speed < 200:
            features.append("Speeed")
    except:
        pass


    finalDic[index]=features

goldi_Lock_Planets = 0
for key,value in finalDic.items():
    if "goldiLock"in value:
        goldi_Lock_Planets = goldi_Lock_Planets + 1

# print(goldi_Lock_Planets)

speeed_Planets = 0
for key,value in finalDic.items():
    if "Speeed"in value:
        speeed_Planets = speeed_Planets + 1

print(speeed_Planets)

#print(finalDic)