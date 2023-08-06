''' UI for calibration interval calculations '''

from PyQt5 import QtWidgets, QtCore
import matplotlib.dates as mdates
import numpy as np

from . import gui_common
from . import gui_widgets
from . import page_dataimport
from ..intervals import variables, attributes


def get_colidx(hdr, name):
    ''' Get index of column or None if not in list '''
    try:
        return hdr.index(name)
    except ValueError:
        return None


def getNewIntervalCalc():
    ''' Prompt user with questions, return an instance of Interval '''
    dlg = NewIntDialog()
    dlg.exec()
    if dlg.optA3.isChecked():
        if dlg.optAssets.isChecked():
            item = attributes.TestIntervalAssets()
        else:
            item = attributes.TestInterval()
    elif dlg.optS2.isChecked():
        if dlg.optAssets.isChecked():
            item = attributes.BinomialIntervalAssets()
        else:
            item = attributes.BinomialInterval()
    else:
        if dlg.optAssets.isChecked():
            item = variables.VariablesIntervalAssets()
        else:
            item = variables.VariablesInterval()
    return item


class NewIntDialog(QtWidgets.QDialog):
    ''' Dialog for choosing type of interval calculation '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Interval Calculation Setup')
        self.optA3 = QtWidgets.QRadioButton('Attributes (pass/fail only) data, all intervals similar (Method A3)')
        self.optS2 = QtWidgets.QRadioButton('Attributes (pass/fail only) data, many different intervals (Method S2)')
        self.optVar = QtWidgets.QRadioButton('Variables (as-found and/or as-left) data (Variables Method)')
        self.optAssets = QtWidgets.QRadioButton('Results from Individual Calibrations')
        self.optSummary = QtWidgets.QRadioButton('Summarized Reliability Values')
        self.btnok = QtWidgets.QPushButton('Ok')
        self.optA3.setChecked(True)
        self.optAssets.setChecked(True)

        lay1 = QtWidgets.QVBoxLayout()
        lay1.addWidget(self.optA3)
        lay1.addWidget(self.optS2)
        lay1.addWidget(self.optVar)
        lay1.addStretch()
        lay2 = QtWidgets.QVBoxLayout()
        lay2.addWidget(self.optAssets)
        lay2.addWidget(self.optSummary)
        lay2.addStretch()
        self.frame1 = QtWidgets.QFrame()
        self.frame1.setLayout(lay1)
        self.frame2 = QtWidgets.QFrame()
        self.frame2.setLayout(lay2)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel('Select type of historical data for analysis:'))
        layout.addWidget(self.frame1)
        layout.addWidget(QtWidgets.QLabel('Enter data as:'))
        layout.addWidget(self.frame2)
        layout.addStretch()
        layout.addWidget(self.btnok)
        self.setLayout(layout)
        self.btnok.clicked.connect(self.accept)


class A3Params(QtWidgets.QGroupBox):
    ''' Widget for entering parameters for method A3 '''
    changed = QtCore.pyqtSignal()

    def __init__(self, showtol=False, parent=None):
        super().__init__('Test Interval Method (A3) Options', parent=parent)
        self.showtol = showtol
        self.I0 = gui_widgets.IntLineEdit(low=1)
        self.Rt = gui_widgets.FloatLineEdit(low=0.001, high=99.999)
        self.maxchange = gui_widgets.IntLineEdit(low=1, high=999)
        self.mindelta = gui_widgets.IntLineEdit(low=1)
        self.minintv = gui_widgets.IntLineEdit(low=1)
        self.maxintv = gui_widgets.IntLineEdit(low=1)
        self.tol = gui_widgets.IntLineEdit(low=0)
        self.I0.setValue(180)
        self.Rt.setValue(95)
        self.mindelta.setValue(5)
        self.maxchange.setValue(2)
        self.minintv.setValue(14)
        self.maxintv.setValue(1865)
        self.tol.setValue(30)
        self.conf = gui_widgets.FloatLineEdit(low=.001, high=99.999)
        self.conf.setValue(50)
        layout = QtWidgets.QFormLayout()
        layout.addRow('Current Assigned Interval (days)', self.I0)
        layout.addRow('Reliability Target %', self.Rt)
        layout.addRow('Maximum Change Factor', self.maxchange)
        layout.addRow('Minimum Change (days)', self.mindelta)
        layout.addRow('Minimum Allowed Interval (days)', self.minintv)
        layout.addRow('Maximum Allowed Interval (days)', self.maxintv)
        layout.addRow('Minimum Rejection Confidence %', self.conf)
        if self.showtol:
            layout.addRow('Asset Interval Tolerance (days)', self.tol)

        self.I0.setToolTip('Currently assigned interval for the calibrations in the table')
        self.Rt.setToolTip('Desired end-of-period reliability as a percent')
        self.maxchange.setToolTip('Maximum allowable change in interval, as a fraction of the current interval.\nThe new interval will not be greater than current*maxchange or less than current/maxchange.\nEqual to the "b" parameter of Method A3.')
        self.mindelta.setToolTip('Minimum number of days required to change the interval.\nSuggested interval will remain the same if calculated interval is within this many days.')
        self.minintv.setToolTip('Minimum allowable interval, in days')
        self.maxintv.setToolTip('Maximum allowable interval, in days')
        self.conf.setToolTip('Confidence required before rejecting the current interval in favor of the new interval.')
        self.tol.setToolTip('Actual calibration interval must be within this many days of the assigned interval to be used in the calculation.')

        self.setLayout(layout)
        self.I0.editingFinished.connect(self.changed)
        self.Rt.editingFinished.connect(self.changed)
        self.mindelta.editingFinished.connect(self.changed)
        self.maxchange.editingFinished.connect(self.changed)
        self.minintv.editingFinished.connect(self.changed)
        self.maxintv.editingFinished.connect(self.changed)
        self.tol.editingFinished.connect(self.changed)
        self.conf.editingFinished.connect(self.changed)

    def get_params(self):
        ''' Get parameters for A3 method '''
        p = {'I0': self.I0.value(),
             'Rt': self.Rt.value()/100,
             'maxchange': self.maxchange.value(),
             'conf': self.conf.value()/100,
             'mindelta': self.mindelta.value(),
             'minint': self.minintv.value(),
             'maxint': self.maxintv.value()}
        if self.showtol:
            p['tol'] = self.tol.value()
        return p

    def set_params(self, params):
        ''' Fill widgets with parameters '''
        self.I0.setValue(params.get('I0', 180))
        self.Rt.setValue(params.get('Rt', .95) * 100)
        self.maxchange.setValue(params.get('maxchange', 2))
        self.conf.setValue(params.get('conf', .95)*100)
        self.mindelta.setValue(params.get('mindelta', 5))
        self.minintv.setValue(params.get('minint', 14))
        self.maxintv.setValue(params.get('maxint', 1865))
        self.tol.setValue(params.get('tol', 30))


class S2Params(QtWidgets.QGroupBox):
    ''' Widget for entering parameters for method S2 '''
    changed = QtCore.pyqtSignal()

    def __init__(self, showbins=False, parent=None):
        super().__init__('Binomial Method (S2) Options', parent=parent)
        self.showbins = showbins
        self.Rt = gui_widgets.FloatLineEdit(low=.001, high=99.999)
        self.Rt.setValue(95)
        self.conf = gui_widgets.FloatLineEdit(low=0.001, high=99.999)
        self.conf.setValue(95)
        self.bins = QtWidgets.QSpinBox()
        self.bins.setRange(3, 999)
        self.bins.setValue(10)
        layout = QtWidgets.QFormLayout()
        layout.addRow('Reliability Target %', self.Rt)
        layout.addRow('Confidence % for Interval Range', self.conf)
        if self.showbins:
            layout.addRow('Bins', self.bins)

        self.Rt.setToolTip('Desired end-of-period reliability as a percent')
        self.conf.setToolTip('Confidence for calculating range of intervals')
        self.bins.setToolTip('Number of bins for condensing individual calibrations into summary statistics.')

        self.setLayout(layout)
        self.Rt.editingFinished.connect(self.changed)
        self.conf.editingFinished.connect(self.changed)
        self.bins.valueChanged.connect(self.changed)

    def get_params(self):
        ''' Get parameters for S2 method '''
        p = {'Rt': self.Rt.value()/100,
             'conf': self.conf.value()/100}
        if self.showbins:
            p['bins'] = self.bins.value()
        return p

    def set_params(self, params):
        ''' Fill widgets with parameters '''
        self.Rt.setValue(params.get('Rt', .95)*100)
        self.conf.setValue(params.get('conf', .95)*100)
        self.bins.setValue(params.get('bins', 10))


class VarsParams(QtWidgets.QGroupBox):
    ''' Widget for entering parameters for Variables method '''
    changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__('Variables Method Options', parent=parent)
        self.u0 = gui_widgets.FloatLineEdit()
        self.u0.setValue(0)
        self.y0 = gui_widgets.FloatLineEdit()
        self.y0.setValue(0)
        self.m = QtWidgets.QSpinBox()
        self.m.setRange(1, 3)
        self.utargetbox = QtWidgets.QGroupBox('Uncertainty Target')
        self.utargetbox.setCheckable(True)
        self.utarget = gui_widgets.FloatLineEdit()
        self.utarget.setValue(1)
        self.rtargetbox = QtWidgets.QGroupBox('Reliability Target')
        self.rtargetbox.setCheckable(True)
        self.rlimL = gui_widgets.FloatLineEdit()
        self.rlimU = gui_widgets.FloatLineEdit()
        self.rlimL.setValue(-1)
        self.rlimU.setValue(1)
        self.rconf = gui_widgets.FloatLineEdit(low=0, high=99.999)
        self.rconf.setValue(95)
        flayout = QtWidgets.QFormLayout()
        flayout.addRow('Measurement Uncertainty', self.u0)
        flayout.addRow('Initial Deviation Value', self.y0)
        flayout.addRow('Fit Polynomial Order', self.m)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(flayout)
        ulayout = QtWidgets.QFormLayout()
        ulayout.addRow('Uncertainty', self.utarget)
        self.utargetbox.setLayout(ulayout)
        rlayout = QtWidgets.QFormLayout()
        rlayout.addRow('Lower Limit', self.rlimL)
        rlayout.addRow('Upper Limit', self.rlimU)
        rlayout.addRow('Confidence %', self.rconf)
        self.rtargetbox.setLayout(rlayout)
        layout.addWidget(self.utargetbox)
        layout.addWidget(self.rtargetbox)
        self.setLayout(layout)

        self.u0.setToolTip('Uncertainty in new measurements')
        self.y0.setToolTip('Deviation from nominal at time zero')
        self.m.setToolTip('Order of polynomial fit to deviation vs time curve')
        self.utarget.setToolTip('Maximum projected uncertainty before ending interval')
        self.rlimL.setToolTip('Lower deviation limit. Interval ends when fit polynomial minus uncertainty falls below this limit.')
        self.rlimU.setToolTip('Upper deviation limit. Interval ends when fit polynomial plus uncertainty exceeds this limit.')
        self.rconf.setToolTip('Confidence in polynomial fit uncertainty')

        self.u0.editingFinished.connect(self.changed)
        self.y0.editingFinished.connect(self.changed)
        self.m.valueChanged.connect(self.changed)
        self.utarget.editingFinished.connect(self.changed)
        self.rlimL.editingFinished.connect(self.changed)
        self.rlimU.editingFinished.connect(self.changed)
        self.rconf.editingFinished.connect(self.changed)
        self.utargetbox.toggled.connect(self.changed)
        self.rtargetbox.toggled.connect(self.changed)

    def get_params(self):
        ''' Get parameters for variables method '''
        p = {'u0': self.u0.value(),
             'y0': self.y0.value(),
             'm': self.m.value(),
             'utarget': self.utarget.value(),
             'rlimitL': self.rlimL.value(),
             'rlimitU': self.rlimU.value(),
             'rconf': self.rconf.value()/100,
             'calcrel': self.rtargetbox.isChecked(),
             'calcunc': self.utargetbox.isChecked()}
        return p

    def set_params(self, params):
        ''' Fill widgets with parameters '''
        self.u0.setValue(params.get('u0', 0))
        self.y0.setValue(params.get('y0', 0))
        self.m.setValue(params.get('m', 1))
        self.utarget.setValue(params.get('utarget', 1))
        rlimits = params.get('rlimits', (-1, 1))
        self.rlimL.setValue(rlimits[0])
        self.rlimU.setValue(rlimits[1])
        self.rconf.setValue(params.get('rconf', .95)*100)
        self.rtargetbox.setChecked(params.get('calcrel', True))
        self.utargetbox.setChecked(params.get('calcunc', True))


class IntervalTable(gui_widgets.FloatTableWidget):
    ''' Table widget for interval data entry '''
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mode = 'intervaltest'

    def setup_table(self, mode='testinterval', startend=True, foundleft=True):
        ''' Configure table for the given interval mode '''
        currentdata = self.get_data()
        self.startend = startend
        self.foundleft = foundleft
        self.mode = mode

        if mode in ['intervaltestasset', 'intervalbinomasset']:
            hdrs = ['Interval End', 'Pass/Fail']
            if startend:
                hdrs.insert(0, 'Interval Start')
            self.setColumnCount(len(hdrs))
            self.setHorizontalHeaderLabels(hdrs)

        elif mode == 'intervalvariablesasset':
            hdrs = ['Interval End']
            if startend:
                hdrs.insert(0, 'Interval Start')
            if self.foundleft:
                hdrs.append('As-Found Value')
            hdrs.append('As-Left Value')
            self.setColumnCount(len(hdrs))
            self.setHorizontalHeaderLabels(hdrs)

        elif mode == 'intervaltest':
            hdrs = ['Number In-Tolerance', 'Total Calibrations']
            self.setColumnCount(len(hdrs))
            self.setRowCount(1)
            self.setHorizontalHeaderLabels(hdrs)
            self.maxrows = 1

        elif mode == 'intervalbinom':
            hdrs = ['Interval Length', 'Observed Reliability', 'Total Calibrations']
            self.setColumnCount(len(hdrs))
            self.setHorizontalHeaderLabels(hdrs)

        elif mode == 'intervalvariables':
            hdrs = ['Interval Length', 'Deviation from Prior']
            self.setColumnCount(len(hdrs))
            self.setHorizontalHeaderLabels(hdrs)

        else:
            raise ValueError

        self.maxcols = len(hdrs)
        self.filldata(currentdata)
        self.resizeColumnsToContents()

    def get_data(self):
        ''' Get interval data as dictionary '''
        hdr = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]
        tabledata = self.get_table()  # Strips rows with blanks
        if len(tabledata) == 0:
            return {}

        startcol = get_colidx(hdr, 'Interval Start')
        endcol = get_colidx(hdr, 'Interval End')
        pfcol = get_colidx(hdr, 'Pass/Fail')
        if self.mode in ['intervaltestasset', 'intervalbinomasset']:
            dat = {'startdates': tabledata[startcol] if startcol is not None else None,
                   'enddates': tabledata[endcol] if endcol is not None else None,
                   'passfail': tabledata[pfcol] if pfcol is not None else None}

        elif self.mode == 'intervalvariablesasset':
            asfound = get_colidx(hdr, 'As-Found Value')
            asleft = get_colidx(hdr, 'As-Left Value')
            dat = {'startdates': tabledata[startcol] if startcol is not None else None,
                   'enddates': tabledata[endcol] if endcol is not None else None,
                   'asfound': tabledata[asfound] if asfound is not None else None,
                   'asleft': tabledata[asleft] if asleft is not None else None}

        elif self.mode == 'intervaltest':
            intol = get_colidx(hdr, 'Number In-Tolerance')
            n = get_colidx(hdr, 'Total Calibrations')

            dat = {'intol': tabledata[intol][0],
                   'n': tabledata[n][0]}

        elif self.mode == 'intervalbinom':
            dt = get_colidx(hdr, 'Interval Length')
            ri = get_colidx(hdr, 'Observed Reliability')
            n = get_colidx(hdr, 'Total Calibrations')
            dat = {'ti': tabledata[dt],
                   'ri': tabledata[ri],
                   'ni': tabledata[n]}

        elif self.mode == 'intervalvariables':
            t = get_colidx(hdr, 'Interval Length')
            y = get_colidx(hdr, 'Deviation from Prior')
            dat = {'t': tabledata[t],
                   'y': tabledata[y]}

        return dat

    def filldata(self, dat):
        ''' Fill table with data from dictionary '''
        self.blockSignals(True)
        hdr = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]
        startcol = get_colidx(hdr, 'Interval Start')
        endcol = get_colidx(hdr, 'Interval End')
        pfcol = get_colidx(hdr, 'Pass/Fail')
        foundcol = get_colidx(hdr, 'As-Found Value')
        leftcol = get_colidx(hdr, 'As-Left Value')
        ticol = get_colidx(hdr, 'Interval Length')
        ricol = get_colidx(hdr, 'Observed Reliability')
        nicol = get_colidx(hdr, 'Total Calibrations')
        intolcol = get_colidx(hdr, 'Number In-Tolerance')
        deltacol = get_colidx(hdr, 'Deviation from Prior')

        self.clear()
        try:
            rowcount = max([len(dat[k]) for k in dat.keys() if dat[k] is not None])
            rowcount = max(rowcount, 1)
        except (ValueError, TypeError):
            rowcount = 1  # No values
        self.setRowCount(rowcount)

        def fillcol(colidx, vals, date=False):
            if colidx is not None and vals is not None:
                vals = np.atleast_1d(vals)
                for i, val in enumerate(vals):
                    if date:
                        self.setItem(i, colidx, QtWidgets.QTableWidgetItem(mdates.num2date(val).strftime('%d-%b-%Y')))
                    else:
                        self.setItem(i, colidx, QtWidgets.QTableWidgetItem(str(val)))

        fillcol(startcol, dat.get('startdates', None), date=True)
        fillcol(endcol, dat.get('enddates', None), date=True)
        fillcol(pfcol, dat.get('passfail', None))
        fillcol(foundcol, dat.get('asfound', None))
        fillcol(leftcol, dat.get('asleft', None))
        fillcol(ricol, dat.get('ri', None))
        fillcol(nicol, dat.get('ni', None))
        fillcol(ticol, dat.get('ti', dat.get('dt', None)))
        fillcol(intolcol, dat.get('intol', None))
        fillcol(deltacol, dat.get('deltas', None))
        if self.mode == 'intervaltest' and 'intol' in dat:
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(str(dat.get('intol'))))
            self.setItem(0, 1, QtWidgets.QTableWidgetItem(str(dat.get('total'))))

        self.blockSignals(False)


class IntervalWidget(QtWidgets.QWidget):
    ''' Widget for calibration interval calculations '''
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.uinterval = item
        self.table = IntervalTable()
        self.asset = QtWidgets.QComboBox()
        self.asset.addItems(['A'])
        self.asset.setToolTip('Calibration data from multiple assets can be entered. Select different assets here.')
        self.addremasset = gui_widgets.PlusMinusButton()
        self.addremasset.btnplus.setToolTip('Add an asset to the interval calculation')
        self.addremasset.btnminus.setToolTip('Remove the current asset from the interval calculation')
        self.chkStartDates = QtWidgets.QCheckBox('Enter start and end dates')
        self.chkFoundLeft = QtWidgets.QCheckBox('Enter as-found and as-left values')
        self.txtNotes = QtWidgets.QPlainTextEdit()
        self.txtOutput = gui_widgets.MarkdownTextEdit()
        self.btnCalc = QtWidgets.QPushButton('Calculate')

        self.init_mode()
        if self.mode in ['intervalvariables', 'intervalvariablesasset']:
            self.params = VarsParams()
        elif self.mode in ['intervaltest', 'intervaltestasset']:
            self.params = A3Params(showtol=isinstance(item, attributes.TestIntervalAssets))
        else:
            self.params = S2Params(showbins=isinstance(item, attributes.BinomialIntervalAssets))

        clayout = QtWidgets.QVBoxLayout()
        if 'asset' in self.mode:
            alayout = QtWidgets.QHBoxLayout()
            alayout.addWidget(QtWidgets.QLabel('Asset:'))
            alayout.addWidget(self.asset, stretch=4)
            alayout.addWidget(self.addremasset)
            clayout.addLayout(alayout)
        clayout.addWidget(self.table)
        clayout.addWidget(self.chkStartDates)
        clayout.addWidget(self.chkFoundLeft)
        inbox = QtWidgets.QGroupBox('Calibration Data')
        inbox.setLayout(clayout)
        llayout = QtWidgets.QVBoxLayout()
        llayout.addWidget(inbox)
        llayout.addWidget(self.btnCalc)
        r1layout = QtWidgets.QHBoxLayout()
        r1layout.addWidget(self.params)
        notes = QtWidgets.QGroupBox('Notes')
        nlayout = QtWidgets.QVBoxLayout()
        nlayout.addWidget(self.txtNotes)
        notes.setLayout(nlayout)
        r1layout.addWidget(notes)
        rlayout = QtWidgets.QVBoxLayout()
        rlayout.addLayout(r1layout, stretch=1)
        outbox = QtWidgets.QGroupBox('Results')
        outlayout = QtWidgets.QVBoxLayout()
        outlayout.addWidget(self.txtOutput)
        outbox.setLayout(outlayout)
        rlayout.addWidget(outbox, stretch=3)
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(llayout, stretch=2)
        layout.addLayout(rlayout, stretch=3)
        self.setLayout(layout)

        self.actLoadData = QtWidgets.QAction('Insert Data From...', self)
        self.actSaveReport = QtWidgets.QAction('Save Report...', self)
        self.actClear = QtWidgets.QAction('Clear Table', self)
        self.actSaveReport.setEnabled(False)
        self.menu = QtWidgets.QMenu('Intervals')
        self.menu.addSeparator()
        self.menu.addAction(self.actLoadData)
        self.menu.addAction(self.actSaveReport)
        self.menu.addAction(self.actClear)
        self.menu.addSeparator()
        self.menu.addAction(self.actSaveReport)

        self.txtNotes.setPlainText(self.uinterval.description)
        self.table.setRowCount(1)
        self.init_data()
        self.chkStartDates.stateChanged.connect(self.setup_table)
        self.chkFoundLeft.stateChanged.connect(self.setup_table)
        self.asset.currentIndexChanged.connect(self.change_asset)
        self.addremasset.plusclicked.connect(self.add_asset)
        self.addremasset.minusclicked.connect(self.rem_asset)
        self.btnCalc.clicked.connect(self.calculate)
        self.table.valueChanged.connect(self.update_data)
        self.params.changed.connect(self.update_data)
        self.txtNotes.textChanged.connect(self.update_data)
        self.actClear.triggered.connect(self.clear_table)
        self.actSaveReport.triggered.connect(self.save_report)
        self.actLoadData.triggered.connect(self.load_data)

    def init_mode(self):
        self.chkFoundLeft.setVisible(False)
        self.chkStartDates.setVisible(False)
        if isinstance(self.uinterval, attributes.TestInterval):
            self.mode = 'intervaltest'
        elif isinstance(self.uinterval, attributes.BinomialInterval):
            self.mode = 'intervalbinom'
        elif isinstance(self.uinterval, attributes.TestIntervalAssets):
            self.mode = 'intervaltestasset'
        elif isinstance(self.uinterval, attributes.BinomialIntervalAssets):
            self.mode = 'intervalbinomasset'
        elif isinstance(self.uinterval, variables.VariablesInterval):
            self.mode = 'intervalvariables'
        elif isinstance(self.uinterval, variables.VariablesIntervalAssets):
            self.mode = 'intervalvariablesasset'
            self.chkFoundLeft.setVisible(True)
        else:
            raise ValueError

        if 'asset' in self.mode:
            self.chkStartDates.setVisible(True)

    def init_data(self):
        ''' Initialize data with values from saved config '''
        config = self.uinterval.get_config()
        self.params.set_params(config)
        if 'asset' in self.mode:
            assetdict = config.get('assets', {})
            if len(assetdict) > 0:
                self.chkFoundLeft.setChecked(any([d.get('asfound', None) is not None for d in assetdict.values()]))
                self.chkStartDates.setChecked(any([d.get('startdates', None) is not None for d in assetdict.values()]))
                self.asset.clear()
                self.asset.addItems(assetdict.keys())
                dat = assetdict.get(self.asset.currentText(), {})
            self.setup_table()
            if len(assetdict) > 0:
                self.table.filldata(dat)
        elif self.mode == 'intervalbinom':
            dat = {'ri': config.get('ri', []),
                   'ni': config.get('ni', []),
                   'ti': config.get('ti', [])}
            self.setup_table()
            self.table.filldata(dat)
        elif self.mode == 'intervaltest':
            dat = {'intol': config.get('intol', 0),
                   'total': config.get('total', 1)}
            self.setup_table()
            self.table.filldata(dat)
        elif self.mode == 'intervalvariables':
            dat = {'dt': config.get('dt', []),
                   'deltas': config.get('deltas', [])}
            self.setup_table()
            self.table.filldata(dat)

    def setup_table(self):
        ''' Setup the data table for the data entry format '''
        self.table.setup_table(self.mode, self.chkStartDates.isChecked(), self.chkFoundLeft.isChecked())

    def clear_table(self):
        ''' Clear the table (only for the current asset) '''
        self.table.clear()

    def update_data(self):
        ''' Save inputs back to model '''
        dat = self.table.get_data()  # dictionary
        params = self.params.get_params()
        assetname = self.asset.currentText()

        if 'asset' in self.mode:
            self.uinterval.updateasset(assetname, **dat)
        else:
            self.uinterval.update(**dat)

        self.uinterval.update_params(**params)
        self.uinterval.description = self.txtNotes.toPlainText()

    def calculate(self):
        ''' Run the calculation '''
        try:
            self.uinterval.calculate()
        except (TypeError, ValueError, RuntimeError):
            self.txtOutput.setHtml('Error computing interval.')
        else:
            self.txtOutput.setReport(self.get_report())
            self.actSaveReport.setEnabled(True)

    def change_asset(self, idx):
        ''' New asset selected in combobox '''
        assetname = self.asset.currentText()
        if assetname in self.uinterval.assets:
            dat = self.uinterval.assets[assetname]
            self.table.filldata(dat)
        else:
            self.table.clear()

    def add_asset(self):
        ''' Add a new asset to the dropdown '''
        name, ok = QtWidgets.QInputDialog.getText(self, 'New Asset', 'Asset Name:')
        if ok:
            self.asset.addItems([name])
            self.asset.setCurrentIndex(self.asset.count()-1)

    def rem_asset(self):
        ''' Remove current asset from dropdown '''
        if self.asset.count() > 0:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle('Uncertainty Calculator')
            mbox.setText('Remove asset {}?'.format(self.asset.currentText()))
            mbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            ok = mbox.exec_()
            if ok == QtWidgets.QMessageBox.Yes:
                self.uinterval.remasset(self.asset.currentText())
                self.asset.removeItem(self.asset.currentIndex())

    def load_data(self):
        ''' Import data from CSV or another calculation '''
        cols = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        dlg = page_dataimport.ArraySelectWidget(project=self.uinterval.project,
                                                colnames=cols)
        ok = dlg.exec_()
        if ok:
            dat = dlg.get_array()
            for col, colname in enumerate(cols):
                if colname in dat:
                    for row, val in enumerate(dat[colname]):
                        if colname in ['Interval Start', 'Interval End']:
                            self.table.setItem(row, col, QtWidgets.QTableWidgetItem(mdates.num2date(val).strftime('%d-%b-%Y')))
                        else:
                            self.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(val)))
                    self.table.setRowCount(row)

    def get_menu(self):
        ''' Get the menu for this widget '''
        return self.menu

    def get_report(self):
        ''' Get full report of curve fit, using page settings '''
        return self.uinterval.out.report_summary()

    def save_report(self):
        ''' Save full report, asking user for settings/filename '''
        gui_widgets.savereport(self.get_report())
