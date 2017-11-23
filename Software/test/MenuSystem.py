""" Menu System
	Author: Dingjun Yue
	Date: Nov./2017
"""

# List of menu ids for each menu level
menuLevel1 = [1, 2, 3, 4, 5] # Top menu level
menuLevel12 = [11, 12, 13, 14] # Sub menu of menuItem 1
menuLevel22 = [21, 22] # Sub menu of menuItem 2
menuLevel32 = [31] # Sub menu of menuItem 3
menuLevel42 = [41, 42] # Sub menu of menuItem 4
menuLevel52 = [51] # Sub menu of menuItem 5

class MenuItem(object):
	
	def __init__(self, menuID):
		self.menuID = menuID
		#self.menuTitle = menuTitle
		
	def stringForDisplay(self):
		return self.menuTitle
		
    def getMenuID(self):
        return self.menuID
    
    # This method returns the menu's location on the screen (1, 2, 3...)
    def getMenuLocation(self):
		return (self.menuID % 10)