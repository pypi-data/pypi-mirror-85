test_case= [
            {
                "indices": [
                    [
                        3,
                        3
                    ],
                    [
                        3,
                        0
                    ],
                    [
                        4,
                        3
                    ],
                    [
                        4,
                        0
                    ],
                    [
                        5,
                        3
                    ],
                    [
                        5,
                        0
                    ],
                    [
                        6,
                        3
                    ],
                    [
                        6,
                        0
                    ],
                    [
                        7,
                        3
                    ],
                    [
                        7,
                        0
                    ],
                    [
                        8,
                        3
                    ],
                    [
                        8,
                        0
                    ],
                    [
                        9,
                        3
                    ],
                    [
                        9,
                        0
                    ],
                    [
                        10,
                        3
                    ],
                    [
                        10,
                        0
                    ],
                    [
                        11,
                        3
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        12,
                        3
                    ],
                    [
                        12,
                        0
                    ],
                    [
                        13,
                        3
                    ],
                    [
                        13,
                        0
                    ],
                    [
                        14,
                        3
                    ],
                    [
                        14,
                        0
                    ],
                    [
                        15,
                        3
                    ],
                    [
                        15,
                        0
                    ],
                    [
                        16,
                        3
                    ],
                    [
                        16,
                        0
                    ],
                    [
                        17,
                        3
                    ],
                    [
                        17,
                        0
                    ],
                    [
                        18,
                        3
                    ],
                    [
                        18,
                        0
                    ]
                ],
                "type": "qualifier"
            },
            {
                "indices": [
                    [
                        3,
                        2
                    ],
                    [
                        4,
                        2
                    ],
                    [
                        5,
                        2
                    ],
                    [
                        6,
                        2
                    ],
                    [
                        7,
                        2
                    ],
                    [
                        8,
                        2
                    ],
                    [
                        9,
                        2
                    ],
                    [
                        10,
                        2
                    ],
                    [
                        11,
                        2
                    ],
                    [
                        12,
                        2
                    ],
                    [
                        13,
                        2
                    ],
                    [
                        14,
                        2
                    ],
                    [
                        15,
                        2
                    ],
                    [
                        16,
                        2
                    ],
                    [
                        17,
                        2
                    ],
                    [
                        18,
                        2
                    ]
                ],
                "type": "mainSubject"
            },
            {
                "indices": [
                    [
                        3,
                        4
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        5,
                        4
                    ],
                    [
                        6,
                        4
                    ],
                    [
                        7,
                        4
                    ],
                    [
                        8,
                        4
                    ],
                    [
                        9,
                        4
                    ],
                    [
                        10,
                        4
                    ],
                    [
                        11,
                        4
                    ],
                    [
                        12,
                        4
                    ],
                    [
                        13,
                        4
                    ],
                    [
                        14,
                        4
                    ],
                    [
                        15,
                        4
                    ],
                    [
                        16,
                        4
                    ],
                    [
                        17,
                        4
                    ],
                    [
                        18,
                        4
                    ]
                ],
                "type": "dependentVariable"
            },
            {
                "indices": [
                    [
                        3,
                        1
                    ],
                    [
                        4,
                        1
                    ],
                    [
                        5,
                        1
                    ],
                    [
                        6,
                        1
                    ],
                    [
                        7,
                        1
                    ],
                    [
                        8,
                        1
                    ],
                    [
                        9,
                        1
                    ],
                    [
                        10,
                        1
                    ],
                    [
                        11,
                        1
                    ],
                    [
                        12,
                        1
                    ],
                    [
                        13,
                        1
                    ],
                    [
                        14,
                        1
                    ],
                    [
                        15,
                        1
                    ],
                    [
                        16,
                        1
                    ],
                    [
                        17,
                        1
                    ],
                    [
                        18,
                        1
                    ]
                ],
                "type": "property"
            }
        ]

class CellArea:
    def __init__(self, indices):
        self.indices=indices
        row_sorted = sorted(indices, key=lambda index: index[0])
        col_sorted = sorted(indices, key=lambda index: index[1])
        self.min_row=row_sorted[0][0]
        self.max_row=row_sorted[-1][0]
        self.min_col=col_sorted[0][1]
        self.max_col=col_sorted[-1][1]

        self.skipped_cells=[]
        for row in range(self.min_row, self.max_row):
            for col in range(self.min_col, self.max_col):
                if [row, col] not in self.indices:
                    self.skipped_cells.append[[row, col]]

    
    @property
    def dims(self):
        return [self.max_row-self.min_row+1, self.max_col-self.min_col + 1]
    
    @property
    def is_contiguous(self):
        return len(self.skipped_cells)==0
    


def define_relationship(data_rectangle, other_rectangle):
    if other_rectangle.dims==[1,1]:
        #set to a "constant" of whatever the other rectangle is
        pass
    if data_rectangle.dims == other_rectangle.dims:
        if other_rectangle.is_contiguous:
            pass
        else:
            pass


def test():
    data_indices=[]
    mainSubjectIndices=[]
    qualifiers=[]
    properties=[]
    for anote in test_case:
        type = anote["type"]
        indices = anote["indices"]
        if type == "dependentVariable":
            data_indices=indices
        elif type=="mainSubject":
            mainSubjectIndices=indices
        elif type=="qualifier":
            qualifiers.append(anote)
        elif type=="properties":
            properties.append(anote)
    
    data_rectangle=Rectangle.from_indices(data_indices)
    subject_rectangle=Rectangle.from_indices(data_indices)



test()

# some basic rules for yaml formation:

# Qualifiers (purple):
# 1. a qualifier with a single cell is applied to every single statement
# 2. a qualifier with a continuous single-column or single-row region will iterate with dependent variable that follows that region
# 3. a qualifier with split single-column or single-row regions will look for similarly split dependent variable
# 4. a qualifier with split single-cells will follow the -n strategy either leftwards or upwards

# Main subject (blue):
# Other than being required, and limited to only one per statement it should be that main subject has the same issues as qualifier (?)

# Properties (orange):
# 1. any indicated property is going to attempt to find the matching qualifier, main subject, or dependent variable to which it belongs 
# (properties do not exist as standalone objects, without a match they are meaningless)

# Dependent variable (green):
# 1. The dependent variable is simply the region in the yaml. 
# 2. The easiest way to do the dependent variable is simply to leave it the way it was input 
# 3. [ranges + cells - requires change to cell functionality]:
#              selecting cells takes precedence over all skip methods
#              skipping empty cells needs to take place outside of region
# 4. the only interesting challenges related to the dependent variable are relatively linking it to other fields, 
#      whether it's really two dependent variables globbed together
#      or one sparse variable whose spatiral relationships are many steps away
