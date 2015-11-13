from Tkinter import *

COMMENT = 0
RULE = 1
RULESETNAME = 2

class RuleSet():
	def __init__(self, name):
		self.name = name
		self.rules = {}
		self.list = []
		
	def addRule(self, str):
		str = str.rstrip('\n').split(';')[0].strip() # Remove comment and spaces
		pair = str.split('=')
		if len(pair) == 2:
			self.rules[pair[0].strip()] = pair[1].strip()
			self.list.append(pair[0].strip())
			return True
		return False
	
	def getVar(self,name):
		return self.rules[name]
		
	def setVar(self,name,value):
		inlist = True
		if not name in self.rules or self.rules[name] == "":
			inlist = name in self.list
		self.rules[name] = value
		if value != "" and not inlist:
			self.list.append(name)
	
	def __str__(self):
		s = "[%s]\n"%self.name
		for r in self.list:
			if self.rules[r] != "":
				s += r + "=" + self.rules[r] + "\n"
		return s

class RuleSets():
	def __init__(self):
		self.rulesets = {}
		self.list = []
	
	def addRuleSet(self,ruleset):
		self.rulesets[ruleset.name] = ruleset
		self.list.append(ruleset)
	
	def getRuleSet(self,name):
		return self.rulesets[name]
	
	def __str__(self):
		s = ""
		for r in self.list:
			s += str(r) + "\n"
		return s
		
def typeOf(s):
	if len(s) > 2 and s[0] == '[' and s[-1] == ']':
		return RULESETNAME
	if len(s.split('='))==2: return RULE
	return COMMENT
	
def getRuleSetName(s):
	if len(s) > 2 and s[0] == '[' and s[-1] == ']':
		return s[1:-1]
	return None

def readRulesIni(filename):
	rulesets = RuleSets()
	curruleset = None
	with open(filename) as f:
		lines = f.readlines()
	for l in lines:
		l = l.rstrip('\n').split(';')[0].strip()
		t = typeOf(l)
		if t == COMMENT: continue
		if t == RULESETNAME:
			name = getRuleSetName(l)
			curruleset = RuleSet(name)
			rulesets.addRuleSet(curruleset)
			continue
		if t == RULE:
			curruleset.addRule(l)
	return rulesets
	
def writeRulesIni(filename,rulesets):
	with open(filename, 'w') as f:
		f.write(str(rulesets))

class EntryBox(Frame):
	def __init__(self,master,name):
		Frame.__init__(self,master)
		self.label = Label(self,text=name)
		self.var = StringVar()
		self.entry = Entry(self,textvariable=self.var,width=60)
		self.label.pack(side=LEFT,fill=X)
		self.entry.pack(side=RIGHT)
		
class EntryCollection(Frame):
	def __init__(self,master,name):
		Frame.__init__(self,master)
		self.entries = {}
		
	def add(self,name):
		self.entries[name] = EntryBox(self,name)
		self.entries[name].pack(side=TOP,fill=X)
	
class EntrySet(Frame):
	def __init__(self,master,name):
		Frame.__init__(self,master)
		self.master = master
		self.scrollbar = Scrollbar(self,orient=VERTICAL)
		self.listbox = Listbox(self,yscrollcommand=self.scrollbar.set,selectmode=SINGLE)
		self.listbox.bind("<<ListboxSelect>>", self.click)
		self.listbox.pack(side=LEFT, fill=BOTH)
		self.scrollbar.pack(side=LEFT, fill=BOTH)
		
		self.collections = {}
		self.oldselect = None
		self.currcollection = None
	
	def add(self,name):
		self.listbox.insert(END,name)
		self.collections[name] = EntryCollection(self,name)
		self.changedSelect()
		
	def get(self, name):
		return self.collections[name]
	
	def click(self,event):
		self.changedSelect()

	def changedSelect(self):
		curr = self.listbox.curselection()
		if self.oldselect != curr:
			self.oldselect = curr
			if self.currcollection != None:
				self.currcollection.pack_forget()
			if len(curr) == 0:
				if self.listbox.size() > 0:
					self.listbox.selection_set("0")
					curr = self.listbox.curselection()
				else:
					return
			name = self.listbox.get(curr[0])
			self.currcollection = self.collections[name]
			self.currcollection.pack(side=LEFT,expand=YES,fill=BOTH)
			
