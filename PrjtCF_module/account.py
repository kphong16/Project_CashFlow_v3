import pandas as pd
import numpy as np


class account(object):
    def __init__(self, 
                title = None, # string
                tag = None, # string tuple
                mtrt = 0, # int
                bal_strt = 0, # int
                add_scdd_ipt = pd.Series([0], index=[0]), # Series
                sub_scdd_ipt = pd.Series([0], index=[0]), # Series
                note = ""): # string
        self.title = title
        self.tag = tag
        self.mtrt = mtrt
        self.bal_strt = bal_strt
        self.add_scdd_ipt = add_scdd_ipt
        self.sub_scdd_ipt = sub_scdd_ipt
        self.note = note
        self.setdf()
        self.setjnl()
        
    #### INITIAL SETTING ####
    def setdf(self):
        self.dfcol = ['add_scdd', 'add_scdd_cum', 'sub_scdd', 'sub_scdd_cum', 'bal_strt', 'amt_add', 'amt_add_cum',
                      'amt_sub', 'amt_sub_cum', 'bal_end', 'add_rsdl_cum', 'sub_rsdl_cum']
        self.dfidx = np.arange(-1, self.mtrt + 1)
        self.df = pd.DataFrame(np.zeros([len(self.dfidx), len(self.dfcol)]), columns=self.dfcol, index=self.dfidx)
        self.df.loc[-1, 'bal_strt'] = self.bal_strt
        self.df.loc[self.add_scdd_ipt.index, 'add_scdd'] = self.add_scdd_ipt
        self.df.loc[self.sub_scdd_ipt.index, 'sub_scdd'] = self.sub_scdd_ipt
        self._cal_bal()
        
    def setjnl(self):
        self.jnlcol = ['amt_add', 'amt_sub', 'note']
        self.jnlidx = [-1]
        self.jnl = pd.DataFrame(np.zeros([len(self.jnlidx), len(self.jnlcol)]), columns=self.jnlcol, index=self.jnlidx)
    #### INITIAL SETTING ####
    
    #### INPUT DATA ####
    def addscdd(self, index, amt):
        self.df.loc[index, 'add_scdd'] += amt
        self._cal_bal()

    def subscdd(self, index, amt):
        self.df.loc[index, 'sub_scdd'] += amt
        self._cal_bal()

    def addamt(self, index, amt, note=""):
        tmpjnl = pd.DataFrame([[amt, 0, note]], columns=self.jnlcol, index=[index])
        self.jnl = pd.concat([self.jnl, tmpjnl])
        
        self.df.loc[index, 'amt_add'] += amt
        self._cal_bal()
        
    def subamt(self, index, amt, note=""):
        tmpjnl = pd.DataFrame([[0, amt, note]], columns=self.jnlcol, index=[index])
        self.jnl = pd.concat([self.jnl, tmpjnl])
        
        self.df.loc[index, 'amt_sub'] += amt
        self._cal_bal()

    def calamt(self, index, amt, note=""):
        if amt >= 0:
            self.addamt(index, amt, note)
        else:
            self.subamt(index, -amt, note)

    def add_exctn(self, idx=0, rate=1):
        self.addamt(idx, self.add_scdd_cum(idx) * rate)
        for idx in np.arange(idx, self.mtrt+1):
            self.addamt(idx, (self.add_scdd_cum(idx) - self.add_scdd_cum(idx-1)) * rate)

    def sub_exctn(self, idx=0, rate=1):
        if type(idx) in [int]:
            self.subamt(idx, self.sub_scdd_cum(idx) * rate)
            for idx in np.arange(idx+1, self.mtrt+1):
                self.subamt(idx, (self.sub_scdd_cum(idx) - self.sub_scdd_cum(idx-1)) * rate)
        else:
            for i, tmpidx in enumerate(idx):
                self.subamt(tmpidx, self.sub_scdd_cum(tmpidx) * rate[i])
                for k in np.arange(tmpidx+1, self.mtrt + 1):
                    self.subamt(k, (self.sub_scdd_cum(k) - self.sub_scdd_cum(k - 1)) * rate[i])
    #### INPUT DATA ####
    
    #### OUTPUT DATA ####
    def bal_strt(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'bal_strt']
        else:
            return self.df.loc[idx, 'bal_strt']
        
    def bal_end(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'bal_end']
        else:
            return self.df.loc[idx, 'bal_end']
        
    def add_scdd(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'add_scdd']
        else:
            return self.df.loc[idx, 'add_scdd']

    def amt_add_cum(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'amt_add_cum']
        else:
            return self.df.loc[idx, 'amt_add_cum']

    def amt_sub_cum(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'amt_sub_cum']
        else:
            return self.df.loc[idx, 'amt_sub_cum']

    def add_scdd_cum(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'add_scdd_cum']
        else:
            return self.df.loc[idx, 'add_scdd_cum']

    def sub_scdd_cum(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'sub_scdd_cum']
        else:
            return self.df.loc[idx, 'sub_scdd_cum']
    
    def add_rsdl(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'add_rsdl_cum']
        else:
            return self.df.loc[idx, 'add_rsdl_cum']

    def sub_rsdl(self, idx=None):
        if idx is None:
            return self.df.loc[:, 'sub_rsdl_cum']
        else:
            return self.df.loc[idx, 'sub_rsdl_cum']
    #### OUTPUT DATA ####
    
    #### CALCULATE DATA ####
    def _cal_bal(self):
        self.df.loc[:, 'add_scdd_cum'] = self.df.loc[:, 'add_scdd'].cumsum()
        self.df.loc[:, 'sub_scdd_cum'] = self.df.loc[:, 'sub_scdd'].cumsum()
        self.df.loc[:, 'amt_add_cum'] = self.df.loc[:, 'amt_add'].cumsum()
        self.df.loc[:, 'amt_sub_cum'] = self.df.loc[:, 'amt_sub'].cumsum()
        
        self.df.loc[-1, 'bal_end'] = self.df.loc[-1, 'bal_strt'] + self.df.loc[-1, 'amt_add'] \
                                     - self.df.loc[-1, 'amt_sub']
        for idx in np.arange(0, self.mtrt + 1):
            self.df.loc[idx, 'bal_strt'] = self.df.loc[idx-1, 'bal_end']
            self.df.loc[idx, 'bal_end'] = self.df.loc[idx, 'bal_strt'] + self.df.loc[idx, 'amt_add'] \
                                          - self.df.loc[idx, 'amt_sub']
        self.df.loc[:, 'add_rsdl_cum'] = self.df.loc[:, 'add_scdd_cum'] - self.df.loc[:, 'amt_add_cum']
        self.df.loc[:, 'sub_rsdl_cum'] = self.df.loc[:, 'sub_scdd_cum'] - self.df.loc[:, 'amt_sub_cum']
    #### CALCULATE DATA ####
    
    
