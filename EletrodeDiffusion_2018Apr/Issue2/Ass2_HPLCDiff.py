import numpy as np
import matplotlib.pyplot as plt
import xlwt

# Abstract the concentration into linear density in HPLC

xUnit = 1E-4   # meter
tUnit = 2E-4    # sec
txRatio = tUnit / xUnit

diffCoefficient = 2E-5          # Diffusion coefficient
initConcentration = 1           # Initial iteration concentration(mmol/L)

limitDistanceIter = 50          # Max iteration of distance
limitTimeIter = 100             # Max iteration of time

errTolerant = 1E-5              # Define the percentage error

# Define the matrix of concentration with respect to position and time each iteration
# Unit (mmol/m3)
concentrationMatrix = np.zeros((limitTimeIter, limitDistanceIter)) 
# Define the matrix of exert flux with respect to position and time each iteration
fluxMatrix = np.zeros((limitTimeIter - 1, limitDistanceIter - 1)) 

# Initialize the concentration matrix
for i in range(0, limitTimeIter) : 
    concentrationMatrix[i, 0] = initConcentration

# Cal a specific flux at one position at a certain time
def singlePosFlux(presTimeIter, presPosIter) :
    
    fluxMatrix[presTimeIter - 1, presPosIter - 1] = -diffCoefficient * \
        (concentrationMatrix[presTimeIter - 1, presPosIter] - concentrationMatrix[presTimeIter - 1, presPosIter - 1]) / xUnit
    '''
    concentrationMatrix[presTimeIter, presPosIter] = concentrationMatrix[presTimeIter - 1, presPosIter] + \
    (fluxMatrix[presTimeIter - 1, presPosIter - 1] * txRatio)
    '''
    if(presPosIter < limitDistanceIter - 1) : 
        fluxMatrix[presTimeIter - 1, presPosIter - 1] -= -diffCoefficient * \
        (concentrationMatrix[presTimeIter - 1, presPosIter + 1] - concentrationMatrix[presTimeIter - 1, presPosIter]) / xUnit
    
    concentrationMatrix[presTimeIter, presPosIter] = concentrationMatrix[presTimeIter - 1, presPosIter] + \
    (fluxMatrix[presTimeIter - 1, presPosIter - 1] * txRatio)    
    
    #print(presPosIter)
    return

# Cal a series of position in a specific time
def timeFlux(presTimeIter) : 
    for posIter in range(1, limitDistanceIter) : 
        
        if (abs((concentrationMatrix[presTimeIter, posIter] - concentrationMatrix[presTimeIter, posIter - 1]) /\
            concentrationMatrix[presTimeIter, posIter]) <= errTolerant) : break
        
        singlePosFlux(presTimeIter, posIter)

# cal the whole concentration with the finite element method
def wholeFluxCal() : 
    for timeIter in range(1, limitTimeIter) : 
        timeFlux(timeIter)


wholeFluxCal()
print(concentrationMatrix)

# Write into a .xls file
'''
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('Data_%dIter_%dNum' % (limitTimeIter, limitDistanceIter), cell_overwrite_ok=True)
sheet.write(0, 1, 'sample cols ->')
sheet.write(1, 0, 'iteration rows -v')

for i in range(1, limitTimeIter + 1) :
    for j in range(1, limitDistanceIter + 1) :
        sheet.write(i, j, concentrationMatrix[i - 1, j - 1])

book.save('./Ass1_Data_%dIter_%dNum.xls' % (limitTimeIter, limitDistanceIter))
'''
# Draw the plot

xList = np.linspace(0, limitDistanceIter * xUnit, limitDistanceIter, endpoint=False)

plt.title('Concentration distribution\n%d iterations, %d sample points, x_Unit = %s m, t_Unit = %s s'\
 % (limitTimeIter, limitDistanceIter, format(xUnit, '.2e'), format(tUnit, '.2e')))
for iter in range(0, limitTimeIter) : 
    tmpBlue = (iter * 7) / (limitTimeIter * 8)
    plt.plot(xList, concentrationMatrix[iter], color=(0.875 - tmpBlue, 0.125, tmpBlue))
plt.legend()

plt.xlabel('displacement / m')
plt.ylabel('concentration / (mmol/m3)')
plt.show()
