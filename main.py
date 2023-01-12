from kivy.config import Config
from android.permissions import request_permissions, Permission
request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
Config.set('kivy','log_dir','/storage/emulated/0/.kivy/logs')
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.widget import Widget
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.filemanager import MDFileManager
import os
from kivymd.toast import toast
from kivymd.uix.screenmanager import MDScreenManager
from kivy.properties import StringProperty
import requests
import threading
from kivy.clock import  Clock,mainthread

import pathlib
import random
import sys
KV = '''
#:import  CardTransition kivy.uix.screenmanager.CardTransition
<CommonComponentLabel>
    halign: "center"
<CommonComponent>:
    
    type_height:'small'
    title:"Image Background Remover"
    opposite_colors:True
    elevation:3
    left_action_items:[['menu',lambda x:x,"Menu"]]
    

<MD3Card>
    #padding: 4
    id:card
    size_hint: 0.9,0.6
    #size:"360dp","500dp"
    focus_behavior: False
    ripple_behavior: False
    elevation: 6
    pos_hint: {"center_x": .5, "center_y": .5}
    md_bg_color: "darkgrey"
    unfocus_color: "darkgrey"
    focus_color: "grey"
    style:"outlined"
    line_color:(0.2, 0.254, 0.1, 0.8)
    shadow_softness:12
    shadow_offset:0,2


<Main_Screen>:
	name:'main_screen'
    MDBoxLayout:    
        orientation:'vertical'
        CommonComponent:
            
        MDFloatLayout:
            MD3Card:

                MDFloatLayout:
                    #size_hint:0.9,0.6
                    
                    MDRectangleFlatIconButton:
                        text:"Upload"
                        icon:"upload"
                        #font_name:"ubuntu.ttf"                  
                        theme_text_color: "Custom"
                        text_color: "white"
                        font_size:"29sp"
                        theme_icon_color: "Custom"
                        icon_color: "white"
                        md_bg_color:0.2,0.3,0.5,1
                        pos_hint:{'center_x':0.5,'center_y':0.5}
                        halign:"center"
                        anchor_y:"top"
                        anchor_x:"center"
                        size_hint:None,None
                        size:"60dp","60dp"
                        on_release:app.open_manager()
                    MDLabel:
                        text:'Supported format'
                        halign:'center'
                        #font_name:"ubuntu.ttf"
                        font_size:'16sp'  
                        pos_hint:{"center_x":0.5,"center_y":0.3}
                    MDLabel:
                        text:'*png, *jpg, *jpeg'
                        halign:'center'
                        #font_name:"ubuntu.ttf"
                        font_size:'18sp'  
                        pos_hint:{"center_x":0.5,"center_y":0.2}
            
            
            
<Upload_Screen>:
	name:'upload_screen'
    MDBoxLayout:
        orientation:'vertical'
        CommonComponent:

        MDFloatLayout:
            MD3Card:
            	MDFloatLayout:
	            	MDProgressBar:
	            	    id: progress
	            	    pos_hint: {'center_x':0.5,"center_y": .6}
	            	    size_hint:0.8,0.8
	            	    type: "indeterminate"   
	            	    radius:[15,15,15,15] 
	            	    orientation:"horizontal"
	            	    color:0.1,0.2,0.4,1
	            	MDRectangleFlatIconButton:
	            		id:dwn
	            	    #text: "Processing" if root.state == "start" else "START"
	            	    pos_hint: {"center_x": 0.5, "center_y": .45}
	            	    #font_name:'ubuntu.ttf'
	            	    font_size:'25sp'
	            	    theme_text_color: "Custom"
                        text_color: "white"
                        
                        theme_icon_color: "Custom"
                        icon_color: "white"
                        md_bg_color:72.0/255.0, 113.0/255.0, 247.0/255.0,1
                        icon:'download'
	            	    on_release: root.save()



        







WindowManager:
	id:screen_manager
    transition:CardTransition()
    Main_Screen:
    Upload_Screen:

'''
image_name='' 
class MD3Card(MDCard,RectangularElevationBehavior):
    '''Implements a material design v3 card.'''

    pass

class CommonComponent(MDTopAppBar):
    pass







class WindowManager(MDScreenManager):
	pass
class Main_Screen(MDScreen):
    pass