class merge(object):
    def __init__(self, dct):
        self.dct = dct # dictionary

    @property
    def df(self):
        tmp_dct = sum([self.dct[x].df for x in self.dct])
        return tmp_dct

    def df_var(self, var):
        tmp_dct = pd.DataFrame({x: self.dct[x].df.loc[:, var] for x in self.dct})
        return tmp_dct

    def title(self):
        tmp_dct = pd.Series({x: self.dct[x].title for x in self.dct})
        return tmp_dct
    
    def tag(self):
        tmp_dct = pd.Series({x: self.dct[x].tag for x in self.dct})
        return tmp_dct
    
    def mtrt(self):
        tmp_dct = pd.Series({x: self.dct[x].mtrt for x in self.dct})
        return tmp_dct
    
    def note(self):
        tmp_dct = pd.Series({x: self.dct[x].note for x in self.dct})
        return tmp_dct


class Loan(object):
    def __init__(self,
                 title=None, # string
                 tag=None, # string tuple
                 mtrt = 0, # int
                 ntnl = 0.0, # float
                 rate = 0.0, # float
                 note=""): # string
        self.title = title
        self.tag = tag
        self.mtrt = mtrt
        self.ntnl = ntnl
        self.rate = rate
        self.note = note
        self.setdf()

    def setdf(self):
        self.amt = account(title=self.title, tag=self.tag, mtrt=self.mtrt,
                           bal_strt=self.ntnl,
                           sub_scdd_ipt=pd.Series([self.ntnl], index=[0]),
                           add_scdd_ipt=pd.Series([self.ntnl], index=[self.mtrt]),
                           note=self.note)
        self.IR = account(mtrt=self.mtrt)

    @property
    def df(self):
        tmp_df = {'amt_loan': self.amt.df.loc[:, 'amt_sub_cum'] - self.amt.df.loc[:, 'amt_add_cum'],
                  'amt_IR_scdd': self.IR.df.loc[:, 'add_scdd'],
                  'amt_IR_paid': self.IR.df.loc[:, 'amt_add']}
        return pd.DataFrame(tmp_df)

    def loan_rsdl(self, idx):
        return self.amt.df.loc[idx, 'amt_sub_cum'] - self.amt.df.loc[idx, 'amt_add_cum']

    def is_repaid(self, idx):
        if self.amt.df.loc[idx, 'sub_rsdl_cum'] <= 0 and self.loan_rsdl(idx) <= 0:
            return True
        else:
            return False

def result(col_dict):
    "col_dict = {'key': [key_class], 'col_name1', 'col_name2], ...]}"
    result = dict()
    for key, val in col_dict.items():
        for i in range(1, len(val)):
            result[(key, val[i])] = val[0].df[val[i]]
    result = pd.DataFrame(result)

    return result