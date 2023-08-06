import os
import numpy as np
import csv
from tqdm import trange
import sys
import pandas as pd
import itertools
from copy import deepcopy
from dataclasses import dataclass, asdict
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET

@dataclass
class QuenchSweep:
    VarToQuench: str = ""
    iStartQuench: np.ndarray = np.array([])
    ValToQuench: np.ndarray = np.array([])
    QuenchCopy: np.array = np.array([])

@dataclass
class Cable:
    A_CableInsulated: np.ndarray = np.array([])
    f_SC: np.ndarray = np.array([])
    f_ST: np.ndarray = np.array([])
    SCtype: np.ndarray = np.array([])
    STtype: np.ndarray = np.array([])
    Tc0_NbTi: np.ndarray = np.array([])
    Bc20_NbTi: np.ndarray = np.array([])
    c1_Ic_NbTi: np.ndarray = np.array([])
    c2_Ic_NbTi: np.ndarray = np.array([])
    alpha_NbTi: float = 0.59
    Jc_Nb3Sn0: np.ndarray = np.array([])
    Tc0_Nb3Sn: np.ndarray = np.array([])
    Bc20_Nb3Sn: np.ndarray = np.array([])

PossibleQuenchVar = ["tStartQuench", "lengthHotSpot_iStartQuench", "vQ_iStartQuench"]

