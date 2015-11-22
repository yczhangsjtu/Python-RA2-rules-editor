from Tkinter import *
import tkFileDialog

COMMENT = 0
RULE = 1
RULESETNAME = 2

discriptions = {
	"E1":"American Soldier", "ADOG":"Allied Dog", "ENGINEER":"Allied Engineer",
	"GGI":"Soldier with Heavy Equipment", "JUMPJET":"Flying Rocket Soldier",
	"SPY":"Spy", "GHOST":"Nava Seal", "TANY":"Tanya", "CLEG":"Chrono Legion",
	"CCOMAND":"Chrono Attacker (Special)", "PTROOP":"Psi-Corp Trooper (Special)",
	"SNIPE":"Sniper", "E2":"Soviet Soldier", "DOG":"Soviet Dog", "FLAKT":"Anti-air soldier",
	"SHK":"Electric Soldier", "IVAN":"Crazy Ivan", "BORIS":"Elite Soldier", "CIVAN":"Chrono Ivan", 
	"LUNR": "Lunar Soldier", "TERROR":"Terrorist", "DESO":"Radiation Soldier", "INIT":"Yuri Soldier",
	"YENGINEER":"Yuri Engineer", "BRUTE":"Violent Man", "VIRUS":"Virus Sniper", "YURI":"Yuri",
	"YURIPR":"Yuri X", "MTNK":"Grizz Tank", "FV":"Multi-Functional Vehicle", "MGTK":"Mirage Tank",
	"SREF":"Prism Tank", "BFRT":"Battle Fortress", "AMCV":"Allied Mobile Construction Vehicle",
	"CMON":"Chrono Miner", "CMIN":"Chrono Miner", "ROBO":"Robot Tank", "TNKD":"Tank Killer",
	"HOWI":"Howitzer (Special)", "DRON":"Terrifying Robot", "HTK":"Anti-Air Flak Vehicle",
	"HTNK":"Heavy Tank (Rhinocero Tank)", "V3":"V3 Vehicle", "APOC":"TianQi Tank",
	"SMCV":"Soviet Mobile Construction Vehicle", "HORV":"Armed Miner", "HARV":"Armed Miner",
	"UTNK":"UTNK (Special)", "TTNK":"Magnetic Tank", "DTRUCK":"Explosive Truck",
	"LTNK":"Tornado Tank", "YTNK":"Gattle Tank", "TELE":"Mag-Electric Tank",
	"MIND":"Mind Control Vehicle", "CAOS":"Soul Attacking Vehicle","SENGINEER":"Soviet Engineer",
	"PCV":"Yuri Mobile Construction Vehicle", "SMON":"Slave Miner", "SMIN":"Slave Miner",
	"LCRF":"Landing Craft", "DEST":"Destroyer", "DLPH":"Dophin", "AEGIS":"Aegis Cruiser",
	"CARRIER":"Aircraft Carrier", "SAPC":"Armored Transporter", "HYD":"Sea Scorpion",
	"SUB":"Attacking Submarine", "SQD":"Giant Cuttlefish", "DRED":"Fearless Battleship",
	"YHVR":"Yuri Transporter", "BSUB":"Yuri Boomer", "SHAD":"BlackHawk Helicopter",
	"ORCA":"Intruder Fighter Plane", "ASW":"Osprey (Special)", "HORNET":"Hornet (Special)",
	"BEAG":"Black Eagle", "HIND":"Soviet Helicopter (Special)", "SCHP":"Armed Helicopter",
	"ZEP":"Kirov Airship", "V3ROCKET":"V3 Rocket (not vehicle)", "DMISL":"Fearless Missile",
	"CMISL":"Yuri Submarine Missile", "DISK":"Floating Disk", "PDPLANE":"Paratrooper Plane",
	"CARGOPLANE":"Paratrooper Plane", "GACNST":"Allied Construction Yard",
	"GAPOWR":"Allied Power Plant", "GAPILE":"Allied Infantry Trainer",
	"GAREFN":"Allied Ore Refinery", "GAWEAP":"Allied War Factory",
	"GAAIRC":"Allied Airforce Command Headquarters", "GAYARD":"Allied Shipyard",
	"GADEPT":"Allied Repair Yard", "GATECH":"Allied Battle Lab", "GAOREP":"Allied Ore Processor",
	"GAROBO":"Allied Robot Control Center", "NACNST":"Soviet Construction Yard",
	"NAPOWR":"Soviet Power Plant", "NAHAND":"Soviet Infantry Trainer", "NAREFN":"Soviet Ore Refinery",
	"NAWEAP":"Soviet War Factory", "NARADR":"Soviet Radar Tower", "NAYARD":"Soviet Shipyard",
	"NADEPT":"Soviet Repair Yard", "NATECH":"Soviet Battle Lab", "NANRCT":"Soviet Nuclear Reactor",
	"NAINDP":"Soviet Industrial Plant","YACNST":"Yuri Construction Yard", "YAPOWR":"Yuri Bio Reactor",
	"YABRCK":"Yuri Infantry Trainer", "YACOMD":"Yuri Command Center (Special)",
	"YAREFN":"Yuri Ore Refinery", "YAWEAP":"Yuri War Factory", "NAPSIS":"Yuri Psychic Sensor",
	"YAYARD":"Yuri Shipyard", "YADEPT":"Yuri Service Depot", "YATECH":"Yuri Battle Lab",
	"YAGRND":"Yuri Grinder", "NACLON":"Yuri Cloning Vats", "CAAIRP":"Tech Airport",
	"CAOILD":"Tech Oil Derrick", "CAMACH":"Tech Machine Shop", "CATHOSP":"Tech Hospital",
	"CAHOSP":"Old Civilian Hospital",  "GAWALL":"Allied Wall", "GAPILL":"Allied Pill Box",
	"NASAM":"Allied Patriot Missile", "ATESLA":"Allied Prism Tower", "GASPYSAT":"Allied Spy Satellite",
	"GAGAP":"Allied Gap Generator", "GACSPH":"Allied Chrono Sphere",
	"GAWEAT":"Allied Weather Controller", "AMRADR":"Allied American Airforce Command Headquarters",
	"GTGCAN":"Allied Giant Cannon", "NAWALL":"Soviet Wall", "NALASR":"Soviet Sentry Gun",
	"NAFLAK":"Anti-Air Artillery", "TESLA":"Soviet Mega-Electric Coil", "NABNKR":"Soviet Battle Bunker",
	"NAIRON":"Soviet Iron Curtain Device", "NAMISL":"Soviet Nuclear Missile Silo",
	"GAFWLL":"Yuri Citadel Wall", "YAGGUN":"Yuri Gattling Cannon", "YAPSYT":"Yuri Psychic Tower",
	"NATBNK":"Yuri Tank Bunker", "YAGNTC":"Yuri Genetic Mutator Device", "YAPPET":"Yuri Puppet Master"
}
attackTargets = {"0":"","1":"any enemy","2":"enemy building","3":"mine units","4":"infantry","5":"vehicle",\
	"6":"factory","7":"defence","8":"threats to base","9":"power plant","10":"civilian building",\
	"11":"civilian tech building"}