class Configuration(Frame):
	def __init__(self, master):
		Frame.__init__(self,master)
		self.master = master
		self.scrollbar = Scrollbar(self,orient=VERTICAL)
		self.listbox = Listbox(self,yscrollcommand=self.scrollbar.set,selectmode=SINGLE)
		self.scrollbar.config(command=self.listbox.yview)
		self.listbox.bind("<<ListboxSelect>>", self.click)
		self.listbox.pack(side=LEFT, fill=BOTH)
		self.scrollbar.pack(side=LEFT, fill=BOTH)
		
		self.entrysets = {}
		self.oldselect = None
		self.currset = None
		
	def show(self):
		self.pack(side=LEFT, expand=YES, fill=BOTH)
	
	def add(self, name):
		self.listbox.insert(END,name)
		self.entrysets[name] = EntrySet(self,name)
		self.changedSelect()
	
	def get(self, name):
		return self.entrysets[name]
	
	def click(self,event):
		self.changedSelect()
	
	def changedSelect(self):
		curr = self.listbox.curselection()
		if self.oldselect != curr:
			self.oldselect = curr
			if self.currset != None:
				self.currset.pack_forget()
			if len(curr) == 0:
				if self.listbox.size() > 0:
					self.listbox.selection_set("0")
					curr = self.listbox.curselection()
				else:
					return
			name = self.listbox.get(curr[0])
			self.currset = self.entrysets[name]
			self.currset.pack(side=LEFT,expand=YES,fill=BOTH)
	
	def readConfigure(self,rulesets):
		for sname in self.entrysets:
			entryset = self.entrysets[sname]
			for cname in entryset.collections:
				collection = entryset.collections[cname]
				for ename in collection.entries:
					entry = collection.entries[ename]
					try:
						entry.var.set(rulesets.getRuleSet(sname).getVar(ename))
					except:
						entry.var.set("")
					
	def writeConfigure(self,rulesets):
		for sname in self.entrysets:
			entryset = self.entrysets[sname]
			for cname in entryset.collections:
				collection = entryset.collections[cname]
				for ename in collection.entries:
					entry = collection.entries[ename]
					if entry.var.get().strip() != "":
						rulesets.getRuleSet(sname).setVar(ename,entry.var.get().strip())
					else:
						rulesets.getRuleSet(sname).setVar(ename,"")

class Tab(Frame):
	def __init__(self, master, name):
		Frame.__init__(self, master)
		self.tab_name = name

class TabBar(Frame):
	def __init__(self, master=None, init_name=None):
		Frame.__init__(self, master, height=50)
		self.pack_propagate(0)
		self.tabs = {}
		self.buttons = {}
		self.current_tab = None
		self.init_name = init_name
	
	def show(self):
		self.pack(side=TOP, expand=NO, fill=BOTH)
		self.switch_tab(self.init_name or self.tabs.keys()[-1])
	
	def add(self, tab):
		tab.pack_forget()
		
		self.tabs[tab.tab_name] = tab
		b = Button(self, text=tab.tab_name, relief=RAISED,
			command=(lambda name=tab.tab_name: self.switch_tab(name)))
		b.pack(side=LEFT,fill=BOTH)
		self.buttons[tab.tab_name] = b
	
	def delete(self, tabname):
		
		if tabname == self.current_tab:
			self.current_tab = None
			self.tabs[tabname].pack_forget()
			del self.tabs[tabname]
			self.switch_tab(self.tabs.keys()[0])
		
		else: del self.tabs[tabname]
		
		self.buttons[tabname].pack_forget()
		del self.buttons[tabname]
	
	def switch_tab(self, name):
		if self.current_tab:
			self.buttons[self.current_tab].config(relief=RAISED)
			self.tabs[self.current_tab].pack_forget()
		self.tabs[name].pack(side=BOTTOM,expand=YES,fill=BOTH)
		self.current_tab = name
		
		self.buttons[name].config(relief=FLAT)
		
def	openfile():
	global rulesets
	rulesets = readRulesIni("rulesmd.ini")
	readConfigure()
	
def	savefile():
	global rulesets
	writeConfigure()
	writeRulesIni("newrules.ini",rulesets)

def writeConfigure():
	global rulesets
	generalConfig.writeConfigure(rulesets)
	buildingConfig.writeConfigure(rulesets)
	defenceConfig.writeConfigure(rulesets)
	infantryConfig.writeConfigure(rulesets)
	vehicleConfig.writeConfigure(rulesets)
	navalConfig.writeConfigure(rulesets)
	airfoceConfig.writeConfigure(rulesets)
	
def readConfigure():
	global rulesets
	generalConfig.readConfigure(rulesets)
	buildingConfig.readConfigure(rulesets)
	defenceConfig.readConfigure(rulesets)
	infantryConfig.readConfigure(rulesets)
	vehicleConfig.readConfigure(rulesets)
	navalConfig.readConfigure(rulesets)
	airforceConfig.readConfigure(rulesets)
	

