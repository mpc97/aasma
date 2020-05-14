import random
from random import randint

def main():
    #creation of airports
    locl = 0
    nFlightsCreated = 0 
    for i in range(nAirports):
        an = random.choice(airportNames)
        airportNames.remove(an)
        d = random.choice(dimensions)
        nl = random.randint(1,3)
        nfm = random.randint(1,3)
        nFlightsCreated += nfm
        l = random.randint(locl, locl + 20)
        locl += 30  #garantir que estao pelo menos a 10 de distancia uns dos outros
        airport = Airport(an, d, nl, nfm, l)
        airports.append(airport)
    nPlanes = nFlightsCreated

    #creation of airplanes 
    airplanesAvailableToChooseFrom = [] #lista usada para fazer com o id dos voos seja unico
    for i in range(nPlanes):
        iden = "id" + str(i)
        #np = random.choice(passengers)
        d = random.choice(dimensions)
        fl = 100
        ac = random.choice(airlineCompanies)
        airplane = Airplane(iden, d, fl, ac, 1)
        airplanes.append(airplane)
        airplanesAvailableToChooseFrom.append(airplane)

    #distribute the airplanes for the different airports
    airplanesToDistribute = airplanes
    for plane in airplanesToDistribute:
        ap = random.choice(airports)
        ap.airplanes.append(plane)
        airplanesToDistribute.remove(plane)

    #creation of flight --> se calhar fazer uma função
    #airplanesAvailableToChooseFrom = airplanes

    for airp in airports:
        for j in range(airp.nFlightsMax):        
            #np = random.choice(passengers)
            aa = airp
            id_plane = ''

            #criar arrival airport que nao seja o mesmo do departure, tendo que ter um aviao de tamanhos semelhantes ou menor
            while aa.name == airp.name:
                aa = random.choice(airports)
            
            #garantir que o aviao vai ter uma dimensao inferior a do aeroporto (acho que vou ignorar esta parte)
            '''while id_plane == '':
                print('Preso no garantir que plane cabe no aero de chegada')
                print(airplanesAvailableToChooseFrom)
                p = random.choice(airplanesAvailableToChooseFrom)
                if p.dim <= aa.dim:
                    id_plane = p.id
                    airplanesAvailableToChooseFrom.remove(p)'''

            try:
                p = random.choice(airplanesAvailableToChooseFrom)
            except:
                print("no more airplanes available for creation")

            id_plane = p.id
            if airplanesAvailableToChooseFrom != []:
                airplanesAvailableToChooseFrom.remove(p)
                
            #time that lasts the flight, which is the distance divided by 2(random number)
            t = (airp.localization - aa.localization) / 2
            t = abs(t)

            #distance is the subtraction of the localization of the two airports
            d = airp.localization - aa.localization
            d = abs(d)

            #cria com partida com 0, preocupamo-nos depois
            departure = 0

            flight = Flight(id_plane, airp.name, departure, 1, aa.name, departure + t, 1, t, d)
            airp.flights.append(flight)
            flights.append(flight)

    #criar as horas de partida, distribuindo consoante o numero de pistas do aeroporto
    for aeroporto in airports:
        lane = 0 #começa a 0 para o primeiro voo poder ser no departure 0
        dep = 0
        for i in range(len(aeroporto.flights)):
            if aeroporto.nLanes == lane:
                #Muda hora do departure
                dep += 5
                aeroporto.flights[i].setDepartureTime(dep)
                aeroporto.flights[i].setArrivalTime(aeroporto.flights[i].getDepartureTime() + aeroporto.flights[i].getFlightTime())
                #se ja houver o tempo de descolagem no dicionario, entao adicionamos a lista o voo, se nao cria
                if aeroporto.flights[i].getDepartureTime() in aeroporto.departuresFlights:
                    aeroporto.departuresFlights[aeroporto.flights[i].getDepartureTime()].append(aeroporto.flights[i])
                else:
                    aeroporto.departuresFlights[aeroporto.flights[i].getDepartureTime()] = []
                    aeroporto.departuresFlights[aeroporto.flights[i].getDepartureTime()].append(aeroporto.flights[i])
                
                lane = 1
            
            else:
                lane += 1
                aeroporto.flights[i].setDepartureLane(lane)    
                #se ja houver o tempo de descolagem no dicionario, entao adicionamos a lista o voo, se nao cria
                if aeroporto.flights[i].getDepartureTime() in aeroporto.departuresFlights:
                    aeroporto.departuresFlights[aeroporto.flights[i].getDepartureTime()].append(aeroporto.flights[i])
                else:
                    aeroporto.departuresFlights[aeroporto.flights[i].getDepartureTime()] = []
                    aeroporto.departuresFlights[aeroporto.flights[i].getDepartureTime()].append(aeroporto.flights[i])



    print("Número total de voos: " + str(len(flights)))

    for pora in airports:
        print("----Aeroporto seguinte----")
        print("Airport name: " + pora.name)
        print("Airport numero de voos: " + str(pora.nFlightsMax))
        print("Airport numero de pistas: " + str(pora.nLanes))
        print("Airport dimension: " + str(pora.dim))
        for i in range(len(pora.flights)):
            print("------Próximo voo-------")
            print("Airport flights: " + pora.flights[i].planeID)
            print("Airport departure time: " + str(pora.flights[i].departureTime))
            print("Airport lane: " + str(pora.flights[i].departureLane))
            print("Airport departure: " + pora.flights[i].departureAirport)
            print("Airport arrival: " + pora.flights[i].arrivalAirport)
            print("Arrival time: " + str(pora.flights[i].arrivalTime))
            print("Flight distance: " + str(pora.flights[i].flightDistance))
            print("Flight time: " + str(pora.flights[i].flightTime))
        print("--------------------")

    '''while True:
        break'''
        
