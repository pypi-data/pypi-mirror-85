import os
import numpy as np
import datetime
import xlrd
import xlsxwriter
from dataclasses import dataclass, asdict

from steam_nb_api.resources.ResourceReader import ResourceReader

@dataclass
class LEDETInputs:
    BlankRows: np.ndarray = np.array([[3,4,6,36,37,41,45,49,52,55,57,63,77,79],[3,4,6,36,37,41,45,49,52,55,57,63,77,79]])
    T00: float= 0.0
    l_magnet: float= 0.0
    I00: float= 0.0
    M_m: np.ndarray = np.array([])
    fL_I: np.ndarray = np.array([])
    fL_L: np.ndarray = np.array([])
    GroupToCoilSection: np.ndarray = np.array([])
    polarities_inGroup: np.ndarray = np.array([])
    nT: np.ndarray = np.array([])
    nStrands_inGroup: np.ndarray = np.array([])
    l_mag_inGroup: np.ndarray = np.array([])
    ds_inGroup: np.ndarray = np.array([])
    f_SC_strand_inGroup: np.ndarray = np.array([])
    f_ro_eff_inGroup: np.ndarray = np.array([])
    Lp_f_inGroup: np.ndarray = np.array([])
    RRR_Cu_inGroup: np.ndarray = np.array([])
    SCtype_inGroup: np.ndarray = np.array([])
    STtype_inGroup: np.ndarray = np.array([])
    insulationType_inGroup: np.ndarray = np.array([])
    internalVoidsType_inGroup: np.ndarray = np.array([])
    externalVoidsType_inGroup: np.ndarray = np.array([])
    wBare_inGroup: np.ndarray = np.array([])
    hBare_inGroup: np.ndarray = np.array([])
    wIns_inGroup: np.ndarray = np.array([])
    hIns_inGroup: np.ndarray = np.array([])
    Lp_s_inGroup: np.ndarray = np.array([])
    R_c_inGroup: np.ndarray = np.array([])
    Tc0_NbTi_ht_inGroup: np.ndarray = np.array([])
    Bc2_NbTi_ht_inGroup: np.ndarray = np.array([])
    c1_Ic_NbTi_inGroup: np.ndarray = np.array([])
    c2_Ic_NbTi_inGroup: np.ndarray = np.array([])
    Tc0_Nb3Sn_inGroup: np.ndarray = np.array([])
    Bc2_Nb3Sn_inGroup: np.ndarray = np.array([])
    Jc_Nb3Sn0_inGroup: np.ndarray = np.array([])
    overwrite_f_internalVoids_inGroup: np.ndarray = np.array([])
    overwrite_f_externalVoids_inGroup: np.ndarray = np.array([])
    el_order_half_turns: np.ndarray = np.array([])
    alphasDEG: np.ndarray = np.array([])
    rotation_block: np.ndarray = np.array([])
    mirror_block: np.ndarray = np.array([])
    mirrorY_block: np.ndarray = np.array([])
    iContactAlongWidth_From: np.ndarray = np.array([])
    iContactAlongWidth_To: np.ndarray = np.array([])
    iContactAlongHeight_From: np.ndarray = np.array([])
    iContactAlongHeight_To: np.ndarray = np.array([])
    iStartQuench: np.ndarray = np.array([])
    tStartQuench: np.ndarray = np.array([])
    lengthHotSpot_iStartQuench: np.ndarray = np.array([])
    vQ_iStartQuench: np.ndarray = np.array([])
    R_circuit: float= 0.0
    R_crowbar: float= 0.0
    Ud_crowbar: float= 0.0
    t_PC: float= 0.0
    t_PC_LUT: np.ndarray = np.array([])
    I_PC_LUT: np.ndarray = np.array([])
    tEE: float= 0.0
    R_EE_triggered: float= 0.0
    tCLIQ: np.ndarray = np.array([])
    directionCurrentCLIQ: np.ndarray = np.array([])
    nCLIQ: np.ndarray = np.array([])
    U0: np.ndarray = np.array([])
    C: np.ndarray = np.array([])
    Rcapa: np.ndarray = np.array([])
    tQH: np.ndarray = np.array([])
    U0_QH: np.ndarray = np.array([])
    C_QH: np.ndarray = np.array([])
    R_warm_QH: np.ndarray = np.array([])
    w_QH: np.ndarray = np.array([])
    h_QH: np.ndarray = np.array([])
    s_ins_QH: np.ndarray = np.array([])
    type_ins_QH: np.ndarray = np.array([])
    s_ins_QH_He: np.ndarray = np.array([])
    type_ins_QH_He: np.ndarray = np.array([])
    l_QH: np.ndarray = np.array([])
    f_QH: np.ndarray = np.array([])
    iQH_toHalfTurn_From: np.ndarray = np.array([])
    iQH_toHalfTurn_To: np.ndarray = np.array([])
    tQuench: np.ndarray = np.array([])
    initialQuenchTemp: np.ndarray = np.array([])
    HalfTurnToInductanceBlock: np.ndarray = np.array([])
    M_InductanceBlock_m: np.ndarray= np.array([])
