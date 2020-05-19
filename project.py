import random
from random import randint

def main():

    #-------------INICIALIZAÇÃO------------------

    #creation of airports
    locl = 0
    nFlightsCreated = 0 
    for i in range(nAirports):
        an = random.choice(airportNames)
        airportNames.remove(an)
        d = random.choice(dimensions)
        #nl = random.randint(1,3)        #numero de lanes para partidas
        #nla = random.randint(1,3)       #numero de lanes para chegadas
        #nfm = random.randint(1,3)       #numero maximo de voos que partem daquele aeroporto
        nl = 5
        nla = 1
        nfm = 5
        nFlightsCreated += nfm
        locl = random.randint(locl, locl + 20)
        locl += 30  #garantir que estao pelo menos a 10 de distancia uns dos outros
        if (locl % 2) != 0:
            locl -= 1
        airport = Airport(an, d, nl, nla, nfm, locl)
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
        airplane = Airplane(iden, d, fl, ac)
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
        
            try:
                p = random.choice(airplanesAvailableToChooseFrom)
            except:
                print("no more airplanes available for creation")

            id_plane = p.id
            airplane = p
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

            delay = 0

            flight = Flight(id_plane, airp.name, departure, 1, aa.name, departure + t, 1, t, d, delay, airplane)
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


    '''print("Número total de voos: " + str(len(flights)))

    for pora in airports:
        print("----Aeroporto seguinte----")
        print("Airport name: " + pora.name)
        print("Airport localization: " + str(pora.localization))
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
        print("--------------------")'''

    #----------COMEÇA O CRONOMETRO--------------

    time = 0

    while flights != []:
        
        #mudar o estado para dizer que o aviao ja partiu
        for apt in airports:
            if time in apt.departuresFlights:
                for f in apt.departuresFlights[time]:
                    #cria um dicionario do tempo das chegadas no aeroporto de chegada
                    apt_aa_name = f.getArrivalAirport()
                    arrivalTimeOficial = int(f.getDepartureTime() + f.getFlightTime())
                    for i in range(len(airports)):
                        if airports[i].name == apt_aa_name:
                            if arrivalTimeOficial in airports[i].arrivalFlights:
                                airports[i].arrivalFlights[arrivalTimeOficial].append(f)
                            else:    
                                airports[i].arrivalFlights[arrivalTimeOficial] = []
                                airports[i].arrivalFlights[arrivalTimeOficial].append(f)
        
        t1 = time + 1
        for a in airports:
            l = 0
            arri = t1
            delay = 0
            priority = []
            if t1 in a.arrivalFlights:
                arrayFlights = a.arrivalFlights[t1]
                for af in arrayFlights:
                    if af.getDelay() >= 5:
                        priority.append(af)

                msp = mergeSort(priority)
                ms = mergeSort(arrayFlights)

                if msp != []:
                    for j in range(len(msp)):
                        ms.insert(0,msp[-1])
                        msp.remove(msp[-1])

                for i in range(len(ms)):
                    if a.nLanesArrivals == l:
                        #Muda hora do arrival
                        arri += 1
                        ms[i].setArrivalTime(arri)
                        ms[i].setDelay(delay + 1)
                        #se ja houver o tempo de descolagem no dicionario, entao adicionamos a lista o voo, se nao cria
                        if ms[i].getArrivalTime() in a.arrivalFlights:
                            a.arrivalFlights[ms[i].getArrivalTime()].append(ms[i])
                        else:
                            a.arrivalFlights[ms[i].getArrivalTime()] = []
                            a.arrivalFlights[ms[i].getArrivalTime()].append(ms[i])
                        
                        l = 1

                        delay += 1
                    
                    else:
                        l += 1
                        aeroporto.flights[i].setArrivalLane(l)    
                        #se ja houver o tempo de aterragem no dicionario, entao adicionamos a lista o voo, se nao cria
                        if ms[i].getArrivalTime() in a.arrivalFlights:
                            a.arrivalFlights[ms[i].getArrivalTime()].append(ms[i])
                        else:
                            a.arrivalFlights[ms[i].getArrivalTime()] = []
                            a.arrivalFlights[ms[i].getArrivalTime()].append(ms[i])

        for a in airports:
            for f in a.flights:
                if f.getDepartureTime() < time:
                    currentFuelLevel = f.getAirplane().getFuelLevel()
                    updateLevel = round(currentFuelLevel - 0.2, 2)
                    f.getAirplane().setFuelLevel(updateLevel)


        #condição de paragem
        maximo = 0
        for a in airports:
            for key in a.arrivalFlights:
                if key > maximo:
                    maximo = key
        
        if time > maximo:
            break

        time += 1

    print("Número total de voos: " + str(len(flights)))

    for pora in airports:
        print("----Aeroporto seguinte----")
        print("Airport name: " + pora.name)
        print("Airport localization: " + str(pora.localization))
        print("Airport numero de voos: " + str(pora.nFlightsMax))
        print("Airport numero de pistas: " + str(pora.nLanes))
        print("Airport numero de pistas para aterrar: " + str(pora.nLanesArrivals))
        print("Airport dimension: " + str(pora.dim))
        for i in range(len(pora.flights)):
            print("------Próximo voo-------")
            print("Airport flights: " + pora.flights[i].planeID)
            print("Airport departure: " + pora.flights[i].departureAirport)
            print("Airport departure time: " + str(pora.flights[i].departureTime))
            print("Airport departure lane: " + str(pora.flights[i].departureLane))
            print("Airport arrival: " + pora.flights[i].arrivalAirport)
            print("Airport arrival time: " + str(pora.flights[i].arrivalTime))
            print("Airport arrival lane: " + str(pora.flights[i].arrivalLane))
            print("Delay: " + str(pora.flights[i].delay))
            print("Flight distance: " + str(pora.flights[i].flightDistance))
            print("Flight time: " + str(pora.flights[i].flightTime))
            print("Fuel Level: " + str(pora.flights[i].getAirplane().fuelLevel))
        print("--------------------")


