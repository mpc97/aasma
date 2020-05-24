import random
from random import randint
import time

def main():

    #-------------INICIALIZAÇÃO------------------

    totalDelay = 0
    avgDelay = 0.0
    totalFlights = 0

    #creation of airports
    locl = 0
    nFlightsCreated = 0 
    for i in range(nAirports):
        an = random.choice(airportNames)
        airportNames.remove(an)
        nl = 3

        nla = 1 #numero pistas de aterragem
        nfm = 100 #numero de avioes que partem por aeroporto
        
        nFlightsCreated += nfm
        locl = random.randint(locl, locl + 20)
        locl += 30  #garantir que estao pelo menos a 10 de distancia uns dos outros
        if (locl % 2) != 0:
            locl -= 1
        airport = Airport(an, nl, nla, nfm, locl)
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
        airplane.calculateUtility()
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


    #----------COMEÇA O CRONOMETRO--------------

    timer = 0

    while flights != []:
        for apt in airports:
            if timer in apt.departuresFlights:
                for f in apt.departuresFlights[timer]:
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
        
        t1 = timer + 1
        for a in airports:
            l = 0
            arri = t1
            delay = 0
            priorityDelays = []
            priorityFuel = []


            ########################
            ##    NÃO APAGAR, ESTE FAZ AS PRIORIDADES QUANDO ESTAMOS A FALAR DE ATRIBUTOS FIXOS
            ########################

            '''if t1 in a.arrivalFlights:
                arrayFlights = a.arrivalFlights[t1]
                for af in arrayFlights:
                    if af.getDelay() >= 5:
                        priority.append(af)
                    if af.getAirplane().fuelLevel <= 20:
                        priorityFuel.append(af)

                #print(a.name)
                #print('Flights: ' + str(arrayFlights))
                #for fl in arrayFlights:
                    #print('dimensao dos avioes dos voos: ' + str(fl.getAirplane().dim))

                msp = mergeSort(priority)
                msf = mergeSortFuel(priorityFuel)
                ms = mergeSort(arrayFlights)

                #Só para visualizar que as prioridades estão a funcionar
                #print('Depois do merge')
                #print('Flights: ' + str(arrayFlights))
                #for fl in arrayFlights:
                    #print('dimensao dos avioes dos voos: ' + str(fl.getAirplane().dim))'''

            ########################
            ##    NÃO APAGAR, ESTE FAZ AS PRIORIDADES QUANDO ESTAMOS A FALAR DE  UTILIDADES
            ########################
            
            if t1 in a.arrivalFlights:
                arrayFlights = a.arrivalFlights[t1]
                for af in arrayFlights:
                    if af.getDelay() >= 5:
                        af.getAirplane().setUtility(10)
                        priorityDelays.append(af)
                    if af.getAirplane().fuelLevel <= 20:
                        priorityFuel.append(af)

                #Só para visualizar que as prioridades estão a funcionar
                '''print(a.name)
                print('Flights: ' + str(arrayFlights))
                for fl in arrayFlights:
                    print('fuelLevel dos voos: ' + str(fl.getAirplane().fuelLevel))'''
                
                #msp = mergeSortUtilities(priorityDelays)
                #msf = mergeSortFuel(priorityFuel)
                #ms = mergeSortUtilities(arrayFlights)

                msp = mergeSort(priorityDelays)
                msf = mergeSortFuel(priorityFuel)
                ms = mergeSort(arrayFlights)
                
                #Só para visualizar que as prioridades estão a funcionar
                '''print('Depois do merge')
                print('Flights: ' + str(arrayFlights))
                for fl in ms:
                    print('fuelLevel dos voos: ' + str(fl.getAirplane().fuelLevel))'''



                if msp != []:
                    for j in range(len(msp)):
                        ms.insert(0,msp[-1])
                        msp.remove(msp[-1])

                if msf != []:
                    for j in range(len(msf)):
                        ms.insert(0,msf[-1])
                        msf.remove(msf[-1])

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
                        ms[i].setArrivalLane(l)    
                        #se ja houver o tempo de aterragem no dicionario, entao adicionamos a lista o voo, se nao cria
                        if ms[i].getArrivalTime() in a.arrivalFlights:
                            a.arrivalFlights[ms[i].getArrivalTime()].append(ms[i])
                        else:
                            a.arrivalFlights[ms[i].getArrivalTime()] = []
                            a.arrivalFlights[ms[i].getArrivalTime()].append(ms[i])

        for a in airports:
            for f in a.flights:
                if f.getArrivalTime() > timer:
                    currentFuelLevel = f.getAirplane().getFuelLevel()
                    perc = 0.5
                    newFuel = round(currentFuelLevel - perc, 2)
                    f.getAirplane().setFuelLevel(newFuel)

        #condição de paragem
        maximo = 0
        for a in airports:
            for key in a.arrivalFlights:
                if key > maximo:
                    maximo = key

        if time.time() > timeout:
            break
        
        if timer > maximo:
            break

        timer += 1

    #---------- Delay ---------
    for a in airports:
        totalFlights += len(a.flights)
        for f in a.flights:
            totalDelay += f.delay
    
    avgDelay = totalDelay / totalFlights

    print("\n-------INICIO DOS RESULTS---------")
    print("Total Delay in all flights: " + str(totalDelay))
    print("Total flights: " + str(totalFlights))
    print("Average: " + str(avgDelay))
    print("-------FIM DOS RESULTS---------\n")

    print("Número total de voos: " + str(len(flights)))

    for pora in airports:
        print("----Aeroporto seguinte----")
        print("Airport name: " + pora.name)
        print("Airport localization: " + str(pora.localization))
        print("Airport numero de voos: " + str(pora.nFlightsMax))
        print("Airport numero de pistas: " + str(pora.nLanes))
        print("Airport numero de pistas para aterrar: " + str(pora.nLanesArrivals))
        for i in range(len(pora.flights)):
            print("------Próximo voo-------")
            print("Airport flights: " + pora.flights[i].planeID)
            print("Airline Company: " + pora.flights[i].getAirplane().airlineCompany)
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
            print("Uility: " + str(pora.flights[i].getAirplane().utility))
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
            lst = L[i].getAirplane().broadcast()
            res = R[j].getAirplane().receiveBroadcast(lst)
            if res == 0:
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