@dataclass
class LEDETOptions:
    BlankRows: np.ndarray= np.array([[],[]])
    time_vector_params: np.ndarray = np.array([])
    Iref: float = 0.0
    flagIron: float = 0.0
    flagSelfField: float = 0.0
    headerLines: float = 0.0
    columnsXY: np.ndarray = np.array([])
    columnsBxBy: np.ndarray = np.array([])
    flagPlotMTF: float = 0.0
    flag_calculateInductanceMatrix: float = 0.0
    flag_useExternalInitialization: float = 0.0
    flag_initializeVar: float = 0.0
    flag_fastMode: float = 0.0
    flag_controlCurrent: float = 0.0
    flag_automaticRefinedTimeStepping: float = 0.0
    flag_IronSaturation: float = 0.0
    flag_InvertCurrentsAndFields: float = 0.0
    flag_ScaleDownSuperposedMagneticField: float = 0.0
    flag_HeCooling: float = 0.0
    fScaling_Pex: float = 0.0
    fScaling_Pex_AlongHeight: float = 0.0
    fScaling_MR: float = 0.0
    flag_scaleCoilResistance_StrandTwistPitch: float = 0.0
    flag_separateInsulationHeatCapacity: float = 0.0
    flag_ISCL: float = 0.0
    fScaling_Mif: float = 0.0
    fScaling_Mis: float = 0.0
    flag_StopIFCCsAfterQuench: float = 0.0
    flag_StopISCCsAfterQuench: float = 0.0
    tau_increaseRif: float = 0.0
    tau_increaseRis: float = 0.0
    fScaling_RhoSS: float = 0.0
    maxVoltagePC: float = 0.0
    flag_symmetricGroundingEE: float = 0.0
    flag_removeUc: float = 0.0
    BtX_background: float = 0.0
    BtY_background: float = 0.0
    flag_showFigures: float = 0.0
    flag_saveFigures: float = 0.0
    flag_saveMatFile: float = 0.0
    flag_saveTxtFiles: float = 0.0
    flag_generateReport: float = 0.0
    flag_hotSpotTemperatureInEachGroup: float = 0.0
    MinMaxXY_MTF: np.ndarray = np.array([])
@dataclass
class LEDETPlots:
    BlankRows: np.ndarray = np.array([[],[]])
    suffixPlot: str = ''
    typePlot: int = 0
    outputPlotSubfolderPlot: str = ''
    variableToPlotPlot: np.ndarray = np.array([])
    selectedStrandsPlot: np.ndarray = np.array([])
    selectedTimesPlot: np.ndarray = np.array([])
    labelColorBarPlot: np.ndarray = np.array([])
    minColorBarPlot: float = 0.0
    maxColorBarPlot: float = 0.0
    MinMaxXYPlot: np.ndarray = np.array([])
    flagSavePlot: int = 0
    flagColorPlot: int = 0
    flagInvisiblePlot: int = 0
@dataclass
class LEDETVariables:
    BlankRows: np.ndarray = np.array([[],[]])
    variableToSaveTxt: np.ndarray = np.array([])
    typeVariableToSaveTxt: np.ndarray = np.array([])
    variableToInitialize: np.ndarray = np.array([])

