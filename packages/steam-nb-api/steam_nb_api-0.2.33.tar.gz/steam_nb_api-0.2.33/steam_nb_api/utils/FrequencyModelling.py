from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.utils.SelfMutualInductanceCalculation import SelfMutualInductanceCalculation
import numpy as np
import os
import sys
import datetime
import xlrd
from pathlib import Path
from steam_nb_api.utils import workbook as w # changed to be more general
from steam_nb_api.utils import arrays as a # changed to be more general
from py4j.java_gateway import launch_gateway, java_import, JavaGateway, JavaObject, GatewayParameters, Py4JNetworkError

class FrequencyModelling:
    # This dataclass is created to generate frequency based netlist of any LHC magnet. The class is based around
    # creating to different models, one based on the turns of the magnet and one based of the groups of the magnet.
    # This is done so that the simulation can be done faster if needed by the group based model, at the cost of loosing
    # detail. Which is especially useful for the very complex magnet models normally taking hours to run.

    def __init__(self, nameMagnet,excelfilename,roxieextension,headerLines,swanpath,cappath,inputpath):
        # Initiate the model. The function loads in the relevant files from LEDET and Roxie, as specfied in the input arguments.
        # The function further more calculates and saves relevant data to be used in by other functions.
        #
        # NOTE: New groups (called turn-groups in specific cases) are created since the coupling coefficient of the
        #       original groups can't be calculated correctly
        #
        # ASSUMPTION: this code is always run inside SWAN_projects for now, meaning that the first part of the string,
        #             in particulairly the user, can be found by searching for 'SWAN_projects' in os.getcwd()
        #
        # Input Arguments
        # nameMagnet                : The name of the magnet. This is used to find the correct file folder, LEDET excel file and Roxie file.
        # excelfilename             : Everything that is not the magnet name in the LEDET excel file name.
        # roxieextension            : Similair to excelfilename however only part of the filename is needed, since the 'Iron' and 'SelfField' part of the name is found automatically
        # headerlines               : The amount of headerlines in the Roxie file
        # swanpath                  : The partial path string from 'SWAN_projects' and onwards to the file folder containing the LEDET file
        #
        # Capacitance specifications:
        # magnet_center             : The geometric center of the magnet in mm
        # epsR_LayerToBore          : The relative permittivity of the insulation between the bore and turns
        # epsR_LayerToCollar        : The relative permittivity of the insulation between the collar and turns
        # epsR_BetweenLayers        : The relative permittivity of the insulation between the layers of the magnet
        # hIns_InnerLayerToBore     : The thickness of the insulation between the bore and turns
        # hIns_OuterLayerToCollar   : The thickness of the insulation between the collar and turns
        # hIns_BetweenLayers        : The thickness of the insulation between the between the layers of the magnet
        # LayerPattern_Quadrant     : The pattern of the layers of the magnet for each quadrant
        # GeoArr                    : GeoArr
        #
        # Inputs:
        # flag_strandCorrection     : Passed directly to the 'calculateInductance' function
        # flag_sumTurnToTurn        : Passed directly to the 'calculateInductance' function
        # flag_writeOutput          : Passed directly to the 'calculateInductance' function
        # dev_max                   : The maximum allowed relative deviation when comparing the calculated turns based
        #                             M-matrix to the one found in the LEDET file.
        # flag_CapacitanceToBore    : If the flag is high the capacitance between the bore and the magnet is calculated
        # flag_CapacitanceToCollar  : If the flag is high the capacitance between the collar and the magnet is calculated
        # magnet_center             : The center coordinates of the magnet
        # epsR_LayerToBore          : The relative permittivity of the insulation between the turns and the bore
        # epsR_LayerToCollar        : The relative permittivity of the insulation between the turns and the collar
        # hIns_InnerLayerToBore     : The thickness of the insulation between the turns and the bore
        # hIns_OuterLayerToCollar   : The thickness of the insulation between the turns and the collar
        # LayerPattern_Quadrant     : The number of groups (not turn-groups) per Layer in one Quadrant/Sextant (Outer first)
        # Capacity_T2T              : An array that lists the values of the capacitance between the nodes specified by Contact_To and Contact_From
        # Contact_To                : An array of nodes to which the capacitance should be added (between Contact_To and Contact_From)
        # Contact_From              : An array of nodes to which the capacitance should be added (between Contact_To and Contact_From)
        # lag_T2TCapWidth           : If the flag is high the capacitance between the turns width-wise is calculated
        # flag_T2TCapHeight         : If the flag is high the capacitance between the turns heihgt-wise is calculated
        # epsR_BetweenLayers        : The relative permittivity of the additional insulation between the layers of the turns
        # hIns_BetweenLayers        : The thickness of the additional insulation between the layers of the turns
        # flag_writeFile            : If true a '.cir' file is created based on the magnet name. The file has an extension
        #                             specifying if it is a turn or group based model. The file is created inside a subdirectory,
        #                             also named in relation to either turns or groups, of the folder containing the notebook
        #                             used to run the code.
        # flag_R_Par                : If true the function adds a parallel resistance with the value 'R_par' to the netlist
        # R_Par                     : The value of the added parallel resistance (Implemented as a parameter in the netlist)
        # flag_E_loops              : If true the function adds a edyy current loops based on 'E_loops' to the netlist
        # E_loops                   : The values of resistance, inductance and coupling coefficients of the added eddy current
        #                             loops. FORMAT: [[L1,R1,K1] , [L2,R2,K2] , ... , [LX,RX,KX]]
        # F_SCALE_C_GROUND          : The default scaling of the capacitance to ground in the netlist (added as a parameter)
        # F_SCALE_C_T2T             : The default scaling of the capacitance between turns/groups in the netlist
        #                             (added as a parameter)
        # F_SCALE_L                 : The default scaling of the self inductance in the netlist (added as a parameter)
        # F_SCALE_R                 : The default scaling of the resistance in the netlist (added as a parameter)
        # pointsPerDecade           : Points per decade in the AC simulation
        # startFrequency            : Start frequency of the AC simulation
        # stopFrequency             : Stop frequency of the AC simulation
        eospath = os.getcwd()
        eossplit = eospath.split(os.path.sep)
        SWAN_index = eossplit.index('SWAN_projects')  # If this line throws an error it is most likely because the current working directory doesn't include 'SWAN_projects'
        eospath = ''
        for j in range(SWAN_index):
            eospath = eospath + eossplit[j] + '/'
        filename = eospath + swanpath + excelfilename

        capname = eospath + cappath

        inputname = eospath + inputpath

        xl_workbook = xlrd.open_workbook(capname)
        a = xl_workbook.sheet_by_index(0)

        xl_workbook2 = xlrd.open_workbook(inputname)
        b = xl_workbook2.sheet_by_index(0)

        LEDET = ParametersLEDET()

        LEDET.readLEDETExcel(filename)

        # Acquire data from ROXIE .map2d file
        # Roxie filename autimatically found from LEDET options
        if LEDET.Options.flagIron:
            roxieextension += 'WithIron_'
        else:
            roxieextension += 'NoIron_'
        if LEDET.Options.flagSelfField:
            roxieextension += 'WithSelfField'
        else:
            roxieextension += 'NoSelfField'
        roxieextension = roxieextension + '.map2d'
        fileNameRoxie = eospath + swanpath + nameMagnet + roxieextension

        strandToHalfTurn = np.array([])

        x = []
        y = []

        ## Read file
        file = open(fileNameRoxie, "r")
        fileContent = file.read()

        ## Separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow) - 1):
            if index > headerLines:
                fc = fileContentByRow[index]
                row = fc.split()
                strandToHalfTurn = np.hstack([strandToHalfTurn, int(row[1])])
                x = np.hstack([x, float(row[3]) / 1000])  # in [m]
                y = np.hstack([y, float(row[4]) / 1000])  # in [m]
        # Count number of groups defined
        nCoilSectionsDefined = np.max(LEDET.Inputs.GroupToCoilSection)
        nCoilSectionsDefined = nCoilSectionsDefined.astype(np.int64)
        nGroupsDefined = len(LEDET.Inputs.GroupToCoilSection)

        print(str(nCoilSectionsDefined) + ' coil sections defined.')
        print(str(nGroupsDefined) + ' groups defined.')

        # Number of half-turns in each group
        nT = LEDET.Inputs.nT
        nT = nT.astype(np.int64)  # needs to be integers (LEDET is inputtet as float)

        nHalfTurns = int(sum(nT));
        nTurns = int(nHalfTurns / 2)

        nStrandsL = LEDET.Inputs.nStrands_inGroup
        nStrandsL = np.int_(nStrandsL)
        nS = np.repeat(nStrandsL, nT)  # Number of strands in each half-turn

        strandToHalfTurn = np.int_(strandToHalfTurn)

        #polarity from LEDET
        polaritiesL1 = np.repeat(LEDET.Inputs.polarities_inGroup, nT)  # polarity for each half turn
        polarities = np.repeat(polaritiesL1, nS)  # polarity for each strand
        polarities = polarities.astype(np.int64)

        # Calculate group to which each half-turn belongs
        indexTstart = np.hstack([1, 1 + np.cumsum(nT[:-1])]);
        indexTstop = np.cumsum(nT);
        HalfTurnToGroup = np.zeros((1, nHalfTurns), dtype=int)
        HalfTurnToGroup = HalfTurnToGroup[0]
        HalfTurnToCoilSection = np.zeros((1, nHalfTurns), dtype=int)
        HalfTurnToCoilSection = HalfTurnToCoilSection[0]
        for g in range(1, nGroupsDefined + 1):
            HalfTurnToGroup[indexTstart[g - 1] - 1:indexTstop[g - 1]] = g
            HalfTurnToCoilSection[indexTstart[g - 1] - 1:indexTstop[g - 1]] = LEDET.Inputs.GroupToCoilSection[g - 1]

        # Calculate group to which each strand belongs
        indexSstart = np.hstack([1, 1 + np.cumsum(nS[:-1])]);
        indexSstop = np.cumsum(nS);
        strandToGroup = np.zeros((1, sum(nS)), dtype=int)
        strandToGroup = strandToGroup[0]
        strandToCoilSection = np.zeros((1, sum(nS)), dtype=int)
        strandToCoilSection = strandToCoilSection[0]
        for ht in range(1, nHalfTurns + 1):
            strandToGroup[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToGroup[ht - 1]
            strandToCoilSection[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToCoilSection[ht - 1]

        # Calculate diameter of each strand
        Ds = np.zeros((1, sum(nS)), dtype=float)
        Ds = Ds[0]
        for g in range(1, nGroupsDefined + 1):
            Ds[np.where(strandToGroup == g)] = LEDET.Inputs.ds_inGroup[g - 1]

        # New groups (called turn-groups in specific cases) since the coupling coefficient of the original groups can't be calculated correctly
        turnGroup_ind = int(nGroupsDefined / 2)
        strandToTurnGroup = np.concatenate((strandToGroup[strandToGroup < turnGroup_ind + 1],strandToGroup[strandToGroup > turnGroup_ind] - turnGroup_ind))

        # number of half turns in each turn-group
        nTG = nT[:turnGroup_ind] + nT[turnGroup_ind:]

        print(str(max(strandToTurnGroup)) + ' turn-groups defined.')

        #Turns to group
        TurnToGroup=HalfTurnToGroup[HalfTurnToGroup < turnGroup_ind + 1]

        # Electrical order
        EO_turns = LEDET.Inputs.el_order_half_turns
        EO_turns = np.int_(EO_turns[EO_turns<nTurns+1])
        temp = TurnToGroup[EO_turns - 1] # The group of each turn in electrical order
        EO_groups = temp[0]
        for i in range(1,len(temp)): # Removing repeat values
            if temp[i-1] != temp[i]:
                EO_groups=np.append(EO_groups,temp[i])
        # A test could be to check if len(EO_groups) == turnGroup_ind

        # Capacitor specifics
        magnets_name = []
        for i in range(0, a.nrows):
            magnets_name.append(a.cell(i, 0).value)
        ind = magnets_name.index(nameMagnet)

        magnets_columns = []
        for i in range(0, a.ncols):
            magnets_columns.append(a.cell(0, i).value)

        magnet_center = np.int_(a.cell(ind, magnets_columns.index('magnet_center (mm)')).value.split(','))

        epsR_LayerToBore = a.cell(ind, magnets_columns.index('epsR_LayerToCollar')).value
        epsR_LayerToCollar = a.cell(ind, magnets_columns.index('epsR_LayerToBore')).value
        epsR_BetweenLayers = a.cell(ind, magnets_columns.index('epsR_BetweenLayers')).value

        hIns_InnerLayerToBore = a.cell(ind, magnets_columns.index('hIns_InnerLayerToBore (m)')).value
        hIns_OuterLayerToCollar = a.cell(ind, magnets_columns.index('hIns_OuterLayerToCollar (m)')).value
        hIns_BetweenLayers = a.cell(ind, magnets_columns.index('hIns_BetweenLayers (m)')).value

        LayerPattern_Quadrant = np.int_(a.cell(ind, magnets_columns.index('LayerPattern_Quadrant')).value.split(','))

        GeoArr = np.int_(a.cell(ind, magnets_columns.index('GeoArr')).value.split(','))
        GeoArr = GeoArr.reshape(np.int_(len(GeoArr) / 2), 2)


        # Inputs

        # magnets name is redone for robustness
        magnets_name = []
        for i in range(0, b.nrows):
            magnets_name.append(b.cell(i, 0).value)
        ind = magnets_name.index(nameMagnet)
        magnets_columns = []
        for i in range(0, b.ncols):
            magnets_columns.append(b.cell(0, i).value)

        flag_R_Par = b.cell(ind, magnets_columns.index('flag_R_Par')).value
        R_Par = b.cell(ind, magnets_columns.index('R_Par (Ohm)')).value

        # Eddy current loops
        flag_E_loops = b.cell(ind, magnets_columns.index('flag_E_loops')).value
        E_loops = np.array(b.cell(ind, magnets_columns.index('E_loops [L (H), R (Ohm), k]')).value.split(','))
        E_loops = E_loops.astype(np.float)
        E_loops = E_loops.reshape(np.int_(len(E_loops) / 3), 3)
        E_loops_old = [[1e-3 , 1e-1 , 0.3] , [1e-3 , 1, 0.65]] # Array needs to be formatted like this -> [[L1,R1,K1] , [L2,R2,K2] , ... , [LX,RX,KX]]

        # Scales
        F_SCALE_C_GROUND = b.cell(ind, magnets_columns.index('F_SCALE_C_GROUND')).value
        F_SCALE_C_T2T = b.cell(ind, magnets_columns.index('F_SCALE_C_T2T')).value
        F_SCALE_L = b.cell(ind, magnets_columns.index('F_SCALE_L')).value
        F_SCALE_R = b.cell(ind, magnets_columns.index('F_SCALE_R')).value

        # Self-mutual inductance calculation, using SMIC (https://cernbox.cern.ch/index.php/s/37F87v3oeI2Gkp3)
        flag_strandCorrection = b.cell(ind, magnets_columns.index('flag_strandCorrection')).value
        flag_sumTurnToTurn = b.cell(ind, magnets_columns.index('flag_sumTurnToTurn')).value
        flag_writeOutput = b.cell(ind, magnets_columns.index('flag_writeOutput')).value
        dev_max=b.cell(ind, magnets_columns.index('dev_max')).value # maximum relative deviation

        # Capacitance to ground
        flag_CapacitanceToBore = b.cell(ind, magnets_columns.index('flag_CapacitanceToBore')).value
        flag_CapacitanceToCollar = b.cell(ind, magnets_columns.index('flag_CapacitanceToCollar')).value

        # Capacitance between turns/groups
        flag_T2TCapWidth = b.cell(ind, magnets_columns.index('flag_T2TCapWidth')).value
        flag_T2TCapHeight = b.cell(ind, magnets_columns.index('flag_T2TCapHeight')).value

        # Netlist
        pointsPerDecade = int(b.cell(ind, magnets_columns.index('pointsPerDecade')).value)
        startFrequency = b.cell(ind, magnets_columns.index('startFrequency')).value
        stopFrequency = b.cell(ind, magnets_columns.index('stopFrequency')).value

        flag_writeFile = b.cell(ind, magnets_columns.index('flag_writeFile')).value

        # self section
        self.nameMagnet = nameMagnet
        self.LEDET = LEDET
        self.x = x
        self.y = y
        self.nT = nT
        self.nTG = nTG
        self.strandToHalfTurn = strandToHalfTurn
        self.strandToGroup = strandToGroup
        self.strandToTurnGroup = strandToTurnGroup
        self.HalfTurnToGroup = HalfTurnToGroup
        self.TurnToGroup = TurnToGroup
        self.nStrandsL = nStrandsL
        self.nS = nS
        self.Ds = Ds
        self.polarities = polarities
        self.nHalfTurns = nHalfTurns
        self.nTurns = nTurns
        self.turnGroup_ind = turnGroup_ind
        self.eospath = eospath
        self.EO_groups = EO_groups
        self.EO_turns = EO_turns

        self.magnet_center = magnet_center
        self.epsR_LayerToBore = epsR_LayerToBore
        self.epsR_LayerToCollar = epsR_LayerToCollar
        self.epsR_BetweenLayers = epsR_BetweenLayers
        self.hIns_InnerLayerToBore = hIns_InnerLayerToBore
        self.hIns_OuterLayerToCollar = hIns_OuterLayerToCollar
        self.hIns_BetweenLayers = hIns_BetweenLayers
        self.LayerPattern_Quadrant = LayerPattern_Quadrant
        self.GeoArr = GeoArr

        self.flag_R_Par = flag_R_Par
        self.R_Par = R_Par
        self.flag_E_loops = flag_E_loops
        self.E_loops = E_loops
        self.F_SCALE_C_GROUND = F_SCALE_C_GROUND
        self.F_SCALE_C_T2T = F_SCALE_C_T2T
        self.F_SCALE_L = F_SCALE_L
        self.F_SCALE_R = F_SCALE_R
        self.flag_strandCorrection = flag_strandCorrection
        self.flag_sumTurnToTurn = flag_sumTurnToTurn
        self.flag_writeOutput = flag_writeOutput
        self.dev_max = dev_max
        self.flag_CapacitanceToBore = flag_CapacitanceToBore
        self.flag_CapacitanceToCollar = flag_CapacitanceToCollar
        self.flag_T2TCapWidth = flag_T2TCapWidth
        self.flag_T2TCapHeight = flag_T2TCapHeight
        self.pointsPerDecade = pointsPerDecade
        self.startFrequency = startFrequency
        self.stopFrequency = stopFrequency
        self.flag_writeFile = flag_writeFile


    def epsRCabIns(self):
        # Used to translate the insulation type from LEDET to an usuable value in calculations.
        epsR_CabIns = self.LEDET.Inputs.insulationType_inGroup
        epsR_CabIns = np.where(epsR_CabIns == 1, 4.4 , epsR_CabIns) # G10
        epsR_CabIns = np.where(epsR_CabIns == 2, 3.4 , epsR_CabIns) # kapton
        return epsR_CabIns

    def SelfMutualInductance(self):
        # This function uses the 'calculateInductance' function from the 'SelfMutualInductanceCalculation' dataclass
        # to calculate the mutual-inductance (M) matrixes based on turns and groups.
        # The calculated turn based M-matrix is compared to the one from the LEDET file, to check if they are a match.
        # The amount of devation is printed. However since deviation aren't necesarilly cause for concern the code
        # continous, no matter the result of the deviation test.
        # Some corrections are made, so that the length of the magnet, as well as the yoke effect is taken into account.
        # Finally the coupling coefficients (k) matrixes are calculated since PSpice needs those.
        nameMagnet = self.nameMagnet
        LEDET = self.LEDET
        x = self.x
        y = self.y
        nT = self.nT
        nTG = self.nTG
        strandToHalfTurn = self.strandToHalfTurn
        strandToGroup = self.strandToGroup
        strandToTurnGroup = self.strandToTurnGroup
        HalfTurnToGroup = self.HalfTurnToGroup
        nStrandsL = self.nStrandsL
        nS = self.nS
        Ds = self.Ds
        polarities = self.polarities
        nHalfTurns = self.nHalfTurns
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind

        flag_strandCorrection = self.flag_strandCorrection
        flag_sumTurnToTurn = self.flag_sumTurnToTurn
        flag_writeOutput = self.flag_writeOutput
        dev_max = self.dev_max

        coil = SelfMutualInductanceCalculation(x, y, polarities, nS, Ds, strandToHalfTurn, strandToTurnGroup,flag_strandCorrection, flag_sumTurnToTurn, flag_writeOutput,nameMagnet)  # Coilsection changed to groups

        # Calculate self-mutual inductance between half-turns, turns, and turn-groups, per unit length [H/m]
        M_halfTurns_calculated_m, M_turns_calculated_m, M_groups_calculated_m,L_mag0_calculated_m = coil.calculateInductance(x, y, polarities, nS, Ds, strandToHalfTurn, strandToTurnGroup,flag_strandCorrection=0)  # Coilsection changed to groups

        # Self-mutual inductance between turn-groups, per unit length [H/m] (replaces coilsection)
        M_groups0_m = M_groups_calculated_m
        # Self-mutual inductances between turns, per unit length [H/m]
        M_InductanceBlock_m = M_turns_calculated_m
        # Total magnet self-mutual inductance, per unit length [H/m]
        L_mag0_m = L_mag0_calculated_m

        print('')
        print('Total magnet self-inductance per unit length: ' + str(L_mag0_m) + ' H/m')

        # Defining to which inductive block each half-turn belongs
        HalfTurnToInductanceBlock = range(1, int(nTurns + 1))
        HalfTurnToInductanceBlock = []
        for i in range(2):
            for j in range(1, int(nTurns+ 1)):
                HalfTurnToInductanceBlock.append(j)

        # Deviation test
        M_dev = abs(M_InductanceBlock_m - LEDET.Inputs.M_InductanceBlock_m)  # deviation of each element
        M_dev_rel = M_dev / abs(M_InductanceBlock_m)  # relative deviation of each element
        nDev = sum(sum(M_dev_rel > dev_max))  # number of devations in the entire matrix
        sizeM = len(M_dev) * len(M_dev[0])
        print('')
        print('Number of devations: ' + str(nDev) + ' out of ' + str(sizeM))

        # Iron yoke effect
        M_groups_m = M_groups0_m * LEDET.Inputs.fL_L[0]
        M_turns_m = M_turns_calculated_m * LEDET.Inputs.fL_L[0]
        L_mag0_m = L_mag0_calculated_m * LEDET.Inputs.fL_L[0]

        # Self-mutual inductances between turn-groups
        M_groups = M_groups_m * LEDET.Inputs.l_magnet
        # Self-mutual inductances between turns
        M_turns = M_turns_m * LEDET.Inputs.l_magnet
        # Total magnet self-mutual inductance
        L_mag0 = L_mag0_m * LEDET.Inputs.l_magnet
        print('')
        print('Total inductance:')
        print(L_mag0)

        # Changed to M to L for easier comparison to older code
        L_turns = M_turns
        L_groups = M_groups

        # Matrix calc version
        L_turns_diag = np.diagonal(L_turns)
        L_turns_diag_rep = np.tile(L_turns_diag, (len(L_turns), 1))  # this replicates the effect of L_xx[i][i] (or [j][j] i'm not sure, but it shouldn't matter)
        denom_turns = np.sqrt(L_turns_diag_rep.T * L_turns_diag_rep)
        k_turns = L_turns / denom_turns  # matrix alt to k_turns[i][j]=L_turns[i][j]/np.sqrt(L_turns[j][j]*L_turns[i][i])
        L_groups_diag = np.diagonal(L_groups)
        L_groups_diag_rep = np.tile(L_groups_diag, (len(L_groups), 1))  # this replicates the effect of L_xx[i][i] (or [j][j] i'm not sure, but it shouldn't matter)
        denom_groups = np.sqrt(L_groups_diag_rep.T * L_groups_diag_rep)
        k_groups = L_groups / denom_groups  # matrix alt to k_groups[i][j]=L_groups[i][j]/np.sqrt(L_groups[j][j]*L_groups[i][i])

        # replace diagonal with 0's
        np.fill_diagonal(k_turns, 0)
        np.fill_diagonal(k_groups, 0)

        print('')
        print('max |k_turns| (should be lower than 1):')
        print(np.max(abs(k_turns)))

        print('')
        print('max |k_groups| (should be lower than 1):')
        print(np.max(abs(k_groups)))

        return L_turns, L_groups, k_turns, k_groups

    def Resistance(self):
        # The resistance based on turns and groups is calculated.
        # More specifically the resistance of the half turns in each group is calculated with the formula shown below:
        # R = rho_Cu / (pi * strand_diameter^2 / 4 * nStrandsL * fraction_Cu) * magnetic_length
        # Then these resistance values are repeated and summed to create the turn and group based resistance.
        # All the needed information is preloaded into the model by the 'init' function.
        LEDET = self.LEDET
        nT = self.nT
        nTG = self.nTG
        nStrandsL = self.nStrandsL
        nS = self.nS
        nS = self.nS
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind

        rho_Cu = 1.6965e-8
        strand_diameter = LEDET.Inputs.ds_inGroup
        fraction_Cu = 1 - LEDET.Inputs.f_SC_strand_inGroup
        magnetic_length = LEDET.Inputs.l_mag_inGroup
        R_ght = rho_Cu / (np.pi * strand_diameter * strand_diameter / 4 * nStrandsL * fraction_Cu) * magnetic_length  # Resistance of each EACH HALF TURN in a specific group
        R_turns = np.repeat(R_ght[0:int(len(nT) / 2)] + R_ght[int(len(nT) / 2):len(nT)], nT[0:int(len(nT) / 2)])  # len(nT) is assumed to be even!
        R_groups = R_ght[:turnGroup_ind] * nTG

        #print('R_turns = ')
        #print(R_turns)
        #print('R_groups = ')
        #print(R_groups)

        return R_turns, R_groups

    def CapacitanceToGround(self):
        # This function calculates the capacitance to ground from each turn and group.
        # The capacitance is calculated under the assumption that the turns and groups can be approximated as parallel
        # plates. And hence the formula shown below can be used:
        # C = eps_0 * eps_r * A / d, where eps_0 is the vacuum permitivity, eps_r is the relative permitivity of the
        # insulation, A is the contact area, and d is the distance between plates.
        # Different types of insulation is dealt with by modelling each type of insulation as it own capacitor,
        # which are then placed in series.
        nameMagnet = self.nameMagnet
        LEDET = self.LEDET
        x = self.x
        y = self.y
        nT = self.nT
        nTG = self.nTG
        strandToHalfTurn = self.strandToHalfTurn
        strandToGroup = self.strandToGroup
        strandToTurnGroup = self.strandToTurnGroup
        HalfTurnToGroup = self.HalfTurnToGroup
        nStrandsL = self.nStrandsL
        nS = self.nS
        Ds = self.Ds
        polarities = self.polarities
        nHalfTurns = self.nHalfTurns
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind

        magnet_center = self.magnet_center
        epsR_LayerToBore = self.epsR_LayerToBore
        epsR_LayerToCollar = self.epsR_LayerToCollar
        epsR_BetweenLayers = self.epsR_BetweenLayers
        hIns_InnerLayerToBore = self.hIns_InnerLayerToBore
        hIns_OuterLayerToCollar = self.hIns_OuterLayerToCollar
        hIns_BetweenLayers = self.hIns_BetweenLayers
        LayerPattern_Quadrant = self.LayerPattern_Quadrant
        GeoArr = self.GeoArr

        flag_CapacitanceToBore = self.flag_CapacitanceToBore
        flag_CapacitanceToCollar = self.flag_CapacitanceToCollar
        # LEDET inputs

        # new GeoArr is recreated from shape and the assumption that [16, 12, 17, 5] is related to the number of half turns in each group
        # The above assumption is not correct in the case of layered groups! and hence the following code is not universal
        #OnesGeo = np.ones(len(nT), dtype=int)
        #GeoArr = np.concatenate((OnesGeo, nT))
        #GeoArr = np.reshape(GeoArr, (2, len(nT))).T

        l_mag_inGroup = LEDET.Inputs.l_mag_inGroup
        wBare_inGroup = LEDET.Inputs.wBare_inGroup
        hBare_inGroup = LEDET.Inputs.hBare_inGroup
        wIns_inGroup = LEDET.Inputs.wIns_inGroup
        hIns_inGroup = LEDET.Inputs.hIns_inGroup

        # Average half-turn positions
        x_ave = []
        y_ave = []
        for ht in range(1, nHalfTurns + 1):
            x_ave = np.hstack([x_ave, np.mean(x[np.where(strandToHalfTurn == ht)])])  # mean x-coord of the strands of each half turn
            y_ave = np.hstack([y_ave, np.mean(y[np.where(strandToHalfTurn == ht)])])  # mean y-coord of the strands of each half turn

        epsR_CabIns = self.epsRCabIns()
        # Capacitance between inner turns and bore
        eps0 = 1 / (4 * np.pi * 1E-7 * 299792458 ** 2)
        Turns_InnerBore = np.array([])
        Turns_OuterCollar = np.array([])
        ProximityCable = np.zeros((nHalfTurns, 1))
        LayerCount = 1
        GroupCount = 1
        for j in range(nHalfTurns):
            ProximityCable[j] = np.sqrt((magnet_center[0] / 1000 - x_ave[j]) ** 2 + (magnet_center[1] / 1000 - y_ave[j]) ** 2)
        CondCount = 0
        for i in range(len(GeoArr)):
            CabSnippet = ProximityCable[CondCount:CondCount + GeoArr[i][0] * GeoArr[i][1]]
            if LayerCount == len(LayerPattern_Quadrant):
                Turns_InnerBore = np.concatenate((Turns_InnerBore, CondCount + np.argsort(CabSnippet[:, 0])[:GeoArr[i][1]]))
            if LayerCount == 1:
                Turns_OuterCollar = np.concatenate((Turns_OuterCollar, CondCount + np.argsort(CabSnippet[:, 0])[GeoArr[i][0] * GeoArr[i][1] - GeoArr[i][1]:]))
            CondCount = CondCount + GeoArr[i][0] * GeoArr[i][1]
            GroupCount = GroupCount + 1
            if GroupCount > LayerPattern_Quadrant[LayerCount - 1]:
                GroupCount = 1
                LayerCount = LayerCount + 1
                if LayerCount > len(LayerPattern_Quadrant):
                    LayerCount = 1
        Turns_InnerBore = Turns_InnerBore.astype(int)
        Turns_OuterCollar = Turns_OuterCollar.astype(int)

        Capacity_Inner_Bore = []
        Capacity_Collar = []
        Contact_Area = (l_mag_inGroup * (hBare_inGroup + 2 * hIns_inGroup))
        if flag_CapacitanceToBore:
            for i in range(len(Turns_InnerBore)):
                i_Bore = HalfTurnToGroup[Turns_InnerBore[i]] - 1  # added to make the following equation more readable
                Capacity_Inner_Bore_Temp = 1 / (1 / (eps0 * epsR_CabIns[i_Bore] * (Contact_Area[i_Bore] / hIns_inGroup[i_Bore])) \
                                              + 1 / (eps0 * epsR_LayerToBore * (Contact_Area[i_Bore] / hIns_InnerLayerToBore)))
                Capacity_Inner_Bore = np.append(Capacity_Inner_Bore, Capacity_Inner_Bore_Temp)
        else:
            for i in range(len(Turns_InnerBore)):
                Capacity_Inner_Bore = np.append(Capacity_Inner_Bore, 0)

        if flag_CapacitanceToCollar:
            for i in range(len(Turns_OuterCollar)):
                i_Collar = HalfTurnToGroup[Turns_OuterCollar[i]] - 1
                Capacity_Collar_Temp = 1 / (1 / (eps0 * epsR_CabIns[i_Collar] * (Contact_Area[i_Collar] / hIns_inGroup[i_Collar])) \
                                          + 1 / (eps0 * epsR_LayerToCollar * (Contact_Area[i_Collar] / hIns_OuterLayerToCollar)))
                Capacity_Collar = np.append(Capacity_Collar, Capacity_Collar_Temp)
        else:
            for i in range(len(Turns_OuterCollar)):
                Capacity_Collar = np.append(Capacity_Collar, 0)

        print('Number of caps to inner bore')
        print(len(Capacity_Inner_Bore))
        print('Number of caps to collar')
        print(len(Capacity_Collar))
        # It is assumed that the capacitance Capacity_Inner_Bore[i] corresponds to the turn Turns_InnerBore[i]. The same assumption is made for Collar.
        Cap_index = np.concatenate((Turns_InnerBore, Turns_OuterCollar))
        Cap_combined = np.concatenate((Capacity_Inner_Bore, Capacity_Collar))  # Concatenated the same way as the index!
        # Caps sorted using Cap_index so that the first half-turn's cap is first in the array, and so on.
        C_HalfTurns = Cap_combined[Cap_index.argsort()]
        C_turns = C_HalfTurns[0:int(len(C_HalfTurns) / 2)] + C_HalfTurns[int(len(C_HalfTurns) / 2):len(C_HalfTurns)]
        C_groups = np.bincount(HalfTurnToGroup - 1, C_HalfTurns)
        C_groups = C_groups[:turnGroup_ind] + C_groups[turnGroup_ind:]  # turn-group correction

        return C_turns, C_groups

    def CapSum(self,Capacity_T2T,Contact_To,Contact_From):
        # Sums capacitances in parralel by checking if Contact_To and Contact_From match an already existen pair of nodes.
        # If the pair exist Capacity_T2T is added to the already existing value, if not the value and node pair are appended to their respective arrays.
        # The function automatically disregards any shorted capacitances. (Useful for summation of groups)
        Capacity_T2T_new = []
        Contact_From_new = []
        Contact_To_new = []
        for i in range(len(Capacity_T2T)):
            if Contact_To[i] != Contact_From[i]:
                if sum((Contact_To_new == Contact_To[i]) * (Contact_From_new == Contact_From[i])):  # check if current combination of contact to and from already exist
                    Capacity_T2T_new[(Contact_To_new == Contact_To[i]) * (Contact_From_new == Contact_From[i])] = \
                    Capacity_T2T_new[(Contact_To_new == Contact_To[i]) * (Contact_From_new == Contact_From[i])] + \
                    Capacity_T2T[i]
                else:
                    Capacity_T2T_new = np.append(Capacity_T2T_new, Capacity_T2T[i])
                    Contact_From_new = np.append(Contact_From_new, Contact_From[i])
                    Contact_To_new = np.append(Contact_To_new, Contact_To[i])

        Contact_From_new = np.int_(Contact_From_new)
        Contact_To_new = np.int_(Contact_To_new)

        return Capacity_T2T_new, Contact_From_new, Contact_To_new

    def CapacitanceT2T(self):
        # Calculates the capacitance between turns and between groups.
        # The calculation is done similairly to the capacitance to ground calculation and is based on heat exchange
        # information from the LEDET file.
        # The capacitance is found between each half-turn and is then summed, since the capacitors would be in parallel,
        # to create the value for each turn.
        # To create the group capacitance the same is done. However since there will be capacitance between turns inside
        # each group these capacitances are disregarded, since they are shorted in this model.
        nameMagnet = self.nameMagnet
        LEDET = self.LEDET
        x = self.x
        y = self.y
        nT = self.nT
        nTG = self.nTG
        strandToHalfTurn = self.strandToHalfTurn
        strandToGroup = self.strandToGroup
        strandToTurnGroup = self.strandToTurnGroup
        HalfTurnToGroup = self.HalfTurnToGroup
        nStrandsL = self.nStrandsL
        nS = self.nS
        Ds = self.Ds
        polarities = self.polarities
        nHalfTurns = self.nHalfTurns
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind
        HalfTurnToGroup = self.HalfTurnToGroup

        magnet_center = self.magnet_center
        epsR_LayerToBore = self.epsR_LayerToBore
        epsR_LayerToCollar = self.epsR_LayerToCollar
        epsR_BetweenLayers = self.epsR_BetweenLayers
        hIns_InnerLayerToBore = self.hIns_InnerLayerToBore
        hIns_OuterLayerToCollar = self.hIns_OuterLayerToCollar
        hIns_BetweenLayers = self.hIns_BetweenLayers
        LayerPattern_Quadrant = self.LayerPattern_Quadrant
        GeoArr = self.GeoArr

        flag_T2TCapWidth = self.flag_T2TCapWidth
        flag_T2TCapHeight = self.flag_T2TCapHeight

        l_mag_inGroup = LEDET.Inputs.l_mag_inGroup
        wBare_inGroup = LEDET.Inputs.wBare_inGroup
        hBare_inGroup = LEDET.Inputs.hBare_inGroup
        wIns_inGroup = LEDET.Inputs.wIns_inGroup
        hIns_inGroup = LEDET.Inputs.hIns_inGroup

        eps0 = 1 / (4 * np.pi * 1E-7 * 299792458 ** 2)
        epsR_CabIns = self.epsRCabIns()

        Capacity_T2T_Width = []
        Capacity_T2T_Height = []

        ContactW_From = np.int_(LEDET.Inputs.iContactAlongWidth_From)
        ContactW_To = np.int_(LEDET.Inputs.iContactAlongWidth_To)
        ContactH_From = np.int_(LEDET.Inputs.iContactAlongHeight_From)
        ContactH_To = np.int_(LEDET.Inputs.iContactAlongHeight_To)

        Contact_Area_Width = (l_mag_inGroup * (wBare_inGroup + 2 * wIns_inGroup))
        Contact_Area_Height = (l_mag_inGroup * (hBare_inGroup + 2 * hIns_inGroup))

        if flag_T2TCapWidth:
            for i in range(len(ContactW_From)):
                i_Width_From = HalfTurnToGroup[ContactW_From[i] - 1] - 1
                i_Width_To = HalfTurnToGroup[ContactW_To[i] - 1] - 1
                CA_From = Contact_Area_Width[i_Width_From]  # Contact area of the from cable
                CA_To = Contact_Area_Width[i_Width_To]  # Contact area of the to cable
                if CA_From < CA_To:  # find index of the minimum
                    i_Width = i_Width_From
                else:
                    i_Width = i_Width_To

                # is this correct, or should it be some average epsR_CabIns, and with a thickness of wIns_inGroup[i_Width_To] + wIns_inGroup[i_Width_From]
                Capacity_T2T_Width_Temp = 1 / (1 / (eps0 * epsR_CabIns[i_Width_To] * (Contact_Area_Width[i_Width] / (wIns_inGroup[i_Width_To]))) \
                                             + 1 / (eps0 * epsR_CabIns[i_Width_From] * (Contact_Area_Width[i_Width] / (wIns_inGroup[i_Width_From]))))
                Capacity_T2T_Width = np.append(Capacity_T2T_Width, Capacity_T2T_Width_Temp)
        else:
            for i in range(len(ContactW_From)):
                Capacity_T2T_Width = np.append(Capacity_T2T_Width, 0)

        if flag_T2TCapHeight:
            for i in range(len(ContactH_From)):
                i_Height_From = HalfTurnToGroup[ContactH_From[i] - 1] - 1
                i_Height_To = HalfTurnToGroup[ContactH_To[i] - 1] - 1
                CA_From = Contact_Area_Height[i_Height_From]  # Contact area of the from cable
                CA_To = Contact_Area_Height[i_Height_To]  # Contact area of the to cable
                if CA_From < CA_To:  # find index of the minimum contact area
                    i_Height = i_Height_From
                else:
                    i_Height = i_Height_To

                # is this correct, or should it be some average epsR_CabIns, and with a thickness of wIns_inGroup[i_Width_To] + wIns_inGroup[i_Width_From]
                Capacity_T2T_Height_Temp = 1 / (1 / (eps0 * epsR_CabIns[i_Height_To] * (Contact_Area_Height[i_Height] / (hIns_inGroup[i_Height_To]))) \
                                              + 1 / (eps0 * epsR_BetweenLayers * (Contact_Area_Height[i_Height] / (hIns_BetweenLayers))) \
                                              + 1 / (eps0 * epsR_CabIns[i_Height_From] * (Contact_Area_Width[i_Height] / (hIns_inGroup[i_Height_From]))))
                Capacity_T2T_Height = np.append(Capacity_T2T_Height, Capacity_T2T_Height_Temp)
        else:
            for i in range(len(ContactH_From)):
                Capacity_T2T_Height = np.append(Capacity_T2T_Height, 0)

        # Concatenate T2T capacitance, should be easier to write the netlist
        # first width then height!
        Capacity_T2T = np.concatenate((Capacity_T2T_Width, Capacity_T2T_Height))
        Contact_From = np.concatenate((ContactW_From, ContactH_From))
        Contact_To = np.concatenate((ContactW_To, ContactH_To))

        # change contact to and from to be for turns instead of half turns
        Contact_From_t0 = Contact_From
        Contact_To_t0 = Contact_To
        Contact_From_t0[Contact_From_t0 > nTurns] = Contact_From_t0[Contact_From_t0 > nTurns] - nTurns
        Contact_To_t0[Contact_To_t0 > nTurns] = Contact_To_t0[Contact_To_t0 > nTurns] - nTurns

        # change contact to and from to be for groups instead of half turn
        Contact_From_g0 = HalfTurnToGroup[Contact_From-1]
        Contact_To_g0 = HalfTurnToGroup[Contact_To-1]

        Capacity_T2T_turns, Contact_From_turns, Contact_To_turns = self.CapSum(Capacity_T2T, Contact_To_t0, Contact_From_t0)
        Capacity_T2T_groups, Contact_From_groups, Contact_To_groups = self.CapSum(Capacity_T2T, Contact_To_g0, Contact_From_g0)


        return Capacity_T2T_turns, Contact_From_turns, Contact_To_turns, Capacity_T2T_groups, Contact_From_groups, Contact_To_groups

    def netlist (self,L,R,C,k,Capacity_T2T_new,Contact_From_new,Contact_To_new):
        # Creates a netlist of all the calculated components as well as additional custom components and scaling
        # factors, which can be changed later in the generated netlist.
        # This function only creates one netlist, and hence should be run with different inputs for the turn and group
        # based models.
        # This function supports implementation of a custom parallel resistance and an eddy current loops.
        #
        # NOTE: This function creates the netlist according to the electrical order of turns specified in the LEDET file.
        #
        # Input arguments
        # L                 : The self inductances of the model
        # R                 : The resistance of the model
        # C                 : The capacitance to ground of the model
        # k                 : The coupling coefficients of the model
        # Capacity_T2T_new  : The capacitance between turns/groups in the model
        # Contact_From_new  : An array of nodes to which the capacitance should be added (between Contact_To_new and
        #                     Contact_From_new)
        # Contact_To_new    : An array of nodes to which the capacitance should be added (between Contact_To_new and
        #                     Contact_From_new)
        flag_writeFile = self.flag_writeFile
        flag_R_Par = self.flag_R_Par
        R_Par = self.R_Par
        flag_E_loops = self.flag_E_loops
        E_loops = self.E_loops
        F_SCALE_C_GROUND = self.F_SCALE_C_GROUND
        F_SCALE_C_T2T = self.F_SCALE_C_T2T
        F_SCALE_L = self.F_SCALE_L
        F_SCALE_R = self.F_SCALE_R
        pointsPerDecade = self.pointsPerDecade
        startFrequency = self.startFrequency
        stopFrequency = self.stopFrequency

        path_gateway = self.eospath + 'SWAN_projects/steam-notebooks/steam/*'

        # Launch a Gateway in a new Java process, this returns port
        port = launch_gateway(classpath=path_gateway)
        # JavaGateway instance is connected to a Gateway instance on the Java side
        gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
        # Get STEAM API Java classes
        MutualInductance = gateway.jvm.component.MutualInductance
        Netlist = gateway.jvm.netlist.Netlist
        CommentElement = gateway.jvm.netlist.elements.CommentElement
        GeneralElement = gateway.jvm.netlist.elements.GeneralElement
        GlobalParameterElement = gateway.jvm.netlist.elements.GlobalParameterElement
        ACSolverElement = gateway.jvm.netlist.solvers.ACSolverElement
        CircuitalPreconditionerSubcircuit = gateway.jvm.preconditioner.CircuitalPreconditionerSubcircuit
        TextFile = gateway.jvm.utils.TextFile
        CSVReader = gateway.jvm.utils.CSVReader

        # Electrical order:
        nameOrder = np.arange(1, self.nTurns + 1)
        if self.nTurns == len(L):
            nameOrder = self.EO_turns
        else:
            nameOrder = self.EO_groups


        netlist = Netlist("")

        globalParameters_Parameters = ['F_SCALE_C_GROUND', 'F_SCALE_C_T2T', 'F_SCALE_L', 'F_SCALE_R']
        globalParameters_Values = [str.format('{}', F_SCALE_C_GROUND), str.format('{}', F_SCALE_C_T2T),
                                   str.format('{}', F_SCALE_L), str.format('{}', F_SCALE_R)]

        E_param_param = []
        E_param_values = []

        if flag_E_loops:
            for i in range(len(E_loops)):
                E_param_param = E_param_param + [str.format('L_EDDY{}', i + 1), str.format('R_EDDY{}', i + 1),
                                                 str.format('K_EDDY{}', i + 1)]
                E_param_values = E_param_values + [str.format('{}', E_loops[i][0]), str.format('{}', E_loops[i][1]),
                                                   str.format('{}', E_loops[i][2])]

            globalParameters_Parameters = globalParameters_Parameters + E_param_param
            globalParameters_Values = globalParameters_Values + E_param_values

        if flag_R_Par:
            globalParameters_Parameters = globalParameters_Parameters + ['R_Par']
            globalParameters_Values = globalParameters_Values + [str.format('{}', R_Par)]

        globalParameters_Parameters = a.create_string_array(gateway, globalParameters_Parameters)
        globalParameters_Values = a.create_string_array(gateway, globalParameters_Values)

        netlist.add(CommentElement("**** Global parameters ****"))
        netlist.add(GlobalParameterElement(globalParameters_Parameters, globalParameters_Values))

        netlist.add(CommentElement("* .STEP PARAM R_Par 10k, 10k, 100k"))

        nodesL = gateway.new_array(gateway.jvm.String, len(L), 2)
        nodesR = gateway.new_array(gateway.jvm.String, len(R), 2)
        nodesC = gateway.new_array(gateway.jvm.String, len(C), 2)

        GROUND_NODE = "0"

        for i in range(len(L)):
            if i == 0:
                nodesL[i][0] = str.format("{}in", i + 1)
            else:
                nodesL[i][0] = str.format("{}out", i)

            # L - negative (right terminal) - imid, e.g., 1mid
            nodesL[i][1] = str.format("{}mid", i + 1);

            # R_par - positive (left terminal) - imid, e.g., 1mid
            nodesR[i][0] = str.format("{}mid", i + 1);

            # R_par - negative (right terminal) - iout, e.g., 1out
            nodesR[i][1] = str.format("{}out", i + 1);

            # C - positive (left terminal) - iout, e.g., 1out
            nodesC[i][0] = str.format("{}out", i + 1);

            # C - negative (right terminal)
            nodesC[i][1] = GROUND_NODE;

        namesL = gateway.new_array(gateway.jvm.String, len(L))
        namesR = gateway.new_array(gateway.jvm.String, len(R))
        namesC = gateway.new_array(gateway.jvm.String, len(C))

        nodes = gateway.new_array(gateway.jvm.String, 2)

        for i in range(len(L)):
            netlist.add(CommentElement(str.format("* Cell {}", i + 1)))

            # Add inductors
            namesL[i] = str.format("L_{}", nameOrder[i])
            nodes[0], nodes[1] = nodesL[i][1], nodesL[i][0]
            value = '{' + str(L[nameOrder[i]-1][nameOrder[i]-1]) + '*F_SCALE_L}'
            netlist.add(GeneralElement(namesL[i], nodes, value))

            # Add resistance in series with the inductor
            namesR[i] = str.format("R_{}", nameOrder[i])
            nodes[0], nodes[1] = nodesR[i][1], nodesR[i][0]
            value = '{' + str(R[nameOrder[i]-1]) + '*F_SCALE_R}'
            netlist.add(GeneralElement(namesR[i], nodes, value))

            # Add capacitance to ground
            if C[i]:
                namesC[i] = str.format("C_{}", nameOrder[i])
                nodes[0], nodes[1] = nodesC[i][1], nodesC[i][0]
                value = '{' + str(C[nameOrder[i]-1]) + '*F_SCALE_C_GROUND}'
                netlist.add(GeneralElement(namesC[i], nodes, value))


        nodesT2TC = gateway.new_array(gateway.jvm.String, len(Capacity_T2T_new), 2)

        #explain!
        reverseOrder=np.array([i for i, v in sorted(enumerate(nameOrder), key=lambda iv: iv[1])])+1

        for i in range(len(Capacity_T2T_new)):
            nodesT2TC[i][0] = str.format("{}out", reverseOrder[Contact_From_new[i]-1]);
            nodesT2TC[i][1] = str.format("{}out", reverseOrder[Contact_To_new[i]-1]);

        namesT2TC = gateway.new_array(gateway.jvm.String, len(Capacity_T2T_new))
        if self.nTurns == len(L):
            netlist.add(CommentElement("Turn to Turn Capacitance"))
        else:
            netlist.add(CommentElement("Group to Group Capacitance"))

        for i in range(len(Capacity_T2T_new)):
            namesT2TC[i] = str.format("C_T2T_{}_{}", Contact_From_new[i], Contact_To_new[i])
            nodes[0], nodes[1] = nodesT2TC[i][1], nodesT2TC[i][0]
            value = '{' + str(Capacity_T2T_new[i]) + '*F_SCALE_C_T2T}'
            netlist.add(GeneralElement(namesT2TC[i], nodes, value))

        netlist.add(CommentElement("Mutual coupling between cells"))
        # Add inductive coupling coefficients - upper diagonal
        for row in range(len(L)):
            for col in range(row + 1, len(L)):
                name = str.format("K_{}_{}", row + 1, col + 1)
                nodes[0], nodes[1] = str.format("L_{}", row + 1), str.format("L_{}", col + 1)
                value = str(k[row][col])
                netlist.add(GeneralElement(name, nodes, value))

        # Add parralel resistance
        if flag_R_Par:
            netlist.add(CommentElement("* Parallel resistance"));
            name = "R_Par";
            nodes[0], nodes[1] = nodesL[0][0], nodesR[len(L) - 1][1]
            value = '{R_Par}';
            netlist.add(GeneralElement(name, nodes, value));

        # Add eddy current loops
        if flag_E_loops:
            nodesR_E = gateway.new_array(gateway.jvm.String, 2)
            nodesL_E = gateway.new_array(gateway.jvm.String, 2)
            nodesG_E = gateway.new_array(gateway.jvm.String, 2)

            netlist.add(CommentElement("* Eddy current loops"));
            for i in range(len(E_loops)):
                netlist.add(CommentElement(str.format("* Loop {}", i + 1)));

                nameR = str.format('R_EDDY{}', i + 1)
                nameL = str.format('L_EDDY{}', i + 1)
                nameG = str.format('R_EDDY{}_GND', i + 1)

                nodesR_E[0], nodesR_E[1] = str.format('{}E_L', i + 1), str.format('{}E_R', i + 1)
                nodesL_E[0], nodesL_E[1] = str.format('{}E_R', i + 1), str.format('{}E_L', i + 1)
                nodesG_E[0], nodesG_E[1] = str.format('{}E_L', i + 1), '0'

                valueL = '{' + nameL + '}'
                valueR = '{' + nameR + '}'
                valueK = '{' + str.format('K_EDDY{}', i + 1) + '}'
                valueG = '1E12'

                netlist.add(GeneralElement(nameR, nodesR_E, valueR));
                netlist.add(GeneralElement(nameL, nodesL_E, valueL));
                netlist.add(GeneralElement(nameG, nodesG_E, valueG));

                netlist.add(CommentElement('* Coupling coefficients'));
                for j in range(len(L)):
                    name = str.format("K_E_{}_{}", i + 1, j + 1)
                    nodes[0], nodes[1] = nameL, str.format("L_{}", j + 1)
                    value = valueK
                    netlist.add(GeneralElement(name, nodes, value))

        # Voltage source
        netlist.add(CommentElement("* Voltage source"));
        name = "V_AC"
        nodes[0], nodes[1] = nodesL[0][0], nodesR[len(L) - 1][1]
        value = "AC 1"
        netlist.add(GeneralElement(name, nodes, value));

        # Add a resistor to ground for a bias point calculation
        netlist.add(CommentElement("* Resistance to ground"));
        name = "R_GND"
        nodes[0], nodes[1] = nodesR[len(L) - 1][1], GROUND_NODE
        value = "1e6"
        netlist.add(GeneralElement(name, nodes, value));

        netlist.setSolver(ACSolverElement.Builder()
                            .pointsPerDecade(pointsPerDecade)
                            .startFrequency(startFrequency)
                            .stopFrequency(stopFrequency)
                            .build())

        netlistAsListString = netlist.generateNetlistFile("BINARY")

        # Display time stamp
        currentDT = datetime.datetime.now()
        print(' ')
        print('Time stamp: ' + str(currentDT))

        if flag_writeFile:
            cwd = os.getcwd()
            if self.nTurns == len(L):
                Path(cwd + '/Turns').mkdir(parents=True, exist_ok=True)
                Circ = 'Turns/' + self.nameMagnet + '_turns.cir'
                print('Turn-based netlist file generated.')

            else:
                Path(cwd + '/Groups').mkdir(parents=True, exist_ok=True)
                Circ = 'Groups/' + self.nameMagnet + '_groups.cir'
                print('Group-based netlist file generated.')

            TextFile.writeMultiLine(Circ, netlistAsListString, False)
        else:
            print('Netlist generation done, file generation disabled.')

        return netlist, netlistAsListString