afterUnload = {"0":"","1":"","2":"and dismiss unloaded troop","3":"and dismiss transporter",\
	"4":"and dismiss all"}
getintoState = {"5":"Stay","6":"Stay forever","10":"Start mining","11":"Guard","15":"Search for enemy"}
triggerConditions = {"0":"target enemy units satisfies ","1":"my units satisfy ","2":"enemy power is yellow ",
	"3":"enemy power is red ","4":"target enemy money is larger than ","5":"my curtain is ready ",
	"6":"my chrono transport is ready ","7":"civilian satisfies "}
comparator = {"0":"<","1":"<=","2":"=","3":">=","4":">","5":"!="}
def describeScript(a,b):
	action = ""
	target = ""
	if a == "0":
		action = "Attack nearest "
		target = attackTargets[b]
	elif a == "5":
		action = "Wait "
		target = "for %d seconds"%(int(b)*6)
	elif a == "6":
		action = "Goto line "
		target = b
	elif a == "8":
		action = "Unload "
		target = afterUnload[b]
	elif a == "9":
		action = "Deploy"
	elif a == "11":
		action = getintoState[b]
	elif a == "14":
		action = "Load"
	elif a == "43":
		action = "Wait until all loaded"
	elif a == "46":
		action = "Attack enemy building "
		target = b
	elif a == "47":
		action = "Move to enemy building "
		target = b
	elif a == "49":
		action = "Finished"
	elif a == "53":
		action = "Gather nearby enemy base"
	elif a == "54":
		action = "Gather nearby self base"
	elif a == "55":
		action = "Ask for curtain"
	elif a == "56":
		action = "Ask to be chrono transported to enemy building "
		target = b
	elif a == "57":
		action = "Ask to be chrono transported to "
		target = attackTargets[b]
	elif a == "58":
		action = "Move to self building "
		target = b
	elif a == "60":
		action = "Send back to recycle"
	elif a == "61":
		action = "Send tank to tank fortress"
	elif a == "62":
		action = "Send infantry to reactor"
	elif a == "63":
		action = "Send infantry to fortress"
	elif a == "64":
		action = "Get into nearest civilian building"
	return action+target

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
	try:
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
	except:
		pass
	return rulesets
	