#########################
###  FUNÇÃO AUXILIAR  ###
#########################

def mergeSort(arr):
    if arr == []:
        return arr

    if len(arr) > 1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R):
            #lst  = a2.broadcast()
            #res = a1.receiveBroadcast(lst)
            lst = L[i].getAirplane().broadcast()
            res = R[j].getAirplane().receiveBroadcast(lst)
            if res > 0:
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

    return arr


#####################
###    CLASSES    ###
#####################

class Airplane:
    def __init__(self, iden, dim, fuelLevel, airlineCompany):
        self.id = iden
        self.dim = dim
        self.fuelLevel = fuelLevel
        self.airlineCompany = airlineCompany

    def broadcast(self):
        propertiesList = [self.id, self.dim, self.airlineCompany, self.fuelLevel]
        return propertiesList

    #se retornar 1 é sinal que o self tem vantagem
    #ordem: Dimensão > Nível de comnustível > Companhia Aerea
    def receiveBroadcast(self, otherList):
        id = otherList[0]
        d = otherList[1]
        ac = otherList[2]
        fl = otherList[3]
        res = 1
        if self.dim == d:
            if self.fuelLevel > fl:
                res = 0
            elif self.fuelLevel == fl:
                indSelf = airlineCompanies.index(self.airlineCompany)
                indOther = airlineCompanies.index(ac)
                if indOther < indSelf:
                    res = 0 
        elif self.dim < d:
            res = 0
        return res

    def setFuelLevel(self, fl):
        self.fuelLevel = fl

    def getFuelLevel(self):
        return self.fuelLevel

class Airport:
    def __init__(self, name, dim, nLanes, nLanesArrivals, nFlightsMax, localization):
        self.name = name
        self.dim = dim
        self.nLanes = nLanes
        self.nLanesArrivals = nLanesArrivals
        self.nFlightsMax = nFlightsMax
        self.localization = localization
        self.airplanes = []
        self.flights = []
        self.departuresFlights = {}
        self.arrivalFlights = {}



class Flight:
    def __init__(self, planeID, departureAirport, departureTime, departureLane, arrivalAirport, arrivalTime, arrivalLane, flightTime, flightDistance, delay, airplane):
        self.planeID = planeID
        #self.nPassengers = nPassengers
        self.arrivalAirport = arrivalAirport
        self.arrivalTime = arrivalTime
        self.departureAirport = departureAirport
        self.departureTime = departureTime
        self.departureLane = departureLane
        self.arrivalLane = arrivalLane
        self.flightTime = flightTime
        self.flightDistance = flightDistance
        self.delay = delay
        self.airplane = airplane

    def getDepartureTime(self):
        return self.departureTime 

    def setDepartureTime(self, departureTime):
        self.departureTime = departureTime

    def getArrivalTime(self):
        return self.arrivalTime 

    def setArrivalTime(self, arrivalTime):
        self.arrivalTime = arrivalTime

    def setDepartureLane(self, lane):
        self.departureLane = lane

    def setArrivalLane(self, lane):
        self.arrivalLane = lane

    def setDelay(self, d):
        self.delay = d

    def getDelay(self):
        return self.delay

    def getFlightTime(self):
        return self.flightTime 

    def getArrivalAirport(self):
        return self.arrivalAirport

    def getAirplane(self):
        return self.airplane


#####################
###      MAIN     ###
#####################

nPlanes = 0
nAirports = 2

dimensions = [100, 150, 180]
airlineCompanies = ['TAP', 'KLM', 'Air France', 'Emirates', 'Qatar', 'British Airways', 'Vueling', 'Iberia', 'Ryanair', 'Easy Jet']
airportNames = ['Lisboa', 'Madrid', 'Paris']
airportNamesSelected = ['Lisboa', 'Madrid', 'Paris']


airplanes = []
airports = []
flights = []

if __name__ == "__main__":
    main()