class Upload_Screen(MDScreen):
	
	def on_enter(self):
		self.img=image_name
		#t1=threading.Thread(target=self.func)
		t2=threading.Thread(target=self.process)
		
		t2.start()
		#t1.start()
		#t1.join()
		#t2.join()
	def process(self):
		
		self.ids.progress.start()
		self.ids.dwn.text='Processing'
		self.ids.dwn.disabled=True
		Clock.schedule_once(self.func,3)
		
	@mainthread	
	def func(self,time):

		
		PATH = image_name
		API_KEY = "XLfY8VTltCo6FHBKBXVgfA4afpGY1aEx"
		file_name=str(os.path.basename(image_name))
		headers = {
		    'x-picsart-api-key': API_KEY,
		}
		files = {
		    'output_type': (None, 'cutout'),
		    'format': (None, 'PNG'),
		    'image':(file_name,open(PATH,'rb'),)
		}
		response = requests.post('https://api.picsart.io/tools/1.0/removebg', headers=headers, files=files)
		status_code=response.status_code
		if status_code==200:
			rjson=response.json()
			output_url=rjson['data']['url']
			self.r=requests.get(output_url,allow_redirects=True)
			self.ids.dwn.text='Save'
			self.ids.progress.stop()
			self.ids.progress.opacity=0
			self.ids.dwn.disabled=False
			
			toast('successfully background removed',3)
		else:
			toast(f"server unreachable: {status_code}")
				
			

		
		
		
		'''
		try:
			file_name=os.path.basename(image_name)
			s=file_name.split(".")
			ext=pathlib.Path((self.img)).suffix
			input_path=(str(self.img))
			print(input_path)
			
			self.output_path=('/storage/emulated/0/Erase/'+str(s[0])+'erase'+str(ext))
			print(self.output_path)
			input = Image.open(input_path)
			
			self.ids.dwn.text='Save'
			self.ids.progress.stop()
			self.ids.progress.opacity=0
			self.ids.dwn.disabled=False

			#os.mkdir(self.output_path)
		except OSError as error:
			print(str(error))

		except Exception as er:
			toast(str(er))
		'''
	def save(self):
		#image_name=r"C:\Users\Anupam\Desktop\edit.jpg"
		#self.ids.dwn.text='Save'
		#self.ids.dwn.disabled=False
		if self.ids.dwn.text=='Save' or self.ids.dwn.disabled==False:
			try:
				
				isfolder=(os.path.exists(path="/storage/emulated/0/output"))
				print(isfolder)
				if isfolder== False:					
					os.mkdir(path="/storage/emulated/0/output")
					
					file=os.path.basename(image_name)
					
					file_nam=os.path.splitext(file)[0]
					file_ext=os.path.splitext(file)[1]
					output_name=str(file_nam)+"bg"+".png"
					if os.path.exists(output_name) ==True:
						no=random.randint(0, 9999)
						split_file=output_name.split()
						modify_file=str(file_nam)+"bg"+str(no)+".png"
						print(modify_file)
						
						os.chdir("/storage/emulated/0/output")

						with open(modify_file,'wb') as file:
							file.write(self.r.content)
						toast("File save successfully",3)
					else:
						os.chdir("/storage/emulated/0/output")

						with open(output_name,'wb') as file:
							file.write(self.r.content)
						toast("File save successfully",3)
				else:
					#os.chdir("/storage/emulated/0/output")
					file=os.path.basename(image_name)
					
					file_nam=os.path.splitext(file)[0]
					file_ext=os.path.splitext(file)[1]
					output_name=str(file_nam)+"bg"+".png"
					if os.path.exists(output_name) ==True:
						no=random.randint(0, 9999)
						split_file=output_name.split()
						modify_file=str(split_file[0])+str(no)+".png"
						print(modify_file)
						os.chmod(modify_file, 0o0777)

						os.chdir("/storage/emulated/0/output")

						with open(modify_file,'wb') as file:
							file.write(self.r.content)
						toast("File save successfully",3)
					else:
						os.chdir("/storage/emulated/0/output")
						with open(output_name,'wb') as file:
							file.write(self.r.content)
						toast("File save successfully",3)

			
			except PermissionError as pr:
				toast(str(pr))
			except Exception as er:
				toast(str(er),3)
				print(er)
				
		else:
			self.ids.dwn.disabled=False
			
		        


	


       

class Test(MDApp):
    def __init__(self,**kw):
        super().__init__(**kw)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(preview=True,exit_manager=self.exit_manager,select_path=self.select_path)

    def exit_manager(self,catch):
        self.manager_open = False
        self.file_manager.close()

        
    def select_path(self,path):
        self.manager_open = False
        self.file_manager.close()
        global image_name
        if image_name == "":
        	image_name=path
        else:
        	image_name=""
        	image_name=path
        toast(str(path),3)
        self.root.current='upload_screen'
    def events(self,instance,keyboard,keycode,text,modifier):
    	if keyboard in (1001,27):
    		if self.manager_open:
    			self.file_manager.back()
    	return True
        
	        


    def open_manager(self):
        self.file_manager.show(os.path.expanduser("/storage/"))  # output manager to the screen
        self.manager_open = True

    def build(self):
        return Builder.load_string(KV)
    #def on_start(self):
    	
    	#self.root.current='upload_screen'
    	#print(dir(os.chmod(path, mode)))


    
            
                    
                    
                    
                
            
try:
	Test().run()
except:

	exc_type,exc_value,exc_traceback=sys.exc_info()
	with open('/storage/emulated/0/error_app.txt','a+') as f:
		f.write(f'{exc_type}\n{exc_value}\n{exc_traceback}')