def writeRulesIni(filename,rulesets):
	try:
		with open(filename, 'w') as f:
			f.write(str(rulesets))
	except:
		pass

class EntryBox(Frame):
	def __init__(self,master,name):
		Frame.__init__(self,master)
		self.label = Label(self,text=name)
		self.var = StringVar()
		self.entry = Entry(self,textvariable=self.var,width=80)
		self.label.pack(side=LEFT,fill=X)
		self.entry.pack(side=RIGHT)
	
	def addButton(self,name,tabname,config,code):
		Button(self,text=name,command=lambda:gotoConfig(tabname,config,code)).pack(side=LEFT,fill=X)
		
class EntryCollection(Frame):
	def __init__(self,master,name):
		Frame.__init__(self,master)
		self.entries = {}
		self.info = Label(self,text="",wraplength=600)
		self.info.pack(side=TOP,fill=X)
		
	def add(self,name):
		self.entries[name] = EntryBox(self,name)
		self.entries[name].pack(side=TOP,fill=X)
	
	def get(self,name):
		return self.entries[name]
		
	def setInfo(self,name):
		self.info.config(text=name)
	
class EntrySet(Frame):
	def __init__(self,master,name):
		Frame.__init__(self,master)
		self.name = name
		self.master = master
		self.scrollbar = Scrollbar(self,orient=VERTICAL)
		self.listbox = Listbox(self,yscrollcommand=self.scrollbar.set,selectmode=SINGLE)
		self.scrollbar.config(command=self.listbox.yview)
		self.listbox.bind("<<ListboxSelect>>", self.click)
		self.listbox.pack(side=LEFT, fill=BOTH)
		self.scrollbar.pack(side=LEFT, fill=BOTH)
		
		self.collections = {}
		self.oldselect = None
		self.currcollection = None
		self.action = ""
	
	def add(self,name):
		self.listbox.insert(END,name)
		self.collections[name] = EntryCollection(self,name)
		self.changedSelect()
		
	def get(self, name):
		return self.collections[name]
	
	def click(self,event):
		self.changedSelect()
	
	def show(self):
		self.pack(side=LEFT,expand=YES,fill=BOTH)

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
	
	def analyseScript(self):
		code = self.name
		i = 0
		actions = []
		while True:
			if not str(i) in self.collections: break
			nums = self.get(str(i)).get(str(i)).var.get().split(',')
			if len(nums) != 2: return
			actions.append(describeScript(nums[0],nums[1]))
			i += 1
		self.action = "; ".join(actions)
		
	def analyseTaskforceName(self):
		code = self.name
		i = 0
		force = []
		while True:
			if not str(i) in self.collections: break
			num,unit = self.get(str(i)).get(str(i)).var.get().split(',')
			force.append("%s %s"%(num,discriptions[unit]))
			i += 1
		self.get("Name").get("Name").var.set(", ".join(force))
			
	def readConfigure(self,rulesets):
		triggers = rulesets.getRuleSet(self.name)
		allcodes = [code for code in triggers.list]
		allcodes.sort()
		for code in allcodes:
			detail = triggers.getVar(code)
			self.add(code)
			self.get(code).add("Name")
			self.get(code).add("Team1")
			self.get(code).add("Country")
			self.get(code).add("TechLevel")
			self.get(code).add("Trigger Condition")
			self.get(code).add("Target")
			self.get(code).add("Compare")
			self.get(code).add("Value")
			self.get(code).add("Prabability")
			self.get(code).add("MaxPrabability")
			self.get(code).add("MinPrabability")
			self.get(code).add("Belong")
			self.get(code).add("Team2")
			self.get(code).add("Easy")
			self.get(code).add("Medium")
			self.get(code).add("Hard")
			info = detail.split(',')
			self.get(code).get("Name").var.set(info[0])
			self.get(code).get("Team1").var.set(info[1])
			self.get(code).get("Country").var.set(info[2])
			self.get(code).get("TechLevel").var.set(info[3])
			self.get(code).get("Trigger Condition").var.set(info[4])
			self.get(code).get("Target").var.set(info[5])
			self.get(code).get("Value").var.set(info[6][:2])
			self.get(code).get("Compare").var.set(info[6][9])
			self.get(code).get("Prabability").var.set(info[7])
			self.get(code).get("MaxPrabability").var.set(info[8])
			self.get(code).get("MinPrabability").var.set(info[9])
			self.get(code).get("Belong").var.set(info[12])
			self.get(code).get("Team2").var.set(info[14])
			self.get(code).get("Easy").var.set(info[15])
			self.get(code).get("Medium").var.set(info[16])
			self.get(code).get("Hard").var.set(info[17])
			self.get(code).get("Team1").addButton("Goto","TeamTypes",teamtypeConfig,info[1])
			
	def writeConfigure(self,rulesets):
		rulesets.addRuleSet(RuleSet(self.name))
		ruleset = rulesets.getRuleSet(self.name)
		for code in self.collections:
			ec = self.get(code)
			info = [ec.get("Name").var.get(),ec.get("Team1").var.get(),ec.get("Country").var.get(),\
				ec.get("TechLevel").var.get(),ec.get("Trigger Condition").var.get(),\
				ec.get("Target").var.get(),
				"%s0000000%s000000000000000000000000000000000000000000000000000000"%(ec.get("Value").var.get(),ec.get("Compare").var.get()),\
				ec.get("Prabability").var.get(),ec.get("MaxPrabability").var.get(),\
				ec.get("MinPrabability").var.get(),"1","0",ec.get("Belong").var.get(),"0",\
				ec.get("Team2").var.get(),ec.get("Easy").var.get(),\
				ec.get("Medium").var.get(),ec.get("Hard").var.get()]
			ruleset.addRule("%s=%s"%(code,','.join(info)))
			