if __name__ == '__main__':
		
	root = Tk()
	root.title("RA2 rules editor")
	root.minsize(width=1000, height=600)
	root.maxsize(width=1000, height=600)
	root.resizable(width=FALSE, height=FALSE)
	bar = TabBar(root, "General")
	
	toolBar = Frame(root);
	Button(toolBar,text="Open",command=openfile).pack(side=LEFT,fill=Y)
	Button(toolBar,text="Save",command=savefile).pack(side=LEFT,fill=Y)
	toolBar.pack(side=BOTTOM,fill=X)
	
	tabGeneral = Tab(root, "General")
	Label(tabGeneral, text="General settings").pack(side=TOP)
	tabBuilding = Tab(root, "Buildings")
	Label(tabBuilding, text="Building settings").pack(side=TOP)
	tabDefence = Tab(root, "Defence")
	Label(tabDefence, text="Defence settings").pack(side=TOP)
	tabInfantry = Tab(root, "Infantry")
	Label(tabInfantry, text="Infantry settings").pack(side=TOP)
	tabVehicle = Tab(root, "Vehicle")
	Label(tabVehicle, text="Vehicle settings").pack(side=TOP)
	tabNaval = Tab(root, "Naval")
	Label(tabNaval, text="Naval settings").pack(side=TOP)
	tabAirforce = Tab(root, "Airforce")
	Label(tabAirforce, text="Airforce settings").pack(side=TOP)
	bar.add(tabGeneral)
	bar.add(tabBuilding)
	bar.add(tabDefence)
	bar.add(tabInfantry)
	bar.add(tabVehicle)
	bar.add(tabNaval)
	bar.add(tabAirforce)
	bar.show()
	
	generalConfig = Configuration(tabGeneral)
	generalConfig.add("General")
	generalConfig.get("General").add("Veteran factors")
	generalConfig.get("General").get("Veteran factors").add("VeteranRatio")
	generalConfig.get("General").get("Veteran factors").add("VeteranCombat")
	generalConfig.get("General").get("Veteran factors").add("VeteranSpeed")
	generalConfig.get("General").get("Veteran factors").add("VeteranSight")
	generalConfig.get("General").get("Veteran factors").add("VeteranArmor")
	generalConfig.get("General").get("Veteran factors").add("VeteranROF")
	generalConfig.get("General").get("Veteran factors").add("VeteranCap")
	generalConfig.get("General").get("Veteran factors").add("InitialVeteran")
	generalConfig.get("General").add("Repair and refit")
	generalConfig.get("General").get("Repair and refit").add("RefundPercent")
	generalConfig.get("General").get("Repair and refit").add("ReloadRate")
	generalConfig.get("General").get("Repair and refit").add("RepairPercent")
	generalConfig.get("General").get("Repair and refit").add("RepairRate")
	generalConfig.get("General").get("Repair and refit").add("RepairStep")
	generalConfig.get("General").get("Repair and refit").add("URepairRate")
	generalConfig.get("General").get("Repair and refit").add("IRepairRate")
	generalConfig.get("General").get("Repair and refit").add("IRepairStep")
	generalConfig.get("General").get("Repair and refit").add("TiberiumHeal")
	generalConfig.get("General").get("Repair and refit").add("SelfHealInfantryFrames")
	generalConfig.get("General").get("Repair and refit").add("SelfHealInfantryAmount")
	generalConfig.get("General").get("Repair and refit").add("SelfHealUnitFrames")
	generalConfig.get("General").get("Repair and refit").add("SelfHealUnitAmount")
	generalConfig.get("General").add("Income and production")
	generalConfig.get("General").get("Income and production").add("BuildSpeed")
	generalConfig.get("General").get("Income and production").add("BuildupTime")
	generalConfig.get("General").get("Income and production").add("GrowthRate")
	generalConfig.get("General").get("Income and production").add("SurvivorRate")
	generalConfig.get("General").get("Income and production").add("AlliedSurvivorDivisor")
	generalConfig.get("General").get("Income and production").add("SovietSurvivorDivisor")
	generalConfig.get("General").get("Income and production").add("PlacementDelay")
	generalConfig.get("General").add("Messile settings")
	generalConfig.get("General").get("Messile settings").add("MissileSafetyAltitude")
	generalConfig.get("General").add("Battle field settings")
	generalConfig.get("General").get("Battle field settings").add("FogOfWar")
	generalConfig.get("General").get("Battle field settings").add("Visceroids")
	generalConfig.get("General").get("Battle field settings").add("Meteorites")
	generalConfig.get("General").get("Battle field settings").add("CrewEscape")
	generalConfig.get("General").get("Battle field settings").add("CameraRange")
	generalConfig.get("General").get("Battle field settings").add("FineDiffControl")
	generalConfig.get("General").get("Battle field settings").add("Pilot")
	generalConfig.get("General").get("Battle field settings").add("AlliedCrew")
	generalConfig.get("General").get("Battle field settings").add("SovietCrew")
	generalConfig.get("General").get("Battle field settings").add("ThirdCrew")
	generalConfig.get("General").get("Battle field settings").add("Technician")
	generalConfig.get("General").get("Battle field settings").add("Engineer")
	generalConfig.get("General").get("Battle field settings").add("PParatrooper")
	generalConfig.get("General").add("Reinforcement/Chrono stuff")
	generalConfig.get("General").get("Reinforcement/Chrono stuff").add("ChronoDelay")
	generalConfig.get("General").get("Reinforcement/Chrono stuff").add("ChronoReinfDelay")
	generalConfig.get("General").get("Reinforcement/Chrono stuff").add("ChronoDistanceFactor")
	generalConfig.get("General").get("Reinforcement/Chrono stuff").add("ChronoTrigger")
	generalConfig.get("General").get("Reinforcement/Chrono stuff").add("ChronoMinimumDelay")
	generalConfig.get("General").get("Reinforcement/Chrono stuff").add("ChronoRangeMinimum")
	generalConfig.get("General").add("American Paradrop")
	generalConfig.get("General").get("American Paradrop").add("AmerParaDropInf")
	generalConfig.get("General").get("American Paradrop").add("AmerParaDropNum")
	generalConfig.get("General").get("American Paradrop").add("AllyParaDropInf")
	generalConfig.get("General").get("American Paradrop").add("AllyParaDropNum")
	generalConfig.get("General").get("American Paradrop").add("SovParaDropInf")
	generalConfig.get("General").get("American Paradrop").add("SovParaDropNum")
	generalConfig.get("General").get("American Paradrop").add("YuriParaDropInf")
	generalConfig.get("General").get("American Paradrop").add("YuriParaDropNum")
	generalConfig.get("General").add("Spy stuff")
	generalConfig.get("General").get("Spy stuff").add("SpyPowerBlackout")
	generalConfig.get("General").get("Spy stuff").add("SpyMoneyStealPercent")
	generalConfig.get("General").add("Environtment")
	generalConfig.get("General").get("Environtment").add("TreeStrength")
	generalConfig.get("General").get("Environtment").add("TrackedUphill")
	generalConfig.get("General").get("Environtment").add("TrackedDownhill")
	generalConfig.get("General").get("Environtment").add("WheeledUphill")
	generalConfig.get("General").get("Environtment").add("WheeledDownhill")
	generalConfig.get("General").get("Environtment").add("AttackingAircraftSightRange")
	generalConfig.get("General").get("Environtment").add("BlendedFog")
	generalConfig.get("General").get("Environtment").add("CliffBackImpassability")
	generalConfig.get("General").get("Environtment").add("IceCrackingWeight")
	generalConfig.get("General").get("Environtment").add("IceBreakingWeight")
	generalConfig.get("General").get("Environtment").add("ShipSinkingWeight")
	generalConfig.get("General").get("Environtment").add("TreeFlammability")
	generalConfig.get("General").get("Environtment").add("CraterLevel")
	generalConfig.add("CrateRules")
	generalConfig.get("CrateRules").add("Crate")
	generalConfig.get("CrateRules").get("Crate").add("CrateMaximum")
	generalConfig.get("CrateRules").get("Crate").add("CrateMinimum")
	generalConfig.get("CrateRules").get("Crate").add("CrateRadius")
	generalConfig.get("CrateRules").get("Crate").add("CrateRegen")
	generalConfig.get("CrateRules").get("Crate").add("SilverCrate")
	generalConfig.get("CrateRules").get("Crate").add("SoloCrateMoney")
	generalConfig.add("CombatDamage")
	generalConfig.get("CombatDamage").add("General")
	generalConfig.get("CombatDamage").get("General").add("MaxDamage")
	generalConfig.get("CombatDamage").get("General").add("MinDamage")
	generalConfig.get("CombatDamage").get("General").add("PlayerAutoCrush")
	generalConfig.get("CombatDamage").get("General").add("PlayerReturnFire")
	generalConfig.get("CombatDamage").get("General").add("PlayerScatter")
	generalConfig.get("CombatDamage").get("General").add("Incoming")
	generalConfig.get("CombatDamage").get("General").add("AmmoCrateDamage")
	generalConfig.get("CombatDamage").get("General").add("IonCannonDamage")
	generalConfig.get("CombatDamage").get("General").add("HarvesterImmune")
	generalConfig.get("CombatDamage").get("General").add("DestroyableBridges")
	generalConfig.get("CombatDamage").get("General").add("TiberiumExplosive")
	generalConfig.get("CombatDamage").get("General").add("TiberiumExplosionDamage")
	generalConfig.get("CombatDamage").get("General").add("TiberiumStrength")
	generalConfig.get("CombatDamage").get("General").add("AtomDamage")
	generalConfig.get("CombatDamage").get("General").add("BallisticScatter")
	generalConfig.get("CombatDamage").get("General").add("BridgeStrength")
	generalConfig.get("CombatDamage").add("Crazy Ivan stuff")
	generalConfig.get("CombatDamage").get("Crazy Ivan stuff").add("IvanDamage")
	generalConfig.get("CombatDamage").get("Crazy Ivan stuff").add("IvanTimedDelay")
	generalConfig.get("CombatDamage").add("Urban combat")
	generalConfig.get("CombatDamage").get("Urban combat").add("OccupyDamageMultiplier")
	generalConfig.get("CombatDamage").get("Urban combat").add("OccupyROFMultiplier")
	generalConfig.get("CombatDamage").get("Urban combat").add("OccupyWeaponRange")
	generalConfig.add("Radiation")
	generalConfig.get("Radiation").add("Ratiation")
	generalConfig.get("Radiation").get("Ratiation").add("RadDurationMultiple")
	generalConfig.get("Radiation").get("Ratiation").add("RadApplicationDelay")
	generalConfig.get("Radiation").get("Ratiation").add("RadLevelMax")
	generalConfig.get("Radiation").get("Ratiation").add("RadLevelDelay")
	generalConfig.get("Radiation").get("Ratiation").add("RadLightDelay")
	generalConfig.get("Radiation").get("Ratiation").add("RadLevelFactor")
	generalConfig.get("Radiation").get("Ratiation").add("RadLightFactor")
	generalConfig.get("Radiation").get("Ratiation").add("RadTintFactor")
	generalConfig.get("Radiation").get("Ratiation").add("RadColor")
	generalConfig.add("MultiplayerDialogSettings")
	generalConfig.get("MultiplayerDialogSettings").add("Settings")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("MinMoney")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("MaxMoney")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("Money")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("MoneyIncrement")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("MinUnitCount")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("MaxUnitCount")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("UnitCount")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("GameSpeed")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("BridgeDestruction")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("TiberiumGrows")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("Crates")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("ShortGame")
	generalConfig.get("MultiplayerDialogSettings").get("Settings").add("FogOfWar")
	generalConfig.add("AI")
	generalConfig.get("AI").add("General")
	generalConfig.get("AI").get("General").add("AttackInterval")
	generalConfig.get("AI").get("General").add("AttackDelay")
	generalConfig.get("AI").get("General").add("PatrolScan")
	generalConfig.get("AI").get("General").add("CreditReserve")
	generalConfig.get("AI").get("General").add("PathDelay")
	generalConfig.get("AI").get("General").add("BlockagePathDelay")
	generalConfig.get("AI").add("Building")
	generalConfig.get("AI").get("Building").add("InfantryReserve")
	generalConfig.get("AI").get("Building").add("InfantryBaseMult")
	generalConfig.get("AI").get("Building").add("PowerSurplus")
	generalConfig.get("AI").get("Building").add("BaseSizeAdd")
	generalConfig.get("AI").get("Building").add("RefineryRatio")
	generalConfig.get("AI").get("Building").add("RefineryLimit")
	generalConfig.get("AI").get("Building").add("BarracksRatio")
	generalConfig.get("AI").get("Building").add("BarracksLimit")
	generalConfig.get("AI").get("Building").add("WarRatio")
	generalConfig.get("AI").get("Building").add("WarLimit")
	generalConfig.get("AI").get("Building").add("DefenseRatio")
	generalConfig.get("AI").get("Building").add("DefenseLimit")
	generalConfig.get("AI").get("Building").add("AARatio")
	generalConfig.get("AI").get("Building").add("AALimit")
	generalConfig.get("AI").get("Building").add("PowerEmergency")
	generalConfig.get("AI").get("Building").add("AIBaseSpacing")
	generalConfig.show()
	
	infantryConfig = Configuration(tabInfantry)
	allInfantries = ["E1","ADOG","ENGINEER","GGI","JUMPJET","SPY","GHOST","TANY","CLEG",\
		"CCOMAND","PTROOP","SNIPE","E2","DOG","FLAKT","SENGINEER","SHK","IVAN","BORIS","CIVAN",\
		"LUNR","TERROR","DESO","INIT","YADOG","SLAV","YENGINEER","BRUTE","VIRUS","YURI","YURIPR"]
	for infantry in allInfantries:
		infantryConfig.add(infantry)
		infantryConfig.get(infantry).add("Basic")
		infantryConfig.get(infantry).get("Basic").add("Name")
		infantryConfig.get(infantry).get("Basic").add("Owner")
		infantryConfig.get(infantry).get("Basic").add("Cost")
		infantryConfig.get(infantry).get("Basic").add("TechLevel")
		infantryConfig.get(infantry).add("Battle")
		infantryConfig.get(infantry).get("Battle").add("Occupier")
		infantryConfig.get(infantry).get("Battle").add("Strength")
		infantryConfig.get(infantry).get("Battle").add("Sight")
		infantryConfig.get(infantry).get("Battle").add("Speed")
		infantryConfig.get(infantry).add("Weapon")
		infantryConfig.get(infantry).get("Weapon").add("Primary")
		infantryConfig.get(infantry).get("Weapon").add("Secondary")
		infantryConfig.get(infantry).get("Weapon").add("ElitePrimary")
		infantryConfig.get(infantry).get("Weapon").add("EliteSecondary")
		infantryConfig.get(infantry).get("Weapon").add("OccupyWeapon")
		infantryConfig.get(infantry).get("Weapon").add("EliteOccupyWeapon")
		infantryConfig.get(infantry).get("Weapon").add("OpenTransportWeapon")
		infantryConfig.get(infantry).get("Weapon").add("Armor")
		infantryConfig.get(infantry).get("Weapon").add("VeteranAbilities")
		infantryConfig.get(infantry).get("Weapon").add("EliteAbilities")
		infantryConfig.get(infantry).get("Weapon").add("Agent")
		infantryConfig.get(infantry).get("Weapon").add("Infiltrate")
		infantryConfig.get(infantry).get("Weapon").add("CanDisguise")
		infantryConfig.get(infantry).get("Weapon").add("C4")
		infantryConfig.get(infantry).get("Weapon").add("Explodes")
		infantryConfig.get(infantry).get("Weapon").add("DeathWeapon")
		infantryConfig.get(infantry).add("Control")
		infantryConfig.get(infantry).get("Control").add("IsSelectableCombatant")
		infantryConfig.get(infantry).get("Control").add("DetectDisguise")
		infantryConfig.get(infantry).get("Control").add("CanPassiveAquire")
		infantryConfig.get(infantry).get("Control").add("BuildLimit")
		infantryConfig.get(infantry).get("Control").add("Teleporter")
		infantryConfig.get(infantry).get("Control").add("Prerequisite")
		infantryConfig.get(infantry).add("Immunity")
		infantryConfig.get(infantry).get("Immunity").add("ImmuneToVeins")
		infantryConfig.get(infantry).get("Immunity").add("ImmuneToPsionics")
		infantryConfig.get(infantry).get("Immunity").add("ImmuneToRadiation")
		infantryConfig.get(infantry).get("Immunity").add("TiberiumProof")
		infantryConfig.get(infantry).get("Immunity").add("Bombable")
		infantryConfig.get(infantry).get("Immunity").add("Crushable")
		infantryConfig.get(infantry).get("Immunity").add("DeployedCrushable")
		infantryConfig.get(infantry).get("Immunity").add("SelfHealing")
	infantryConfig.show()
	
	vehicleConfig = Configuration(tabVehicle)
	allVehicles = ["MTNK","FV","MGTK","SREF","BFRT","AMCV","CMON","CMIN","ROBO","TNKD","HOWI",\
		"DRON","HTK","HTNK","V3","APOC","SMCV","HORV","HARV","UTNK","TTNK","DTRUCK",\
		"LTNK","YTNK","TELE","MIND","CAOS","PCV","SMON","SMIN"]
	for vehicle in allVehicles:
		vehicleConfig.add(vehicle)
		vehicleConfig.get(vehicle).add("Basic")
		vehicleConfig.get(vehicle).get("Basic").add("Name")
		vehicleConfig.get(vehicle).get("Basic").add("Owner")
		vehicleConfig.get(vehicle).get("Basic").add("Cost")
		vehicleConfig.get(vehicle).get("Basic").add("TechLevel")
		vehicleConfig.get(vehicle).add("Battle")
		vehicleConfig.get(vehicle).get("Battle").add("Strength")
		vehicleConfig.get(vehicle).get("Battle").add("Sight")
		vehicleConfig.get(vehicle).get("Battle").add("Speed")
		vehicleConfig.get(vehicle).add("Weapon")
		vehicleConfig.get(vehicle).get("Weapon").add("Primary")
		vehicleConfig.get(vehicle).get("Weapon").add("Secondary")
		vehicleConfig.get(vehicle).get("Weapon").add("ElitePrimary")
		vehicleConfig.get(vehicle).get("Weapon").add("EliteSecondary")
		vehicleConfig.get(vehicle).get("Weapon").add("Armor")
		vehicleConfig.get(vehicle).get("Weapon").add("VeteranAbilities")
		vehicleConfig.get(vehicle).get("Weapon").add("EliteAbilities")
		vehicleConfig.get(vehicle).get("Weapon").add("Explodes")
		vehicleConfig.get(vehicle).get("Weapon").add("DeathWeapon")
		vehicleConfig.get(vehicle).get("Weapon").add("Crusher")
		vehicleConfig.get(vehicle).get("Weapon").add("CanDisguise")
		vehicleConfig.get(vehicle).get("Weapon").add("OmniCrusher")
		vehicleConfig.get(vehicle).add("Control")
		vehicleConfig.get(vehicle).get("Control").add("IsSelectableCombatant")
		vehicleConfig.get(vehicle).get("Control").add("DetectDisguise")
		vehicleConfig.get(vehicle).get("Control").add("CanPassiveAquire")
		vehicleConfig.get(vehicle).get("Control").add("BuildLimit")
		vehicleConfig.get(vehicle).get("Control").add("Teleporter")
		vehicleConfig.get(vehicle).get("Control").add("Prerequisite")
		vehicleConfig.get(vehicle).get("Control").add("Accelerates")
		vehicleConfig.get(vehicle).get("Control").add("DeploysInto")
		vehicleConfig.get(vehicle).get("Control").add("Naval")
		vehicleConfig.get(vehicle).add("Immunity")
		vehicleConfig.get(vehicle).get("Immunity").add("ImmuneToVeins")
		vehicleConfig.get(vehicle).get("Immunity").add("ImmuneToPsionics")
		vehicleConfig.get(vehicle).get("Immunity").add("ImmuneToRadiation")
		vehicleConfig.get(vehicle).get("Immunity").add("TiberiumProof")
		vehicleConfig.get(vehicle).get("Immunity").add("OmniCrushResistant")
		vehicleConfig.get(vehicle).get("Immunity").add("Bombable")
		vehicleConfig.get(vehicle).get("Immunity").add("Crushable")
		vehicleConfig.get(vehicle).get("Immunity").add("SelfHealing")
		vehicleConfig.get(vehicle).add("Carrier")
		vehicleConfig.get(vehicle).get("Carrier").add("Passengers")
		vehicleConfig.get(vehicle).get("Carrier").add("AirRangeBonus")
	vehicleConfig.show()
	
	navalConfig = Configuration(tabNaval)
	allNavals = ["LCRF","DEST","DLPH","AEGIS","CARRIER","SAPC","HYD","SUB","SQD","DRED","YHVR","BSUB"]
	for naval in allNavals:
		navalConfig.add(naval)
		navalConfig.get(naval).add("Basic")
		navalConfig.get(naval).get("Basic").add("Name")
		navalConfig.get(naval).get("Basic").add("Owner")
		navalConfig.get(naval).get("Basic").add("Cost")
		navalConfig.get(naval).get("Basic").add("TechLevel")
		navalConfig.get(naval).add("Battle")
		navalConfig.get(naval).get("Battle").add("Strength")
		navalConfig.get(naval).get("Battle").add("Sight")
		navalConfig.get(naval).get("Battle").add("Speed")
		navalConfig.get(naval).add("Weapon")
		navalConfig.get(naval).get("Weapon").add("Primary")
		navalConfig.get(naval).get("Weapon").add("Secondary")
		navalConfig.get(naval).get("Weapon").add("ElitePrimary")
		navalConfig.get(naval).get("Weapon").add("EliteSecondary")
		navalConfig.get(naval).get("Weapon").add("Armor")
		navalConfig.get(naval).get("Weapon").add("VeteranAbilities")
		navalConfig.get(naval).get("Weapon").add("EliteAbilities")
		navalConfig.get(naval).get("Weapon").add("Explodes")
		navalConfig.get(naval).get("Weapon").add("DeathWeapon")
		navalConfig.get(naval).get("Weapon").add("Crusher")
		navalConfig.get(naval).get("Weapon").add("CanDisguise")
		navalConfig.get(naval).get("Weapon").add("OmniCrusher")
		navalConfig.get(naval).add("Control")
		navalConfig.get(naval).get("Control").add("IsSelectableCombatant")
		navalConfig.get(naval).get("Control").add("DetectDisguise")
		navalConfig.get(naval).get("Control").add("CanPassiveAquire")
		navalConfig.get(naval).get("Control").add("BuildLimit")
		navalConfig.get(naval).get("Control").add("Teleporter")
		navalConfig.get(naval).get("Control").add("Prerequisite")
		navalConfig.get(naval).get("Control").add("Accelerates")
		navalConfig.get(naval).get("Control").add("DeploysInto")
		navalConfig.get(naval).get("Control").add("Naval")
		navalConfig.get(naval).add("Immunity")
		navalConfig.get(naval).get("Immunity").add("ImmuneToVeins")
		navalConfig.get(naval).get("Immunity").add("ImmuneToPsionics")
		navalConfig.get(naval).get("Immunity").add("ImmuneToRadiation")
		navalConfig.get(naval).get("Immunity").add("TiberiumProof")
		navalConfig.get(naval).get("Immunity").add("OmniCrushResistant")
		navalConfig.get(naval).get("Immunity").add("Bombable")
		navalConfig.get(naval).get("Immunity").add("Crushable")
		navalConfig.get(naval).get("Immunity").add("SelfHealing")
		navalConfig.get(naval).add("Carrier")
		navalConfig.get(naval).get("Carrier").add("Passengers")
		navalConfig.get(naval).get("Carrier").add("AirRangeBonus")
	navalConfig.show()
	
	airforceConfig = Configuration(tabAirforce)
	allAirforces = ["SHAD","ORCA","ASW","HORNET","BEAG","HIND","SCHP","ZEP","V3ROCKET","DMISL",\
		"CMISL","DISK","PDPLANE","CARGOPLANE"]
	for airforce in allAirforces:
		airforceConfig.add(airforce)
		airforceConfig.get(airforce).add("Basic")
		airforceConfig.get(airforce).get("Basic").add("Name")
		airforceConfig.get(airforce).get("Basic").add("Owner")
		airforceConfig.get(airforce).get("Basic").add("Cost")
		airforceConfig.get(airforce).get("Basic").add("TechLevel")
		airforceConfig.get(airforce).add("Battle")
		airforceConfig.get(airforce).get("Battle").add("Strength")
		airforceConfig.get(airforce).get("Battle").add("Sight")
		airforceConfig.get(airforce).get("Battle").add("Speed")
		airforceConfig.get(airforce).add("Weapon")
		airforceConfig.get(airforce).get("Weapon").add("Primary")
		airforceConfig.get(airforce).get("Weapon").add("Secondary")
		airforceConfig.get(airforce).get("Weapon").add("ElitePrimary")
		airforceConfig.get(airforce).get("Weapon").add("EliteSecondary")
		airforceConfig.get(airforce).get("Weapon").add("Armor")
		airforceConfig.get(airforce).get("Weapon").add("VeteranAbilities")
		airforceConfig.get(airforce).get("Weapon").add("EliteAbilities")
		airforceConfig.get(airforce).get("Weapon").add("Explodes")
		airforceConfig.get(airforce).get("Weapon").add("DeathWeapon")
		airforceConfig.get(airforce).get("Weapon").add("Crusher")
		airforceConfig.get(airforce).get("Weapon").add("CanDisguise")
		airforceConfig.get(airforce).get("Weapon").add("OmniCrusher")
		airforceConfig.get(airforce).add("Control")
		airforceConfig.get(airforce).get("Control").add("IsSelectableCombatant")
		airforceConfig.get(airforce).get("Control").add("DetectDisguise")
		airforceConfig.get(airforce).get("Control").add("CanPassiveAquire")
		airforceConfig.get(airforce).get("Control").add("BuildLimit")
		airforceConfig.get(airforce).get("Control").add("Teleporter")
		airforceConfig.get(airforce).get("Control").add("Prerequisite")
		airforceConfig.get(airforce).get("Control").add("Accelerates")
		airforceConfig.get(airforce).get("Control").add("DeploysInto")
		airforceConfig.get(airforce).get("Control").add("Airforce")
		airforceConfig.get(airforce).add("Immunity")
		airforceConfig.get(airforce).get("Immunity").add("ImmuneToVeins")
		airforceConfig.get(airforce).get("Immunity").add("ImmuneToPsionics")
		airforceConfig.get(airforce).get("Immunity").add("ImmuneToRadiation")
		airforceConfig.get(airforce).get("Immunity").add("TiberiumProof")
		airforceConfig.get(airforce).get("Immunity").add("OmniCrushResistant")
		airforceConfig.get(airforce).get("Immunity").add("Bombable")
		airforceConfig.get(airforce).get("Immunity").add("Crushable")
		airforceConfig.get(airforce).get("Immunity").add("SelfHealing")
		airforceConfig.get(airforce).add("Carrier")
		airforceConfig.get(airforce).get("Carrier").add("Passengers")
		airforceConfig.get(airforce).get("Carrier").add("AirRangeBonus")
	airforceConfig.show()
	
	buildingConfig = Configuration(tabBuilding)
	allBuildings = ["GACNST","GAPOWR","GAPILE","GAREFN","GAWEAP","GAAIRC","GAYARD","GADEPT","GATECH",\
		"GAOREP","GAROBO","NACNST","NAPOWR","NAHAND","NAREFN","NAWEAP","NARADR","NAYARD","NADEPT",\
		"NATECH","NANRCT","NAINDP","YACNST","YAPOWR","YABRCK","YACOMD","YAREFN","YAWEAP","NAPSIS",\
		"YAYARD","YADEPT","YATECH","YAGRND","NACLON","CAAIRP","CAOILD","CAMACH","CATHOSP","CAHOSP"]
	for building in allBuildings:
		buildingConfig.add(building)
		buildingConfig.get(building).add("Basic")
		buildingConfig.get(building).get("Basic").add("Name")
		buildingConfig.get(building).get("Basic").add("Owner")
		buildingConfig.get(building).get("Basic").add("Cost")
		buildingConfig.get(building).get("Basic").add("Strength")
		buildingConfig.get(building).get("Basic").add("TechLevel")
		buildingConfig.get(building).get("Basic").add("Power")
		buildingConfig.get(building).get("Basic").add("Powered")
		buildingConfig.get(building).get("Basic").add("Prerequisite")
		buildingConfig.get(building).get("Basic").add("Unsellable")
		buildingConfig.get(building).add("Weapon")
		buildingConfig.get(building).get("Weapon").add("Armor")
		buildingConfig.get(building).get("Weapon").add("Sight")
		buildingConfig.get(building).get("Weapon").add("DeathWeapon")
		buildingConfig.get(building).get("Weapon").add("FactoryPlant")
		buildingConfig.get(building).get("Weapon").add("InfantryCostBonus")
		buildingConfig.get(building).get("Weapon").add("UnitsCostBonus")
		buildingConfig.get(building).get("Weapon").add("AircraftCostBonus")
		buildingConfig.get(building).get("Weapon").add("BuildingsCostBonus")
		buildingConfig.get(building).get("Weapon").add("DefensesCostBonus")
		buildingConfig.get(building).get("Weapon").add("PsychicDetectionRadius")
		buildingConfig.get(building).get("Weapon").add("DetectDisguise")
		buildingConfig.get(building).get("Weapon").add("DetectDisguiseRange")
		buildingConfig.get(building).get("Weapon").add("Grinding")
		buildingConfig.get(building).get("Weapon").add("Cloning")
		buildingConfig.get(building).get("Weapon").add("InfantryGainSelfHeal")
		buildingConfig.get(building).get("Weapon").add("UnitsGainSelfHeal")
		buildingConfig.get(building).add("Control")
		buildingConfig.get(building).get("Control").add("UndeploysInto")
		buildingConfig.get(building).get("Control").add("Capturable")
		buildingConfig.get(building).get("Control").add("AIBuildThis")
		buildingConfig.get(building).get("Control").add("WaterBound")
		buildingConfig.get(building).get("Control").add("BuildLimit")
		buildingConfig.get(building).get("Control").add("Repairable")
		buildingConfig.get(building).get("Control").add("InfantryAbsorb")
		buildingConfig.get(building).get("Control").add("UnitAbsorb")
		buildingConfig.get(building).get("Control").add("Passengers")
		buildingConfig.get(building).add("Immunity")
		buildingConfig.get(building).get("Immunity").add("ImmuneToPsionics")
		buildingConfig.get(building).get("Immunity").add("Spyable")
		buildingConfig.get(building).get("Immunity").add("UnitRepair")
	buildingConfig.show()
	
	defenceConfig = Configuration(tabDefence)
	allDefences = ["GAWALL","GAPILL","NASAM","ATESLA","GASPYSAT","GAGAP","GACSPH","GAWEAT","AMRADR",\
		"GTGCAN","NAWALL","NALASR","NAFLAK","TESLA","NABNKR","NABNKR","NAIRON","NAMISL","GAFWLL",\
		"YAGGUN","YAPSYT","NATBNK","YAGNTC","YAPPET"]
	for defence in allDefences:
		defenceConfig.add(defence)
		defenceConfig.get(defence).add("Basic")
		defenceConfig.get(defence).get("Basic").add("Name")
		defenceConfig.get(defence).get("Basic").add("Owner")
		defenceConfig.get(defence).get("Basic").add("Cost")
		defenceConfig.get(defence).get("Basic").add("Strength")
		defenceConfig.get(defence).get("Basic").add("TechLevel")
		defenceConfig.get(defence).get("Basic").add("Power")
		defenceConfig.get(defence).get("Basic").add("Powered")
		defenceConfig.get(defence).get("Basic").add("Prerequisite")
		defenceConfig.get(defence).add("Weapon")
		defenceConfig.get(defence).get("Weapon").add("Armor")
		defenceConfig.get(defence).get("Weapon").add("Sight")
		defenceConfig.get(defence).get("Weapon").add("TurretAnim")
		defenceConfig.get(defence).get("Weapon").add("Primary")
		defenceConfig.get(defence).get("Weapon").add("Secondary")
		defenceConfig.get(defence).get("Weapon").add("SpySat")
		defenceConfig.get(defence).get("Weapon").add("DeathWeapon")
		defenceConfig.get(defence).get("Weapon").add("DetectDisguise")
		defenceConfig.get(defence).add("Control")
		defenceConfig.get(defence).get("Control").add("UndeploysInto")
		defenceConfig.get(defence).get("Control").add("Capturable")
		defenceConfig.get(defence).get("Control").add("AIBuildThis")
		defenceConfig.get(defence).get("Control").add("WaterBound")
		defenceConfig.get(defence).get("Control").add("BuildLimit")
		defenceConfig.get(defence).get("Control").add("Repairable")
		defenceConfig.get(defence).add("Immunity")
		defenceConfig.get(defence).get("Immunity").add("ImmuneToPsionics")
		defenceConfig.get(defence).get("Immunity").add("Spyable")
		defenceConfig.get(defence).get("Immunity").add("UnitRepair")
	defenceConfig.show()
	
	root.mainloop()