class ParametersLEDET:
    '''
        Class of LEDET parameters
    '''
    def setAttribute(self, LEDETclass, attribute, value):
        try:
            setattr(LEDETclass, attribute, value)
        except:
            setattr(getattr(self, LEDETclass), attribute, value)

    def getAttribute(self, LEDETclass, attribute):
        try:
            return getattr(LEDETclass, attribute)
        except:
            return getattr(getattr(self, LEDETclass), attribute)

    def updateBlankrows(self,LEDETclass):
        attributeCounter = 1
        lineAdd = np.zeros(LEDETclass.BlankRows[1].shape)
        if lineAdd.size == 0:
            return

        lengthAdd = 1
        currentStatus = 0
        for attribute in LEDETclass.__annotations__:
            if attribute == 'BlankRows':
                continue
            downLength = 1
            if(type(self.getAttribute(LEDETclass,attribute))==np.ndarray):
                if self.getAttribute(LEDETclass, attribute).ndim > 1:
                    downLength = self.getAttribute(LEDETclass, attribute).shape[0]
            lengthAdd = lengthAdd + downLength
            if attributeCounter in LEDETclass.BlankRows[0]:
                lineAdd[currentStatus:] = lineAdd[currentStatus:]+lengthAdd
                lengthAdd = 1
                currentStatus = currentStatus +1

            attributeCounter = attributeCounter + 1
        LEDETclass.BlankRows[1] = lineAdd-1

    def readLEDETExcel(self, file):
        ##File must be whole eos string
        workbookVariables = xlrd.open_workbook(file)

        #Inputs
        worksheetInputs = workbookVariables.sheet_by_name('Inputs')
        lastAttribute = worksheetInputs.cell(0, 1).value
        for i in range(worksheetInputs.nrows):
            self.variablesInputs[str(worksheetInputs.cell(i, 1).value)] = str(worksheetInputs.cell(i, 0).value)
            attribute = worksheetInputs.cell(i, 1).value
            if (attribute == ''):
                if (type(worksheetInputs.cell(i, 2).value) != str):
                    values = worksheetInputs.row_values(i, 2)
                    values = np.array([k for k in values if(str(k))])
                    current = self.getAttribute(self.Inputs, lastAttribute)
                    current = np.vstack((current, values))
                    self.setAttribute(self.Inputs, lastAttribute, current)
                else:
                    continue
            elif (type(self.getAttribute(self.Inputs, attribute)) == np.ndarray):
                lastAttribute = attribute
                values = worksheetInputs.row_values(i, 2)
                values = np.array([k for k in values if(str(k))])
                self.setAttribute(self.Inputs, attribute, values)
            else:
                value = worksheetInputs.cell(i, 2).value
                self.setAttribute(self.Inputs, attribute, value)
        #Options
        worksheetOptions = workbookVariables.sheet_by_name('Options')
        for i in range(worksheetOptions.nrows):
            self.variablesOptions[str(worksheetOptions.cell(i, 1).value)] = str(worksheetOptions.cell(i, 0).value)
            attribute = worksheetOptions.cell(i, 1).value
            if (type(self.getAttribute(self.Options, attribute)) == np.ndarray):
                values = worksheetOptions.row_values(i, 2)
                values = np.array([k for k in values if(str(k))])
                self.setAttribute(self.Options, attribute, values)
            else:
                value = worksheetOptions.cell(i, 2).value
                self.setAttribute(self.Options, attribute, value)
        #Plots
        worksheetPlots = workbookVariables.sheet_by_name('Plots')
        for i in range(worksheetPlots.nrows):
            self.variablesPlots[str(worksheetPlots.cell(i, 1).value)] = str(worksheetPlots.cell(i, 0).value)
            attribute = worksheetPlots.cell(i, 1).value
            if (type(self.getAttribute(self.Plots, attribute)) == np.ndarray):
                values = worksheetPlots.row_values(i, 2)
                values = np.array([k for k in values if(str(k))])
                self.setAttribute(self.Plots, attribute, values)
            else:
                try:
                    value = worksheetPlots.cell(i, 2).value
                except:
                    value = ''
                self.setAttribute(self.Plots, attribute, value)
        # Variables
        worksheetVariables = workbookVariables.sheet_by_name('Variables')
        for i in range(worksheetVariables.nrows):
            self.variablesVariables[str(worksheetVariables.cell(i, 1).value)] = str(worksheetVariables.cell(i, 0).value)
            attribute = worksheetVariables.cell(i, 1).value
            if (type(self.getAttribute(self.Variables, attribute)) == np.ndarray):
                values = worksheetVariables.row_values(i, 2)
                values = np.array([k for k in values if(str(k))])
                self.setAttribute(self.Variables, attribute, values)
            else:
                value = worksheetVariables.cell(i, 2).value
                self.setAttribute(self.Variables, attribute, value)

    def __init__(self):
        self.Inputs = LEDETInputs()
        self.Options = LEDETOptions()
        self.Plots = LEDETPlots()
        self.Variables = LEDETVariables()
        self.variablesInputs = {}
        self.variablesOptions = {}
        self.variablesPlots = {}
        self.variablesVariables = {}

        self.variableGroupInputs = asdict(self.Inputs)
        self.variableGroupOptions = asdict(self.Options)
        self.variableGroupPlots = asdict(self.Plots)
        self.variableGroupVariables = asdict(self.Variables)

        # Load and set the default LEDET parameters
        self.fileDefaultParameters = os.path.join('ledet', 'variableNamesDescriptions.xlsx')
        self.loadDefaultParameters(self.fileDefaultParameters)


    def setParameters(self, variablesInputs, variablesOptions, variablesPlots , variablesVariables):
        for k in variablesInputs.keys():
            self.setAttribute(LEDETInputs, k, variablesInputs[k])
        for k in variablesOptions.keys():
            self.setAttribute(LEDETInputs, k, variablesOptions[k])
        for k in variablesPlots.keys():
            self.setAttribute(LEDETInputs, k, variablesPlots[k])
        for k in variablesVariables.keys():
            self.setAttribute(LEDETInputs, k, variablesVariables[k])

        self.variablesInputs, self.variablesOptions, self.variablesPlots, self.variablesVariables = variablesInputs, variablesOptions, variablesPlots, variablesVariables

    def loadDefaultParameters(self, fileDefaultParameters: str):
        '''
            **Loads and sets the default LEDET parameters **

            Function to load and set the default LEDET parameters

            :param fileName: String defining the name of the file defining the default LEDET parameters
            :type fileName: str

            :return: None
        '''

        # Load default LEDET parameters
        # Read variable names and descriptions
        fullfileName = ResourceReader.getResourcePath(fileDefaultParameters)
        # print(fullfileName) # for debug
        workbookVariables = xlrd.open_workbook(fullfileName)

        # Load "Inputs" sheet
        worksheetInputs = workbookVariables.sheet_by_name('Inputs')
        variablesInputs = {}
        for i in range(worksheetInputs.nrows):
            variablesInputs[str(worksheetInputs.cell(i, 1).value)] = str(worksheetInputs.cell(i, 0).value)

        # Load "Options" sheet
        worksheetOptions = workbookVariables.sheet_by_name('Options')
        variablesOptions = {}
        for i in range(worksheetOptions.nrows):
            variablesOptions[str(worksheetOptions.cell(i, 1).value)] = str(worksheetOptions.cell(i, 0).value)

        # Load "Plots" sheet
        worksheetPlots = workbookVariables.sheet_by_name('Plots')
        variablesPlots = {}
        for i in range(worksheetPlots.nrows):
            variablesPlots[str(worksheetPlots.cell(i, 1).value)] = str(worksheetPlots.cell(i, 0).value)

        # Load "Variables" sheet
        worksheetVariables = workbookVariables.sheet_by_name('Variables')
        variablesVariables = {}
        for i in range(worksheetVariables.nrows):
            variablesVariables[str(worksheetVariables.cell(i, 1).value)] = str(worksheetVariables.cell(i, 0).value)

        # Set parameters
        self.setParameters(variablesInputs, variablesOptions, variablesPlots, variablesVariables)

    def addVariablesInputs(self,
                           T00, l_magnet, I00, M_m,
                           fL_I, fL_L,
                           GroupToCoilSection, polarities_inGroup, nT, nStrands_inGroup, l_mag_inGroup, ds_inGroup,
                           f_SC_strand_inGroup, f_ro_eff_inGroup, Lp_f_inGroup, RRR_Cu_inGroup,
                           SCtype_inGroup, STtype_inGroup, insulationType_inGroup, internalVoidsType_inGroup,
                           externalVoidsType_inGroup,
                           wBare_inGroup, hBare_inGroup, wIns_inGroup, hIns_inGroup, Lp_s_inGroup, R_c_inGroup,
                           Tc0_NbTi_ht_inGroup, Bc2_NbTi_ht_inGroup, c1_Ic_NbTi_inGroup, c2_Ic_NbTi_inGroup,
                           Tc0_Nb3Sn_inGroup, Bc2_Nb3Sn_inGroup, Jc_Nb3Sn0_inGroup,
                           el_order_half_turns,
                           alphasDEG, rotation_block, mirror_block, mirrorY_block,
                           iContactAlongWidth_From, iContactAlongWidth_To, iContactAlongHeight_From,
                           iContactAlongHeight_To,
                           iStartQuench, tStartQuench, lengthHotSpot_iStartQuench, vQ_iStartQuench,
                           R_circuit, R_crowbar, Ud_crowbar, t_PC, t_PC_LUT, I_PC_LUT,
                           tEE, R_EE_triggered,
                           tCLIQ, directionCurrentCLIQ, nCLIQ, U0, C, Rcapa,
                           tQH, U0_QH, C_QH, R_warm_QH, w_QH, h_QH, s_ins_QH, type_ins_QH, s_ins_QH_He, type_ins_QH_He, l_QH, f_QH,
                           iQH_toHalfTurn_From, iQH_toHalfTurn_To,
                           tQuench, initialQuenchTemp,
                           HalfTurnToInductanceBlock, M_InductanceBlock_m
                           ):
        '''
            **Adds all LEDET parameters to be written in the "Inputs" sheet **

            Function to add "Inputs" LEDET parameters

            :param T00: String defining the name of the file defining the default LEDET parameters
            :type T00: float

            :return: None
        '''
        ins = locals()
        for attribute in ins:
            self.setAttribute(self.Inputs, attribute, ins[attribute])

    def addVariablesOptions(self,
                            time_vector_params,
                            Iref, flagIron, flagSelfField, headerLines, columnsXY, columnsBxBy, flagPlotMTF,
                            flag_calculateInductanceMatrix, flag_useExternalInitialization, flag_initializeVar,
                            flag_fastMode, flag_controlCurrent, flag_automaticRefinedTimeStepping, flag_IronSaturation,
                            flag_InvertCurrentsAndFields, flag_ScaleDownSuperposedMagneticField, flag_HeCooling,
                            fScaling_Pex, fScaling_Pex_AlongHeight,
                            fScaling_MR, flag_scaleCoilResistance_StrandTwistPitch, flag_separateInsulationHeatCapacity,
                            flag_ISCL, fScaling_Mif, fScaling_Mis, flag_StopIFCCsAfterQuench, flag_StopISCCsAfterQuench,
                            tau_increaseRif, tau_increaseRis,
                            fScaling_RhoSS, maxVoltagePC, flag_symmetricGroundingEE, flag_removeUc, BtX_background,
                            BtY_background,
                            flag_showFigures, flag_saveFigures, flag_saveMatFile, flag_saveTxtFiles,
                            flag_generateReport,
                            flag_hotSpotTemperatureInEachGroup, MinMaxXY_MTF
                           ):
        '''
            **Adds all LEDET parameters to be written in the "Options" sheet **

            Function to add "Options" LEDET parameters

            :param T00: String defining the name of the file defining the default LEDET parameters
            :type T00: float

            :return: None
        '''
        ins = locals()
        for attribute in ins:
            self.setAttribute(self.Options, attribute, ins[attribute])

    def addVariablesPlots(self,
                          suffixPlot, typePlot, outputPlotSubfolderPlot, variableToPlotPlot, selectedStrandsPlot,
                          selectedTimesPlot,
                          labelColorBarPlot, minColorBarPlot, maxColorBarPlot, MinMaxXYPlot, flagSavePlot,
                          flagColorPlot, flagInvisiblePlot
                           ):
        '''
            **Adds all LEDET parameters to be written in the "Plots" sheet **

            Function to add "Plots" LEDET parameters

            :param T00: String defining the name of the file defining the default LEDET parameters
            :type T00: float

            :return: None
        '''
        ins = locals()
        for attribute in ins:
            self.setAttribute(self.Plots, attribute, ins[attribute])

    def addVariablesVariables(self,
                              variableToSaveTxt, typeVariableToSaveTxt, variableToInitialize
                              ):
        '''
            **Adds all LEDET parameters to be written in the "Variables" sheet **

            Function to add "Variables" LEDET parameters

            :param T00: String defining the name of the file defining the default LEDET parameters
            :type T00: float

            :return: None
        '''
        ins = locals()
        for attribute in ins:
            self.setAttribute(self.Variables, attribute, ins[attribute])


    def printVariableDescNameValue(self, variableGroup, variableLabels):
        """

           **Print variable description, variable name, and variable value**

           Function prints variable description, variable name, and variable value

           :param variableGroup: list of tuples; each tuple has two elements: the first element is a string defining
           the variable name, and the second element is either an integer, a float, a list, or a numpy.ndarray
           defining the variable value :type variableGroup: list :param variableLabels: dictionary assigning a
           description to each variable name
           :type variableLabels: dict

           :return: None

           - Example :

           import numpy as np

            variableGroup = []
            variableGroup.append( ('x1', 12) )
            variableGroup.append( ('x2', 23.42) )
            variableGroup.append( ('x3', [2, 4, 6]) )
            variableGroup.append( ('x3', np.array([2, 4, 6])) )

            variableLabels = {'x1': '1st variable', 'x2': '2nd variable', 'x3': '3rd variable'}

            utils.printVariableDescNameValue(variableGroup, variableLabels)
            # >>> 					1st variable x1 12
            # >>> 					2nd variable x2 23.42
            # >>> 					3rd variable x3 [2, 4, 6]
            # >>> 					3rd variable x3 [2 4 6]

        """
        if(type(variableGroup) != dict):
            for k in variableGroup.__annotations__:
                print(k, self.getAttribute(variableGroup, k))
        else:
            for k in variableGroup:
                print(k, variableGroup[k])

    def getNumberOfCoilSections(self):
        k = self.Inputs.M_m
        if k.shape == (1,): return k.shape[0]
        try:
            if k.shape[0] != k.shape[1]: print("M_m is not square")
        except:
            print("M_m is not square")
            return -1
        return k.shape[0]

    def checkM_InductanceBlock_m(self, Turns):
        if type(self.Inputs.M_InductanceBlock_m) != np.ndarray:
            k = np.array(self.Inputs.M_InductanceBlock_m)
        else:
            k = self.Inputs.M_InductanceBlock_m
        if k.shape == (1,):
            return False
        try:
            if k.shape[0] == k.shape[1]:
                if k.shape[0] == Turns:
                    return False
        except:
            print("M_InductanceBlock_m is not correct!")
            return True
        print("M_InductanceBlock_m is not correct!")
        return True

    def checkHeFraction(self, Groups):
        k = self.Inputs.overwrite_f_externalVoids_inGroup
        k2 = self.Inputs.overwrite_f_internalVoids_inGroup
        if len(k) > 0:
            if len(k) != len(k2):
                print("Helium section was set but is corrupted.")
                return False
            if len(k) != Groups:
                print("Helium section was set but is wrong length.")
                return False
        elif len(k2) > 0:
            print("Helium section was set but is corrupted.")
            return False
        return True

    def checkMonotony(self, arr, Invert=False):
        if Invert:
            arr = np.flip(arr)
        b = all(x <= y for x, y in zip(arr, arr[1:]))
        return b

    def checkTimes(self):
        t1 = min(self.Inputs.tQuench)
        t2 = self.Inputs.t_PC_LUT[0]
        t3 = min(self.Inputs.tStartQuench)
        t4 = self.Options.time_vector_params[0]

        if any(x < t4 for x in [t1,t2,t3]):
            print("You're using a time, that is before the start of the simulation. Please check!")
            return 0
        else:
            return 1

    def consistencyCheckLEDET(self):
        ## Consistency check of Inputs
        ## 0 Single - 1 CoilSections - 2 Groups - 3 Half-Turns - 4 doesn't matter - 5 iContactAlongWidth - 6 iContactAlongHeight - 7 vQlength
        ## 8 Quench Heater, 9 QuenchToFrom, 10 CLIQ,
        slicesSameInput = [[0,1,2,49,50,51,52,55,56],
                           [3,58,77,78],
                           [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33],
                           [36,37,38,39,40,79],
                           [4,5,34,35,53,54],
                           [41,42],
                           [43,44],
                           [45,46,47,48],
                           [63,64,65,66,67,68,69,70,71,72,73,74],
                           [75,76],
                           [57,59,60,61,62]]
        lengthInputs = len(self.Inputs.__annotations__)
        sizeInputs = np.zeros((lengthInputs,1))
        sizeInputs[slicesSameInput[0]] = 1
        sizeInputs[slicesSameInput[1]] = self.getNumberOfCoilSections()
        if sizeInputs[slicesSameInput[1][0]] == -1:
            print("M_m is corrupted. please check.")
            return True
        sizeInputs[slicesSameInput[2]] = len(self.Inputs.nT)
        sizeInputs[slicesSameInput[3]] = sum(self.Inputs.nT)
        sizeInputs[slicesSameInput[4]] = 0
        sizeInputs[slicesSameInput[5]] = len(self.Inputs.iContactAlongWidth_From)
        sizeInputs[slicesSameInput[6]] = len(self.Inputs.iContactAlongHeight_From)
        sizeInputs[slicesSameInput[7]] = len(self.Inputs.iStartQuench)
        sizeInputs[slicesSameInput[8]] = len(self.Inputs.tQH)
        sizeInputs[slicesSameInput[9]] = len(self.Inputs.iQH_toHalfTurn_From)
        try:
            sizeInputs[slicesSameInput[10]] = len(self.Inputs.tCLIQ)
        except:
            sizeInputs[slicesSameInput[10]] = 1

        if self.checkM_InductanceBlock_m(int(sum(self.Inputs.nT)/2)):
            return 1

        Count = 0
        Break = 0
        for k in self.Inputs.__annotations__:
            if k== "BlankRows": continue
            if sizeInputs[Count] == 0:
                Count = Count + 1
                continue
            cC = self.getAttribute(self.Inputs, k)
            if type(cC) == np.ndarray or type(cC) == list:
                if not len(cC)==sizeInputs[Count]:
                    print("The variable ",k, " does not have the correct size, should be", sizeInputs[Count]," but is ",len(cC),"! Please check.")
                    Break = 1
            elif type(cC) == float or type(cC) == int or type(cC) == np.float64:
                if not sizeInputs[Count]==1:
                    print("The variable ", k, " does not have the correct size, should be", sizeInputs[Count]," but is ",len(cC)," Please check.")
                    Break = 1
            else:
                print("Variable ", k, " has the wrong data-type set! Please check.")
                Break = 1
            Count = Count + 1
        if not self.checkHeFraction(len(self.Inputs.nT)): Break = 1
        if not self.checkMonotony(self.Inputs.t_PC_LUT):
            print("t_PC_LUT is not monotonic")
            Break = 1
        # if not self.checkMonotony(self.Inputs.fL_L, Invert=True):
        #     print("fL_L is not monotonic")
        #     Break = 1
        if not self.checkMonotony(self.Inputs.fL_I):
            print("fL_I is not monotonic")
            Break = 1
        if not self.checkTimes():
            Break = 1

        return Break

    def writeFileLEDET(self, nameFileLEDET, verbose: bool = False, SkipConsistencyCheck: bool = False):
        '''
            **Writes LEDET input file **

            Function to write a LEDET input file composed of "Inputs", "Options", "Plots", and "Variables" sheets

            :param nameFileLEDET: String defining the name of the LEDET input file to be written
            :type nameFileLEDET: string
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: None
        '''
        if not SkipConsistencyCheck:
            if self.consistencyCheckLEDET():
                print("Variables are not consistent! Writing aborted.")
                return
            else:
                print("Preliminary consistency check was successful!")

        workbook = xlsxwriter.Workbook(nameFileLEDET)

        if verbose:
            print('### Write "Inputs" sheet ###')
        self.writeLEDETInputsNew(workbook, "Inputs", self.Inputs, self.variablesInputs, verbose)

        if verbose:
            print('')
            print('### Write "Options" sheet ###')
        self.writeLEDETInputsNew(workbook, "Options", self.Options, self.variablesOptions, verbose)

        if verbose:
            print('')
            print('### Write "Plots" sheet ###')
        self.writeLEDETInputsNew(workbook, "Plots", self.Plots, self.variablesPlots, verbose)

        if verbose:
            print('')
            print('### Write "Variables" sheet ###')
        self.writeLEDETInputsNew(workbook, "Variables", self.Variables, self.variablesVariables, verbose)

        # Save the workbook
        workbook.close()

        # Display time stamp and end run
        currentDT = datetime.datetime.now()
        if verbose:
            print(' ')
            print('Time stamp: ' + str(currentDT))
            print('New file ' + nameFileLEDET + ' generated.')

        return

    def writeLEDETInputsNew(self, book, sheet, variableGroup, variableLabels, verbose: bool = False):
        """
            **Write one sheet of a LEDET input file**

            Function writes one sheet of a LEDET input file

            :param book: workbook object to write
            :type book: xlsxwriter.Workbook
            :param sheet: name of the sheet to write (first sheet = 0)
            :type sheet: string
            :param variableGroup: list of tuples; each tuple has two elements: the first element is a string defining the variable name, and the second element is either an integer, a float, a list, or a numpy.ndarray defining the variable value
            :param variableLabels: dictionary assigning a description to each variable name
            :type variableLabels: dict
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool
            :return:
        """
        worksheet = book.add_worksheet(sheet)
        cell_format = book.add_format({'bold': False, 'font_name': 'Calibri', 'font_size': 11})

        # Write to the sheet of the workbook
        currentRow = 0
        self.updateBlankrows(variableGroup)
        for attribute in variableGroup.__annotations__:
            if (attribute == "BlankRows"):
                continue
            if (attribute == "overwrite_f_internalVoids_inGroup"):
                ofiVg = self.getAttribute(variableGroup, attribute)
                if len(ofiVg) == 0:
                    currentRow = currentRow + 1
                    continue
            if (attribute == "overwrite_f_externalVoids_inGroup"):
                ofiVg = self.getAttribute(variableGroup, attribute)
                if len(ofiVg) == 0:
                    currentRow = currentRow + 1
                    continue
            if currentRow in variableGroup.BlankRows[1]:
                currentRow = currentRow + 1
            varDesc = variableLabels.get(str(attribute))
            worksheet.write(currentRow, 0, varDesc, cell_format)
            worksheet.write(currentRow, 1, attribute, cell_format)
            varType = type(self.getAttribute(variableGroup, attribute))
            if varType == np.ndarray:
                if self.getAttribute(variableGroup, attribute).ndim > 1:
                    for i in range(self.getAttribute(variableGroup, attribute).shape[1]):
                        worksheet.write_row(currentRow, 2, self.getAttribute(variableGroup, attribute)[i, :], cell_format)
                        currentRow = currentRow + 1
                else:
                    worksheet.write_row(currentRow, 2, self.getAttribute(variableGroup, attribute), cell_format)
                    currentRow = currentRow + 1
            elif varType == list:
                worksheet.write_row(currentRow, 2, self.getAttribute(variableGroup, attribute), cell_format)
                currentRow = currentRow + 1
            else:
                worksheet.write(currentRow, 2, self.getAttribute(variableGroup, attribute), cell_format)
                currentRow = currentRow + 1
            worksheet.set_column(0, 0, 80)
            worksheet.set_column(1, 1, 40)
            worksheet.set_column(2, 1000, 20)