class Configuration(Frame):
	def __init__(self, master, name):
		Frame.__init__(self,master)
		self.name = name
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
	
	def goto(self,name):
		for index in range(self.listbox.size()):
			if self.listbox.get(index) == name:
				self.listbox.selection_set(index)
				self.changedSelect()
				break
	
	def readConfigure(self,rulesets):
		register = rulesets.getRuleSet(self.name)
		allcodes = [register.getVar(r) for r in register.list]
		allcodes.sort()
		for code in allcodes:
			self.add(code)
			info = rulesets.getRuleSet(code)
			for i in info.list:
				self.get(code).add(i)
				self.get(code).get(i).add(i)
				entry = self.get(code).get(i).get(i)
				entry.var.set(info.getVar(i).strip())
					
	def writeConfigure(self,rulesets):
		rulesets.addRuleSet(RuleSet(self.name))
		register = rulesets.getRuleSet(self.name)
		i=0
		for code in self.entrysets:
			register.addRule("%d=%s"%(i,code))
			i += 1
		for code in self.entrysets:
			rulesets.addRuleSet(RuleSet(code))
			ruleset = rulesets.getRuleSet(code)
			for ec in self.get(code).collections:
				ruleset.addRule("%s=%s"%(ec,self.get(code).get(ec).get(ec).var.get()))

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
	options = {'defaultextension':'.ini'}
	options['filetypes'] = [('all files', '.*'), ('ini files', '.ini')]
	filename = tkFileDialog.askopenfilename(**options)
	rulesets = readRulesIni(filename)
	readConfigure()
	
def	savefile():
	global rulesets
	writeConfigure()
	options = {'defaultextension':'.ini'}
	options['filetypes'] = [('all files', '.*'), ('ini files', '.ini')]
	filename = tkFileDialog.asksaveasfilename(**options)
	writeRulesIni(filename,rulesets)

def writeConfigure():
	global rulesets
	rulesets = RuleSets()
	taskforceConfig.writeConfigure(rulesets)
	scripttypeConfig.writeConfigure(rulesets)
	teamtypeConfig.writeConfigure(rulesets)
	triggertypeConfig.writeConfigure(rulesets)
	
