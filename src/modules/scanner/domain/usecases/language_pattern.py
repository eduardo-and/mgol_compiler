from core.models.enums.token_class import TokenClass
from modules.scanner.models.state import StateUnity

class LanguagePattern:
    statesquantity: int = 27
    transitions= {
        (0,1):[range(48,58)],
        (0,11):[range(97,123), range(65,91)],
        (0,12):[34],
        (0,14):[123],
        (0,16):[0], ## \x00 =EOF
        (0,17):[61], 
        (0,18):[62],
        (0,20):[60],
        (0,23):[45,42,43,47],
        (0,24):[40],
        (0,25):[41],
        (0,26):[59],
        (0,27):[44],
        (1,5):[46],
        (1,2):[range(48,58)],
        (2,2):[range(48,58)],
        (2,3):[46],
        (3,4):[range(48,58)],
        (4,4):[range(48,58)],
        (5,6):[range(48,58)],
        (6,6):[range(48,58)],
        (6,7):[101,69],
        (7,8):[range(48,58)],
        (7,9):[43,45],
        (8,8):[range(48,58)],
        (9,10):[range(48,58)],
        (10,10):[range(48,58)],
        (11,11):[95,range(48,58),range(97,123), range(65,91)],
        (12,12):[range(32,34),range(35,127)], ##anything - "
        (12,13):[34],
        (14,14):[range(32,125),range(126,127)], ##anything - }
        (14,15):[125],
        (18,19):[61],
        (20,21):[45],
        (20,22):[61,62]
    }
    stateClass = [
            ([1,2,4,6,8,9,10],TokenClass.NUM),
            ([11],TokenClass.ID),
            ([13],TokenClass.LIT),
            ([15],TokenClass.COMMENT),
            ([16],TokenClass.EOF),
            ([18,19,17,20,21,22],TokenClass.OPR),
            ([21],TokenClass.RCB),
            ([23],TokenClass.OPM),
            ([23],TokenClass.OPM),
            ([24],TokenClass.AB_P),
            ([25],TokenClass.FC_P),
            ([26],TokenClass.PT_V),
            ([27],TokenClass.VIR)
    ]
    
    def __new__(self)->StateUnity:
        states = [StateUnity(i,resultingClass=TokenClass.ERROR) for i in range(self.statesquantity+1)]
      
        for tokenRef in self.stateClass:
            _states,_tokenClass= tokenRef
            for j in states:
                if(j.id in _states):
                    j.resultingClass = _tokenClass
        
        for (key,pattern) in self.transitions.items():
            _from, _to = key
            states[_from].transitions.append((pattern,states[_to]))
        
        return states[0]
        
                

    