def mergeSortUtilities(arr):
    if arr == []:
        return arr

    if len(arr) > 1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSortUtilities(L) # Sorting the first half 
        mergeSortUtilities(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R):
            #lst  = a2.broadcast()
            #res = a1.receiveBroadcast(lst)
            plane1 = L[i].getAirplane().utility
            plane2 = R[j].getAirplane().utility
            if plane1 > plane2: 
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

def mergeSortFuel(arr):
    if arr == []:
        return arr

    if len(arr) > 1:
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSortUtilities(L) # Sorting the first half 
        mergeSortUtilities(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R):
            #lst  = a2.broadcast()
            #res = a1.receiveBroadcast(lst)
            plane1 = L[i].getAirplane().fuelLevel
            plane2 = R[j].getAirplane().fuelLevel
            if plane1 > plane2: 
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

def getIndex(array, thing):
    return array.index(thing)



#####################
###    CLASSES    ###
#####################

class Airplane:
    def __init__(self, iden, dim, fuelLevel, airlineCompany):
        self.id = iden
        self.dim = dim
        self.fuelLevel = fuelLevel
        self.airlineCompany = airlineCompany
        self.utility = 0

    def calculateUtility(self):
        indAc = getIndex(airlineCompanies, self.airlineCompany)
        indD = getIndex(dimensions, self.dim)
        uAC = airlineCompaniesUtilities[indAc]
        uD = dimensionsUtilities[indD]

        self.utility = uAC + uD
    
    def setUtility(self, u):
        self.utility += u

    def getUtility(self):
        return self.utility

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
        
        if self.fuelLevel <= 20:
            if self.fuelLevel == fl:
                if self.dim == d:
                    indSelf = airlineCompanies.index(self.airlineCompany)
                    indOther = airlineCompanies.index(ac)
                    if indOther < indSelf:
                        res = 0  
            elif self.fuelLevel > fl:
                res = 0
        else:
            if self.dim == d:
                indSelf = airlineCompanies.index(self.airlineCompany)
                indOther = airlineCompanies.index(ac)
                if indOther < indSelf:
                    res = 0 
            elif self.dim < d:
                res = 0

        '''if self.fuelLevel <= 20:
            if self.fuelLevel == fl:
                indSelf = airlineCompanies.index(self.airlineCompany)
                indOther = airlineCompanies.index(ac)
                if indSelf == indOther:
                    if self.dim < d:
                        res = 0 
            elif self.fuelLevel > fl:
                res = 0
        else:
            indSelf = airlineCompanies.index(self.airlineCompany)
            indOther = airlineCompanies.index(ac)
            if indSelf == indOther:
                if self.dim < d:
                    res = 0
            elif indOther < indSelf:
                res = 0'''
        
        return res

    def setFuelLevel(self, fl):
        self.fuelLevel = fl

    def getFuelLevel(self):
        return self.fuelLevel

class Airport:
    def __init__(self, name, nLanes, nLanesArrivals, nFlightsMax, localization):
        self.name = name
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
nAirports = 10
timeout = time.time() + 5

dimensions = [200, 180, 150, 100, 85]
dimensionsUtilities = [3.2, 2.4, 1.6, 0.8, 0]
airlineCompanies = ['TAP', 'KLM', 'Air France', 'Emirates', 'Qatar', 'British Airways', 'Vueling', 'Iberia', 'Ryanair', 'Easy Jet']
airlineCompaniesUtilities = [4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0]
airportNames = ['Lisboa', 'Madrid', 'Paris', 'Berlim' , 'Frankfurt', 'Roma', 'Veneza', 'Zagreb', 'Manchester', 'Porto']
airportNamesSelected = ['Lisboa', 'Madrid', 'Paris', 'Berlim' , 'Frankfurt', 'Roma', 'Veneza', 'Zagreb', 'Manchester', 'Porto']


airplanes = []
airports = []
flights = []

if __name__ == "__main__":
    main()