def readConfigure():
	global rulesets
	taskforceConfig.readConfigure(rulesets)
	teamtypeConfig.readConfigure(rulesets)
	scripttypeConfig.readConfigure(rulesets)
	triggertypeConfig.readConfigure(rulesets)
	for code in teamtypeConfig.entrysets:
		entryset = teamtypeConfig.get(code)
		taskforce = entryset.get("TaskForce").get("TaskForce").var.get()
		entryset.get("TaskForce").get("TaskForce").addButton(\
			"Goto","TaskForces",taskforceConfig,taskforce)
		script = entryset.get("Script").get("Script").var.get()
		entryset.get("Script").get("Script").addButton(\
			"Goto","ScriptTypes",scripttypeConfig,script)
	update()

def update():
	for code in scripttypeConfig.entrysets:
		entryset = scripttypeConfig.get(code)
		entryset.analyseScript()
	for code in taskforceConfig.entrysets:
		entryset = taskforceConfig.get(code)
		entryset.analyseTaskforceName()
	for code in triggertypeConfig.collections:
		collection = triggertypeConfig.get(code)
		team = collection.get("Team1").var.get()
		taskforce = teamtypeConfig.get(team).get("TaskForce").get("TaskForce").var.get()
		script = teamtypeConfig.get(team).get("Script").get("Script").var.get()
		units = taskforceConfig.get(taskforce).get("Name").get("Name").var.get()
		action = scripttypeConfig.get(script).action
		condition = triggerConditions[collection.get("Trigger Condition").var.get()]
		target = collection.get("Target").var.get()
		try:
			condition = condition.replace("unit",discriptions[target])
		except:
			pass
		condition += comparator[collection.get("Compare").var.get()]+\
			collection.get("Value").var.get()
		collection.setInfo("%s:\nWhen %s:\n%s"%(units,condition,action))
		
def gotoConfig(tabname,config,code):
	bar.switch_tab(tabname)
	config.goto(code)

if __name__ == '__main__':
		
	root = Tk()
	root.title("RA2 rules editor")
	root.minsize(width=1000, height=600)
	root.maxsize(width=1000, height=600)
	root.resizable(width=FALSE, height=FALSE)
	bar = TabBar(root, "TaskForces")
	
	toolBar = Frame(root);
	Button(toolBar,text="Open",command=openfile).pack(side=LEFT,fill=Y)
	Button(toolBar,text="Save",command=savefile).pack(side=LEFT,fill=Y)
	toolBar.pack(side=BOTTOM,fill=X)
	
	tabTaskForce = Tab(root, "TaskForces")
	Label(tabTaskForce, text="TaskForces").pack(side=TOP)
	tabScriptTypes = Tab(root, "ScriptTypes")
	Label(tabScriptTypes, text="ScriptTypes").pack(side=TOP)
	tabTeamTypes = Tab(root, "TeamTypes")
	Label(tabTeamTypes, text="TeamTypes").pack(side=TOP)
	tabAITriggerTypes = Tab(root, "AITriggerTypes")
	Label(tabAITriggerTypes, text="AITriggerTypes").pack(side=TOP)
	tabInformation = Tab(root, "Information")
	Label(tabInformation, justify=LEFT, text="""
Trigger Condition:
0 If target enemy satisfies ...
1 If my units satisfy ...
2 If enemy power is yellow ...
3 If enemy power is red ...
4 If target enemy money is larger than ...
5 If my curtain is ready ...
6 If my chrono transport is ready ...
7 If civilian satisfies ...
					""").pack(side=TOP, fill=BOTH)
	Label(tabInformation, justify=LEFT, text="Compare: 0 < 1 <= 2 = 3 >= 4 > 5 !=").pack(side=TOP,fill=BOTH)
	Label(tabInformation, justify=LEFT, text="Belong: 1 Allied 2 Soviet 3 Yuri").pack(side=TOP,fill=BOTH)
	
	bar.add(tabTaskForce)
	bar.add(tabScriptTypes)
	bar.add(tabTeamTypes)
	bar.add(tabAITriggerTypes)
	bar.add(tabInformation)
	bar.show()
	
	taskforceConfig = Configuration(tabTaskForce,"TaskForces")
	taskforceConfig.show()
	scripttypeConfig = Configuration(tabScriptTypes,"ScriptTypes")
	scripttypeConfig.show()
	teamtypeConfig = Configuration(tabTeamTypes,"TeamTypes")
	teamtypeConfig.show()
	triggertypeConfig = EntrySet(tabAITriggerTypes,"AITriggerTypes")
	triggertypeConfig.show()
	
	root.mainloop()