class ParameterSweep(object):
    def __init__(self, ParametersLEDET):
        self.ParametersLEDET = ParametersLEDET
        self.ParametersToSweep = []
        self.ParameterMatrix = np.array([])
        self.SweepMatrix = np.array([])
        self.VoidRatio = np.array([])
        self.QuenchSweep = QuenchSweep()

    def _addToParameterMatrix(self, values):
        if(self.ParameterMatrix.size == 0):
            self.ParameterMatrix = values
            return
        lenNew = values.shape[1]
        lenOld = self.ParameterMatrix.shape[1]
        if(lenNew > lenOld):
            fill = np.zeros((self.ParameterMatrix.shape[0],lenNew-lenOld))
            self.ParameterMatrix = np.hstack((self.ParameterMatrix, fill))
        elif(lenNew < lenOld):
            fill = np.zeros((1, lenOld-lenNew))
            values = np.reshape(np.append(values, fill), (1, lenOld))
        self.ParameterMatrix = np.vstack((self.ParameterMatrix, values))

    def cleanParameterMatrix(self):
        self.ParameterMatrix = np.array([])
        self.__cleanParametersToSweep()

    def __cleanParametersToSweep(self):
        self.ParametersToSweep = []

    def __cleanSweepMatrix(self):
        self.SweepMatrix = np.array([])

    def generatePermutations(self):
        list_iterator = iter(self.ParameterMatrix)
        r = self.ParameterMatrix[0, :][self.ParameterMatrix[0, :] != 0]
        if self.ParameterMatrix[0, :][0] == 0:
            r = np.append([0], r)
        next(list_iterator)
        r = np.reshape(r, (r.size, 1))

        for ro in list_iterator:
            temp_mat = np.array([])
            k = ro[ro !=0]
            if(ro[0]==0):
                k = np.append([0], k)

            for l in itertools.product(r, k):
                tupleSize = np.array(l[0]).size
                if(tupleSize > 1):
                    if(temp_mat.size == 0):
                        temp_mat = np.append(l[0], l[1])
                    else:
                        temp = np.append(l[0], l[1])
                        temp_mat = np.vstack((temp_mat, temp))
                else:
                    if (temp_mat.size == 0):
                        temp_mat = np.array(l)
                    else:
                        temp_mat = np.vstack((temp_mat, np.array(l)))
            r = temp_mat
        self.SweepMatrix = r.astype(float)

    def _checkSetClass(self, Parameter):
        if Parameter in self.ParametersLEDET.Inputs.__annotations__:
            return "Inputs"
        if Parameter in self.ParametersLEDET.Options.__annotations__:
            return "Options"
        if Parameter in self.ParametersLEDET.Plots.__annotations__:
            return "Plots"
        if Parameter in self.ParametersLEDET.Variables.__annotations__:
            return "Variables"

    def _generateImitate(self, classvalue, value):
        if type(classvalue) == np.ndarray:
            v = deepcopy(classvalue)
            v = np.where(self.ParametersLEDET.Inputs.polarities_inGroup != 0, value, v)
        else:
            v = value
        return v

    def _generateImitate_Quench(self, classvalue, value):
        if type(classvalue) == np.ndarray:
            v = deepcopy(self.QuenchSweep.QuenchCopy)
            if len(self.QuenchSweep.iStartQuench.shape) > 1:
                for i in range(self.QuenchSweep.iStartQuench.shape[1]):
                    v[self.QuenchSweep.iStartQuench[int(value) -1, i]-1] = self.QuenchSweep.ValToQuench[int(value) - 1, i]
                    v[self.QuenchSweep.iStartQuench[int(value) -1, i]-1] = self.QuenchSweep.ValToQuench[int(value) - 1, i]
            else:
              v[self.QuenchSweep.iStartQuench[int(value)-1]-1] = self.QuenchSweep.ValToQuench[int(value)-2]
              v[self.QuenchSweep.iStartQuench[int(value)-1]-1] = self.QuenchSweep.ValToQuench[int(value)-2]
        return v

    def loadSweepMatrixFromExcel(self, file):
        self.__cleanSweepMatrix()
        self.__cleanParametersToSweep()
        self.cleanParameterMatrix()
        df = pd.read_excel(file, header=None)
        first = 0
        for column in df:
            if first < 2:
                first = first +1
                continue
            cp = df[column].values
            self.ParametersToSweep = np.append(self.ParametersToSweep, cp[0])
            if first == 2:
                self.SweepMatrix = cp[1:]
                first = 3
                continue
            self.SweepMatrix = np.vstack((self.SweepMatrix, cp[1:]))
        self.SweepMatrix = self.SweepMatrix.transpose()

    def setCurrentLUT(self, currentLvl):
        LUT =  self.ParametersLEDET.Inputs.I_PC_LUT
        LUT[LUT != 0] = currentLvl
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, 'Inputs'), 'I_PC_LUT', LUT)

    def cpCu_nist_mat(self, T):
        density = 8960
        cpCu_perMass = np.zeros(T.size)
        T[T < 4] = 4
        idxT1 = np.where(T < 300)
        idxT2 = np.where(T >= 300)
        dc_a = -1.91844
        dc_b = -0.15973
        dc_c = 8.61013
        dc_d = -18.996
        dc_e = 21.9661
        dc_f = -12.7328
        dc_g = 3.54322
        dc_h = -0.3797

        logT1 = np.log10(T[idxT1])
        tempVar = \
        dc_a + dc_b * (logT1)**1 + dc_c * (logT1)**2 + dc_d * (logT1)**3 + \
        dc_e * (logT1)**4 + dc_f * (logT1)**5 + dc_g * (logT1)** 6 + dc_h * (logT1)**7
        cpCu_perMass[idxT1] = 10**tempVar

        cpCu_perMass[idxT2]= 361.5 + 0.093 * T[idxT2]
        cpCu = density * cpCu_perMass
        return cpCu

    def cpNbTi_cudi_mat(self, T, B):
        Tc0 = 9.2
        Bc20 = 14.5
        alpha = .59
        B[B>= Bc20] = Bc20-10E-4

        Tc = Tc0 * (1 - B / Bc20)**alpha
        cpNbTi = np.zeros(T.size)

        idxT1 = np.where(T <= Tc)
        idxT2 = np.where((T > Tc) & (T <= 20.0))
        idxT3 = np.where((T > 20) & (T <= 50))
        idxT4 = np.where((T > 50) & (T <= 175))
        idxT5 = np.where((T > 175) & (T <= 500))
        idxT6 = np.where((T > 500) & (T <= 1000))
        idxT7 = np.where(T > 1000)

        p1 = [0.00000E+00,    4.91000E+01,   0.00000E+00,   6.40000E+01,  0.00000E+00]
        p2 = [0.00000E+00,   1.62400E+01,   0.00000E+00,  9.28000E+02,   0.00000E+00]
        p3 = [-2.17700E-01,   1.19838E+01,   5.53710E+02, - 7.84610E+03,  4.13830E+04]
        p4 = [-4.82000E-03,  2.97600E+00, -7.16300E+02,  8.30220E+04,  -1.53000E+06]
        p5 = [-6.29000E-05, 9.29600E-02, -5.16600E+01,  1.37060E+04,  1.24000E+06]
        p6 = [0.00000E+00, 0.00000E+00,  -2.57000E-01,  9.55500E+02,  2.45000E+06]
        p7 = [0, 0, 0, 0, 3.14850E+06]

        cpNbTi[idxT1] = p1[0] * T[idxT1]**4 + p1[1] * T[idxT1]**3 + p1[2] * T[idxT1]**2 + p1[3] * T[idxT1] + p1[4]
        cpNbTi[idxT2] = p2[0] * T[idxT2]**4 + p2[1] * T[idxT2]**3 + p2[2] * T[idxT2]**2 + p2[3] * T[idxT2] + p2[4]
        cpNbTi[idxT3] = p3[0] * T[idxT3]**4 + p3[1] * T[idxT3]**3 + p3[2] * T[idxT3]**2 + p3[3] * T[idxT3] + p3[4]
        cpNbTi[idxT4] = p4[0] * T[idxT4]**4 + p4[1] * T[idxT4]**3 + p4[2] * T[idxT4]**2 + p4[3] * T[idxT4] + p4[4]
        cpNbTi[idxT5] = p5[0] * T[idxT5]**4 + p5[1] * T[idxT5]**3 + p5[2] * T[idxT5]**2 + p5[3] * T[idxT5] + p5[4]
        cpNbTi[idxT6] = p6[0] * T[idxT6]**4 + p6[1] * T[idxT6]**3 + p6[2] * T[idxT6]**2 + p6[3] * T[idxT6] + p6[4]
        cpNbTi[idxT7] = p7[0] * T[idxT7]**4 + p7[1] * T[idxT7]**3 + p7[2] * T[idxT7]**2 + p7[3] * T[idxT7] + p7[4]
        return cpNbTi

    def quenchPropagationVelocity(self, I, B, T_bath, cable):
        L0 = 2.44E-08
        A_CableBare = cable.A_CableInsulated * (cable.f_SC + cable.f_ST)
        f_SC_inStrand = cable.f_SC / (cable.f_SC + cable.f_ST)
        f_ST_inStrand = cable.f_ST / (cable.f_SC + cable.f_ST)
        I = abs(I)
        J_op = I / A_CableBare

        Tc = cable.Tc0_NbTi * (1 - B / cable.Bc20_NbTi) ** cable.alpha_NbTi
        Tcs= (1 - I / (cable.c1_Ic_NbTi + cable.c2_Ic_NbTi * B)) * Tc
        Ts = (Tcs + Tc) / 2

        cp_ST = self.cpCu_nist_mat(Ts)
        cp_SC = self.cpNbTi_cudi_mat(Ts, B)
        cp = cp_ST * f_ST_inStrand + cp_SC * f_SC_inStrand
        vQ = J_op / cp * ((L0 * Ts) / (Ts - T_bath))**0.5
        idxInfQuenchVelocity=np.where(Tcs <= T_bath)
        vQ[idxInfQuenchVelocity]=1E6
        return vQ

    def acquireBField(self, ROXIE_File):
        reader = csv.reader(open(ROXIE_File), delimiter="\t")
        Inom = self.ParametersLEDET.Options.Iref
        reader = csv.reader(open(ROXIE_File))
        B_Field = np.array([])
        stack = 0
        for row in reader:
            if not row: continue
            row_s = np.array(row[0].split())
            if not stack:
                B_Field = np.array(row_s[1:])
                stack = 1
            else:
                B_Field = np.vstack((B_Field, np.array(row_s)))
        B_Field = B_Field[1:].astype(float)
        BX = B_Field[:, 5].transpose()
        BY = B_Field[:, 6].transpose()
        f_mag_X_all = BX / Inom
        f_mag_Y_all = BY / Inom
        f_mag = (f_mag_X_all**2 + f_mag_Y_all**2) ** 0.5
        B = f_mag * self.ParametersLEDET.Inputs.I00

        B[B > 10E6]=10E-6
        return B

    def repeatCable(self, cable):
        nT = self.ParametersLEDET.Inputs.nT
        nT = nT.astype(int)
        newCable = Cable()
        for attribute in cable.__annotations__:
            if attribute == 'alpha_NbTi': continue
            x = np.ndarray([])
            x = getattr(cable, attribute)
            x = np.repeat(x, nT)
            setattr(newCable, attribute, x)
        return newCable

    def adjust_vQ(self, ROXIE_File):
        if max(self.ParametersLEDET.Inputs.nStrands_inGroup) > 1:
            print('vQ calculation only supports single-stranded wires so far!. Abort.')
            return
        I = self.ParametersLEDET.Inputs.I00
        B = self.acquireBField(ROXIE_File)
        T_bath = self.ParametersLEDET.Inputs.T00
        cable = Cable()
        cable.A_CableInsulated = (self.ParametersLEDET.Inputs.wBare_inGroup+2*self.ParametersLEDET.Inputs.wIns_inGroup) \
                                * (self.ParametersLEDET.Inputs.hBare_inGroup+2*self.ParametersLEDET.Inputs.hIns_inGroup)
        cable.f_SC = self.ParametersLEDET.Inputs.f_SC_strand_inGroup * \
                        (self.ParametersLEDET.Inputs.wBare_inGroup*self.ParametersLEDET.Inputs.hBare_inGroup)/cable.A_CableInsulated
        cable.f_ST = (1- self.ParametersLEDET.Inputs.f_SC_strand_inGroup) * \
                    (self.ParametersLEDET.Inputs.wBare_inGroup*self.ParametersLEDET.Inputs.hBare_inGroup)/cable.A_CableInsulated
        cable.SCtype = self.ParametersLEDET.Inputs.SCtype_inGroup
        cable.STtype = self.ParametersLEDET.Inputs.STtype_inGroup
        cable.Tc0_NbTi = self.ParametersLEDET.Inputs.Tc0_NbTi_ht_inGroup
        cable.Bc20_NbTi = self.ParametersLEDET.Inputs.Bc2_NbTi_ht_inGroup
        cable.c1_Ic_NbTi = self.ParametersLEDET.Inputs.c1_Ic_NbTi_inGroup
        cable.c2_Ic_NbTi = self.ParametersLEDET.Inputs.c2_Ic_NbTi_inGroup
        cable.alpha_NbTi = .59
        cable.Jc_Nb3Sn0 = self.ParametersLEDET.Inputs.Jc_Nb3Sn0_inGroup
        cable.Tc0_Nb3Sn = self.ParametersLEDET.Inputs.Tc0_Nb3Sn_inGroup
        cable.Bc20_Nb3Sn = self.ParametersLEDET.Inputs.Bc2_Nb3Sn_inGroup
        cable = self.repeatCable(cable)

        vQ = 2*self.quenchPropagationVelocity(I, B, T_bath, cable)*1.21
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "vQ_iStartQuench", vQ)

    def prepareSimulation(self, MagnetName, folder, cleanFolder = True,  OffsetNumber = 0, ROXIE_File = '', clean = False):
        Adjust_vQ = 0
        if ROXIE_File:
            Adjust_vQ =1
        #1a. Clean SweepMatrix
        self.__cleanSweepMatrix()
        #1b. Clean Folder
        if not os.path.isdir(folder):
            os.mkdir(folder)
        if cleanFolder:
            filelist = [f for f in os.listdir(folder)]
            for f in filelist:
                if "selfMutualInductanceMatrix" in f:
                    continue
                if clean:
                    os.remove(os.path.join(folder, f))
        #2. Generate Permutations
        self.generatePermutations()
        #3. For loop for all Simulations
        toolbar_width = self.SweepMatrix.shape[0]
        file_name_stub = MagnetName
        for i in trange(self.SweepMatrix.shape[0], file=sys.stdout, desc='Excel Files'):
            file_name = folder + file_name_stub + "_" + str(i+OffsetNumber) +".xlsx"
            for j in range(self.SweepMatrix.shape[1]):
                SetClass = self._checkSetClass(self.ParametersToSweep[j])
                if self.ParametersToSweep[j] in PossibleQuenchVar:
                    if self.QuenchSweep.QuenchCopy.size == 0:
                        self.QuenchSweep.QuenchCopy = deepcopy(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j]))
                    setValue = self._generateImitate_Quench(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j]), self.SweepMatrix[i,j])
                else:
                    setValue = self._generateImitate(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j]), self.SweepMatrix[i,j])
                self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j], setValue)
                if self.ParametersToSweep[j] == "I00":
                    self.setCurrentLUT(self.SweepMatrix[i,j])
                if (self.ParametersToSweep[j] == "overwrite_f_internalVoids_inGroup"):
                    setVal = self.VoidRatio - self.SweepMatrix[i, j]
                    if any(sV < 0 for sV in setVal):
                        print("Negative externalVoids calculated. Abort Sweep, please check.")
                        return
                    setVal = np.where(self.ParametersLEDET.Inputs.polarities_inGroup != 0, setVal, 0)
                    self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "overwrite_f_externalVoids_inGroup", setVal)
            if Adjust_vQ:
                self.adjust_vQ(ROXIE_File)

            self.ParametersLEDET.writeFileLEDET(file_name)

        #4. Write CSV with all Parameters
        SimNumbers = np.linspace(0,self.SweepMatrix.shape[0]-1,self.SweepMatrix.shape[0])
        df = pd.Series(SimNumbers,index=SimNumbers)
        for i in range(self.SweepMatrix.shape[1]):
            par = pd.Series(self.SweepMatrix[:, i], index=SimNumbers)
            df = pd.concat([df, par], axis=1)
        df.columns = np.concatenate((['Simulation'], self.ParametersToSweep))
        writer = pd.ExcelWriter(folder + "SimulationMatrix.xlsx")
        df.to_excel(writer)
        writer.save()