#####################
###    CLASSES    ###
#####################

class Airplane:
    def __init__(self, iden, dim, fuelLevel, airlineCompany, boardingDetails):
        self.id = iden
        #self.nPassengers = nPassengers
        self.dim = dim
        self.fuelLevel = fuelLevel
        self.airlineCompany = airlineCompany
        self.boardingDetails = boardingDetails

class Airport:
    def __init__(self, name, dim, nLanes, nFlightsMax, localization):
        self.name = name
        self.dim = dim
        self.nLanes = nLanes
        self.nFlightsMax = nFlightsMax
        self.localization = localization
        self.airplanes = []
        self.flights = []
        self.departuresFlights = {}


class Flight:
    def __init__(self, planeID, departureAirport, departureTime, departureLane, arrivalAirport, arrivalTime, boardingDetails, flightTime, flightDistance):
        self.planeID = planeID
        #self.nPassengers = nPassengers
        self.arrivalAirport = arrivalAirport
        self.arrivalTime = arrivalTime
        self.departureAirport = departureAirport
        self.departureTime = departureTime
        self.departureLane = departureLane
        self.boardingDetails = boardingDetails
        self.flightTime = flightTime
        self.flightDistance = flightDistance

    def getDepartureTime(self):
        return self.departureTime 

    def setDepartureTime(self, departureTime):
        self.departureTime = departureTime

    def setArrivalTime(self, arrivalTime):
        self.arrivalTime = arrivalTime

    def setDepartureLane(self, lane):
        self.departureLane = lane

    def getFlightTime(self):
        return self.flightTime 


#####################
###      MAIN     ###
#####################

nPlanes = 0
nAirports = 3

#passengers = [250, 300, 350]
dimensions = [100, 150, 180]
airlineCompanies = ['aaa', 'bbb', 'ccc', 'ddd']
airportNames = ['Lisboa', 'Madrid', 'Paris']
airportNamesSelected = ['Lisboa', 'Madrid', 'Paris']


airplanes = []
airports = []
flights = []

if __name__ == "__main__":
    main()