class MinMaxSweep(ParameterSweep):
    def __init__(self, ParametersLEDET, basePoints):
        super(MinMaxSweep, self).__init__(ParametersLEDET)
        self.basePoints = basePoints

    def change_basePoints(self,basePoints):
        self.basePoints = basePoints

    def __generate_points(self, minimum, maximum, basePoints, type = 'linear'):
        if type=='linear':
            return np.array([np.linspace(minimum, maximum, basePoints)])
        if type == 'logarithmic':
            return np.array([np.logspace(minimum, maximum, num=basePoints)])

    def addParameterToSweep(self, parameter, minimum, maximum, basePoints = 0, type = 'linear'):
        if basePoints == 0:
            basePoints = self.basePoints
        self.ParametersToSweep.append(parameter)
        self.ParametersLEDET.Variables.variableToSaveTxt = np.append(self.ParametersLEDET.Variables.variableToSaveTxt,
                                                                     parameter)
        self.ParametersLEDET.Variables.typeVariableToSaveTxt = np.append(self.ParametersLEDET.Variables.typeVariableToSaveTxt,
                                                                         2)
        sweep_points = self.__generate_points(minimum, maximum, basePoints, type = type)
        self._addToParameterMatrix(sweep_points)

    def addParameterToSweep_Vector(self, parameter, vector):
        self.ParametersToSweep.append(parameter)
        self._addToParameterMatrix(np.array([vector]))

    def _activateHelium(self):
        setValue = self._generateImitate(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, "Inputs"),
                                                                           "polarities_inGroup"), 0)
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "overwrite_f_internalVoids_inGroup", setValue)
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "overwrite_f_externalVoids_inGroup", setValue)

    def addHeliumCrossSection(self, minHe, maxHe, basePoints = 0):
        self._activateHelium()
        cs_bare = self.ParametersLEDET.Inputs.wBare_inGroup*self.ParametersLEDET.Inputs.hBare_inGroup
        cs_ins = (self.ParametersLEDET.Inputs.wBare_inGroup +2*self.ParametersLEDET.Inputs.wIns_inGroup)* \
                (self.ParametersLEDET.Inputs.hBare_inGroup +2*self.ParametersLEDET.Inputs.hIns_inGroup)
        cs_strand = self.ParametersLEDET.Inputs.nStrands_inGroup*np.pi*(self.ParametersLEDET.Inputs.ds_inGroup**2)/4

        strand_total = cs_strand/cs_ins
        ins_total = (cs_ins - cs_bare)/cs_ins
        self.VoidRatio = (cs_bare - cs_strand)/cs_ins
        self.addParameterToSweep("overwrite_f_internalVoids_inGroup", minHe/100.0, maxHe/100.0, basePoints = basePoints)

    def addQuenchSweep(self, VarToQuench, iStartQuench, ValToQuench):
        iStartQuench = np.array(iStartQuench)
        ValToQuench = np.array(ValToQuench)
        if not iStartQuench.shape == ValToQuench.shape:
            print("Variable To Sweep and provided Values do not have same shape. Abort.")
        self.QuenchSweep.VarToQuench = np.array(VarToQuench)
        self.QuenchSweep.iStartQuench = np.array(iStartQuench)
        self.QuenchSweep.ValToQuench = np.array(ValToQuench)
        self.ParametersToSweep.append(VarToQuench)
        try:
            imitate = np.linspace(1, len(ValToQuench), len(ValToQuench))
        except:
            imitate = np.array([0])
        self._addToParameterMatrix(np.array([imitate]))

    def addCurrentSweep(self, ultimateCurrent, basePoints, current_vector = np.array([])):
        print('Warning: Current Sweep only works for FPA \n')
        if len(current_vector) == 0:
            if basePoints <= 2:
                print('Less than 3 current level provided. Set first current as level.')
                current_vector = np.array([ultimateCurrent])
            nomCurrent = self.ParametersLEDET.Options.Iref
            current_vector = np.linspace(10, ultimateCurrent, basePoints-1)
            current_vector = np.append(current_vector, nomCurrent)
        self.addParameterToSweep_Vector('I00', current_vector)

