
# C/TK
import tkinter.filedialog
from doctest import master

import tkextrafont as tkfont
import customtkinter
import tkinter
from CTkListbox import CTkListbox
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkImage

# MEDA LIBS
from Lib import socketConn
from Lib import mailApi
from Lib import exerciseApi
from Lib import exerciseGraphicer


from PIL import Image, ImageDraw

import configparser
import shutil
import tkinter
import pywinstyles
import hPyT
import threading
import smtplib
import json
import os

# Font Load

asimovian_FontPath = "Assets/Fonts/Asimovian-Regular.ttf"
kanit_FontPath = "Assets/Fonts/Kanit-Light.ttf"


class LoadMEDA:
    def __init__(self):
        self.event_Meda()

    def event_Meda(self):
        try:
            self.jsondata.close()
        except:
            pass
        with open("Data\\Json\\Data.json", "r") as jsonF:
            self.jsondata = json.load(jsonF)
        if self.jsondata["FirstEntry"] == True:
            firstentry = FirstEntry()
            return
        
        elif self.jsondata["KeepLogin"] == True:
            if self.jsondata["AccountType"] == "Doktor":
                doctorapp = loadDoctor()
                return
            elif self.jsondata["AccountType"] == "Hasta":
                clientapp = loadClient()
                return
            
        elif self.jsondata["KeepLogin"] == False:
            loginapp = loadLogin()
            return


class loadLogin:
    def __init__(self):
        with open("Data\\Json\\Data.json", "r", errors="ignore") as loadDatajsons:
            loginPdata = json.load(loadDatajsons)

        def CheckInfo() -> any:
            name = NameInput.get()
            passW = PassInput.get()

            if name == "" or passW == "":
                errLabel.place(x=50,y=50)
                errLabel.configure(text="Lütfen tüm alanları doldurun.")
                return
            else:
                if loginPdata["Username"] == name:
                    if loginPdata["Password"] == passW:
                        if KeepLoginCheck.get() == "OK":

                            loginPdata["KeepLogin"] = True

                            with open("Data/Json/Data.json", "w") as f:
                                json.dump(loginPdata,f,indent=4,ensure_ascii=False)
                                LoginPage.destroy()
                                doctorApp = loadDoctor()
                        else:
                            LoginPage.destroy()
                            doctorApp = loadDoctor()
                    else:
                        errLabel.place(x=55,y=50)
                        errLabel.configure(text="Girilen Bilgiler Uyuşmuyor.")
                else:
                    errLabel.place(x=55,y=50)
                    errLabel.configure(text="Girilen Bilgiler Uyuşmuyor.")


        LoginPage = customtkinter.CTk(fg_color="#FFFFFF")
        LoginPage.geometry("300x350")
        LoginPage.title("MEDA | Giriş")
        LoginPage.resizable(False, False)
        pywinstyles.change_header_color(LoginPage, color="#0B08AD")
        LoginFrame = customtkinter.CTkFrame(master=LoginPage, width=250,height=300,fg_color="#E7E7E7", corner_radius=10,border_width=1,border_color="#C4C4C4")
        LoginFrame.place(x=25,y=25)

        MediTitle = customtkinter.CTkLabel(master=LoginFrame,text="M.E.D.A", font=("Helvetica",35,"bold"),text_color="#000000")
        MediTitle.place(x=60,y=15)

        errLabel = customtkinter.CTkLabel(master=LoginFrame,text="",text_color="#CC0505", font=("Default", 12, "italic"))
        errLabel.place(x=55,y=50)

        NameInput = customtkinter.CTkEntry(master=LoginFrame,placeholder_text="Kullanıcı Adı", placeholder_text_color="#000000",text_color="#000000",
                                           width=200,
                                           height=40,
                                           corner_radius=10,
                                           fg_color="#0ED482",
                                           border_width=0)
        NameInput.place(x=25,y=85)

        PassInput = customtkinter.CTkEntry(master=LoginFrame,placeholder_text="Şifre", placeholder_text_color="#000000",text_color="#000000",
                                           width=200,
                                           height=40,
                                           corner_radius=10,
                                           fg_color="#DDAC0A",
                                           border_width=0,
                                           show="*")
        PassInput.place(x=25,y=140)


        KeepLoginCheck = customtkinter.CTkCheckBox(master=LoginFrame,text="Beni Hatırla", fg_color="#DFDFDF",hover_color="#BDBBBB",checkmark_color="#0BE0AB", 
                                                   text_color="#000000",
                                                   border_width=2,
                                                   onvalue="OK",
                                                   offvalue="NO")
        KeepLoginCheck.place(x=25,y=185)


        LoginButton = customtkinter.CTkButton(master=LoginFrame,text="Giriş", font=("Default",21),text_color="#000000",fg_color="#08E0CE",
                                              width=150,
                                              height=40,
                                              hover_color="#07B1A3",
                                              command=CheckInfo)
        LoginButton.place(x=50,y=225)
        LoginPage.mainloop()



class FirstEntry:
    def __init__(self):
        RegisteryPage = customtkinter.CTk(fg_color="#FFFFFF")
        RegisteryPage.geometry("350x450")
        RegisteryPage.resizable(False, False)
        RegisteryPage.title("MEDA | KAYIT")
        pywinstyles.change_header_color(RegisteryPage, color="#0B08AD")

        RegisterFrame = customtkinter.CTkFrame(master=RegisteryPage, width=300,height=400,fg_color="#E7E7E7", corner_radius=10,border_width=1,border_color="#C4C4C4")
        RegisterFrame.place(x=25,y=25)


        def event_Register():
            name = NameInput.get()
            passW = PassInput.get()
            passW2 = PassInput2.get()
            mail = MailInput.get()


            if name == "" or passW == "" or passW2 == "" or mail == "":
                errLabel.configure(text="Tüm alanları doldurunuz.")
                return
            
            elif radio_var.get() == "NONE":
                errLabel.configure(text="Tüm alanları doldurunuz.")
                return
            
            elif passW != passW2:
                print(passW)
                print(passW2)
                errLabel.configure(text="Şifre uyuşmazlığı.")
                return

            data={
                "FirstEntry" : False,
                "Username" : NameInput.get(),
                "Password" : PassInput.get(),
                "Mail" : MailInput.get(),
                "AccountType" : radio_var.get(),
                "SMTPKEY" : None,
                "KeepLogin" : False
            }


            with open("Data/Json/Data.json", "w") as f:
                json.dump(data,f,indent=4, ensure_ascii=False)
                RegisteryPage.destroy()

            
        MediTitle = customtkinter.CTkLabel(master=RegisterFrame,text="M.E.D.A", font=("Helvetica",35,"bold"),text_color="#000000")
        MediTitle.place(x=85,y=15)

        errLabel = customtkinter.CTkLabel(master=RegisterFrame,text="",text_color="#CC0505", font=("Default", 12, "italic"))
        errLabel.place(x=80,y=55)


        NameInput = customtkinter.CTkEntry(master=RegisterFrame,placeholder_text="Kullanıcı Adı", placeholder_text_color="#000000",text_color="#000000",
                                           width=200,
                                           height=40,
                                           corner_radius=10,
                                           fg_color="#0ED482",
                                           border_width=0)
        NameInput.place(x=50,y=85)

        MailInput = customtkinter.CTkEntry(master=RegisterFrame,placeholder_text="Mail", placeholder_text_color="#000000",text_color="#000000",
                                           width=200,
                                           height=40,
                                           corner_radius=10,
                                           fg_color="#A5DD0A",
                                           border_width=0)
        MailInput.place(x=50,y=135)

        PassInput = customtkinter.CTkEntry(master=RegisterFrame,placeholder_text="Şifre", placeholder_text_color="#000000",text_color="#000000",
                                           width=200,
                                           height=40,
                                           corner_radius=10,
                                           fg_color="#117ED8",
                                           border_width=0,
                                           show="*")
        PassInput.place(x=50,y=185)

        PassInput2 = customtkinter.CTkEntry(master=RegisterFrame,placeholder_text="Şifre Tekrar", placeholder_text_color="#000000",text_color="#000000",
                                           width=200,
                                           height=40,
                                           corner_radius=10,
                                           fg_color="#4220D8",
                                           border_width=0,
                                           show="*")
        PassInput2.place(x=50,y=235)


        radio_var = tkinter.StringVar(value="NONE")
        clientCheckBox = customtkinter.CTkRadioButton(master=RegisterFrame,text="Hasta", text_color="#000000",hover_color="#04C5CC",fg_color="#02DBE2",
                                                      variable= radio_var, value="Hasta")
        clientCheckBox.place(x=75,y=285)
        doctorCheckBox = customtkinter.CTkRadioButton(master=RegisterFrame,text="Doktor", text_color="#000000",hover_color="#04C5CC",fg_color="#02DBE2",
                                                      variable= radio_var, value="Doktor")
        doctorCheckBox.place(x=150,y=285)


        LoginButton = customtkinter.CTkButton(master=RegisterFrame,text="Kayıt Ol", font=("Default",21),text_color="#000000",fg_color="#08E0CE",
                                              width=150,
                                              height=40,
                                              hover_color="#07B1A3",
                                              command=event_Register)
        LoginButton.place(x=75,y=325)

        RegisteryPage.mainloop()


class loadDoctor:
    def __init__(self):

        with open("Data/Json/Log.json", "r") as f:
            infoData = json.load(f)

        with open("Data/Profiles/Users.json", "r") as f:
            self.usersData = json.load(f)

        self.config = configparser.ConfigParser()
        self.config.read("Config\\settings.ini")

        self.doctorPage = customtkinter.CTk(fg_color="#FFFFFF")
        self.doctorPage.geometry("860x520")
        self.doctorPage.title("MEDA | Doktor")
        self.doctorPage.resizable(False, False)
        asimovian_Font = tkfont.Font(root=self.doctorPage,file=asimovian_FontPath,family="Asimovian")
        kanit_Font = tkfont.Font(root=self.doctorPage,file=kanit_FontPath,family="Kanit")

        pywinstyles.change_header_color(self.doctorPage, color="#0B08AD")
        hPyT.window_dwm.toggle_cloak(self.doctorPage, False)


        # MainMenu Frame and Widgets
        exerciseApi.controlLogs()
        totalExercises = exerciseApi.getLogs(mode="total")
        mostBigExercises = exerciseApi.getLogs(mode="Biggest")
        MainMenuFrame = customtkinter.CTkFrame(master=self.doctorPage,width=640,height=500,corner_radius=10,border_width=0,fg_color="#E7E7E7")
        MainMenuFrame.place(x=210,y=7)

        MainMenuFrameTitle = customtkinter.CTkLabel(master=MainMenuFrame,text="Ana Sayfa",text_color="#000000",font=("Default",35,"bold"))
        MainMenuFrameTitle.place(x=225,y=15)

        InfosFrame = customtkinter.CTkFrame(master=MainMenuFrame,width=250,height=200,corner_radius=15,border_width=0,fg_color="#C4CAC9")
        InfosFrame.place(x=10,y=60)

        InfoFrameTitle = customtkinter.CTkLabel(master=InfosFrame,text="Bilgilendirme",fg_color="#1ED4CA",corner_radius=10, font=("Kanit",24),text_color="#000000")
        InfoFrameTitle.place(x=45,y=5)

        TodayFrame = customtkinter.CTkFrame(master=MainMenuFrame,width=250,height=200,corner_radius=15,border_width=0,fg_color="#C4CAC9")
        TodayFrame.place(x=10,y=270)

        TodayFrameTitle = customtkinter.CTkLabel(master=TodayFrame,text="Bugün",fg_color="#1ED4CA",corner_radius=10, font=("Kanit",24),text_color="#000000")
        TodayFrameTitle.place(x=80,y=5)

        todayExercises = customtkinter.CTkLabel(master=TodayFrame, text=f"Toplam Egzersiz : {totalExercises}", font=("Default",18, "bold"),text_color="#000000", fg_color="#52D47C", corner_radius=10)
        todayExercises.place(x=10,y=50)

        mostExercises = customtkinter.CTkLabel(master=TodayFrame, text=f"En Çok : {mostBigExercises}", font=("Default",18, "bold"),text_color="#000000", fg_color="#52D47C", corner_radius=10)
        mostExercises.place(x=10,y=100)


        todayTime = customtkinter.CTkLabel(master=TodayFrame, text=exerciseApi.getTime(), font=("Kanit", 15, "bold"),text_color="#000000", fg_color="#D4D37D", corner_radius=10)
        todayTime.place(x=75,y=160)


        totalUser = customtkinter.CTkLabel(master=InfosFrame,text=f"Kayıtlı Kullanıcı : {infoData['TotalUser']}", font=("Default", 18),text_color="#000000")
        totalUser.place(x=10,y=50)

        totalExercise = customtkinter.CTkLabel(master=InfosFrame,text=f"Toplam Egzersiz : {infoData['TotalExercise']}",font=("Default", 18),text_color="#000000")
        totalExercise.place(x=10,y=75)

        testSock = socketConn.TryConn()
        connAct = customtkinter.CTkLabel(master=InfosFrame,text=f"Bağlantı : {testSock.connS()}", font=("Default",18),text_color="#000000")
        connAct.place(x=10,y=100)

        mailApiAct = customtkinter.CTkLabel(master=InfosFrame,text=f"Mail : {infoData['MailKEY']}",font=("Default",18),text_color="#000000")
        mailApiAct.place(x=10,y=125)

        self.UsersList = CTkListbox(master=MainMenuFrame,width=300,height=325,corner_radius=15,border_width=0,fg_color="#CFCCCC",command=self.event_UserList,hover_color="#8AE8D9",button_color="#B5E6E8")
        self.UsersList.place(x=290,y=60)

        for user in self.usersData.keys():
            self.UsersList.insert(tkinter.END, user)

        RenewUserList = customtkinter.CTkButton(master=MainMenuFrame,text="",image=CTkImage(light_image=Image.open("Assets\\Button\\renew.png"),size=(38,38)), width=300,height=40,
                                                fg_color="#2AE720",
                                                hover_color="#62E754",
                                                command=lambda:self.renewList(listF=self.UsersList))

        RenewUserList.place(x=300,y=420)

        def loopLabel():
            todayExercises.configure(text=f"Toplam Egzersiz : {exerciseApi.getLogs(mode='total')}")
            mostExercises.configure(text=f"En Çok : {exerciseApi.getLogs(mode='Biggest')}")
            totalUser.configure(text=f"Kayıtlı Kullanıcı : {exerciseApi.getLogs(mode='AllUser')}")
            totalExercise.configure(text=f"Toplam Egzersiz : {exerciseApi.getLogs(mode='AllExercises')}")
            self.doctorPage.after(500, loopLabel)

        self.doctorPage.after(500, loopLabel)

        # UserMenu Frame and Widgets

        UserMenuFrame = customtkinter.CTkFrame(master=self.doctorPage,width=640,height=500,corner_radius=10,border_width=0,fg_color="#E7E7E7")
        UserMenuFrame.place(x=210,y=7)

        def opt(choice):
            if choice == "Hepsi":
                exerciseGraphicer.plot_logs("Hepsi")
                img = customtkinter.CTkImage(light_image=Image.open("user.png"), size=(600, 375))
                imgLabel.configure(image=img)
                imgLabel.image = img
                return
            try:
                exerciseGraphicer.plot_logs(choice)
            except:
                self.event_MSGBOX(mTitle="Egzersiz Grafik İşlem", mText="Kullanıcı Verisi Bulunamadı.", TheCode="cancel")
                return
            img = customtkinter.CTkImage(light_image=Image.open("user.png"), size=(600, 375))
            imgLabel.configure(image=img)
            imgLabel.image = img

        selecterMenu = customtkinter.CTkOptionMenu(master=UserMenuFrame,text_color="#000000",values=list(self.usersData.keys()) + ['Hepsi'],corner_radius=10,fg_color="#39C6CA", button_color="#12CAC6", command=opt)
        selecterMenu.place(x=20,y=75)

        def selecterLoop():
            with open("Data\\Profiles\\Users.json","r",encoding="utf-8") as f:
                data = json.load(f)
            selecterMenu.configure(values=list(data.keys()) + ['Hepsi'])
            self.doctorPage.after(5000, selecterLoop)

        self.doctorPage.after(5000, selecterLoop)

        imgLabel = customtkinter.CTkLabel(master=UserMenuFrame,text="")
        imgLabel.place(x=20,y=110)

        def CreateUser():
            UserAddPage = customtkinter.CTkToplevel(master=self.doctorPage)
            UserAddPage.title("MEDA | Yeni Kullanıcı")
            UserAddPage.geometry("350x350")
            UserAddPage.resizable(False,False)
            self.pfpPath = None

            pywinstyles.change_header_color(UserAddPage, color="#0B08AD")
            hPyT.window_dwm.toggle_cloak(UserAddPage, False)

            UserAddPage.grab_set()

            def createUSER():
                if self.pfpPath:
                    try:
                        with open("Data\\Profiles\\Users.json", "r") as f:
                            readuser = json.load(f)


                        shutil.copyfile(self.pfpPath, os.path.join("Data\\Profiles", os.path.basename(self.pfpPath)))
                        readuser[UserNameEntry.get()] = {
                            "Surname" : SurNameEntry.get(),
                            "Gender" : radio_var.get(),
                            "Age" : int(ageEntry.get()),
                            "Total_Exercises" : 0,
                            "email" : mailEntry.get(),
                            "ProfilePic" : f"Data\\Profiles\\{os.path.basename(self.pfpPath)}"
                        }

                        with open("Data\\Profiles\\Users.json", "w") as f:
                            json.dump(readuser,f,ensure_ascii=False, indent=4)

                        self.event_MSGBOX(mTitle="Kullanıcı Kayıt", mText="Kullanıcı Oluşturuldu.",TheCode="check")
                        UserAddPage.destroy()

                    except Exception as e:
                        print(e)
                        self.event_MSGBOX(mTitle="Hata!", mText=e, TheCode="cancel", master=UserAddPage)

                else:
                    self.event_MSGBOX(mTitle="Hata!", mText="Profil fotoğrafı zorunludur.", TheCode="warning", master=UserAddPage)
                    return
            
            UserFrame = customtkinter.CTkFrame(master=UserAddPage, width=300,height=300,fg_color="#D1E5E7")
            UserFrame.place(x=25,y=25)

            UserFrameTitle = customtkinter.CTkLabel(master=UserFrame,text="Yeni Kullanıcı", font=("Kanit", 20,"bold"),text_color="#000000")
            UserFrameTitle.place(x=10,y=10)

            self.PFPLoadButton = customtkinter.CTkButton(master=UserFrame,text="", image=CTkImage(dark_image=Image.open("Assets\\Button\\loadpfp.png"),size=(110,110)),
                                                    width=110,height=110, fg_color="#F8D407", command=self.loadPFP, hover_color="#DBBD10")
            self.PFPLoadButton.place(x=165,y=50)

            UserNameEntry = customtkinter.CTkEntry(master=UserFrame, placeholder_text="İsim", width=150, height=35, fg_color="#0878F8",border_width=0, placeholder_text_color="#FFFFFF",
                                                   font=("Default", 16, "bold"))
            UserNameEntry.place(x=10,y=50)

            SurNameEntry = customtkinter.CTkEntry(master=UserFrame, placeholder_text="Soyisim", width=150, height=35, fg_color="#08C8F8",border_width=0, placeholder_text_color="#FFFFFF",
                                                   font=("Default", 16, "bold"))
            SurNameEntry.place(x=10,y=90)

            ageEntry = customtkinter.CTkEntry(master=UserFrame, placeholder_text="Yaş", width=150, height=35, fg_color="#0FEBCD",border_width=0, placeholder_text_color="#FFFFFF",
                                                   font=("Default", 16, "bold"))
            ageEntry.place(x=10,y=130)


            mailEntry = customtkinter.CTkEntry(master=UserFrame, placeholder_text="E-Posta", width=150, height=35, fg_color="#DAB511",border_width=0, placeholder_text_color="#FFFFFF",
                                                   font=("Default", 16, "bold"))
            mailEntry.place(x=10,y=170)

            radio_var = tkinter.StringVar(value="NONE")
            maleRadio = customtkinter.CTkRadioButton(master=UserFrame,text="Bay", text_color="#000000",hover_color="#04C5CC",fg_color="#02DBE2",
                                                        variable= radio_var, value="Bay")
            maleRadio.place(x=10,y=210)
            femaleRadio = customtkinter.CTkRadioButton(master=UserFrame,text="Bayan", text_color="#000000",hover_color="#04C5CC",fg_color="#02DBE2",
                                                        variable= radio_var, value="Bayan")
            femaleRadio.place(x=90,y=210)

            femaleRadio.select()

            saveButton = customtkinter.CTkButton(master=UserFrame, text="Oluştur", fg_color="#40F10A", text_color="#000000",
                                                 font=("Kanit", 18,"bold"),
                                                 width=200,height=35,
                                                 command=createUSER, hover_color="#45E215")
            
            saveButton.place(x=50,y=240)


        def LoadUser():
            confPath = tkinter.filedialog.askopenfilename(title="Konfigürasyon Dosyası Seçin", filetypes=(("*JSON Dosyaları", "*.json"),), initialdir=os.path.join("Exports"))
            if confPath:
                with open(confPath, "r") as f:
                    confJson = json.load(f)

                if self.config['MEDA Settings']['msgbox_delay'] == "TRUE":
                    fade_delay = 1

                elif self.config['MEDA Settings']['msgbox_delay'] == "FALSE":
                    fade_delay = 0

                loadResponse = CTkMessagebox(title="Kullanıcı İşlem",message="Kullanıcı Sisteme Yüklenecek. Onaylıyor musunuz?", icon="info",option_1="Tamam",option_2="İptal", sound=True,fade_in_duration=fade_delay)
                if loadResponse.get() == "Tamam":
                    try:
                        with open("Data\\Profiles\\Users.json", "r", encoding='utf-8') as existing_file:
                            existing_data = json.load(existing_file)
                    except (FileNotFoundError, json.JSONDecodeError):
                        existing_data = {} 
                    existing_data.update(confJson) 

                    with open("Data\\Profiles\\Users.json", "w", encoding='utf-8') as confWrite:
                        json.dump(existing_data, confWrite, ensure_ascii=False, indent=4)

                else:
                    return


                self.event_MSGBOX(mText="Kullanıcı Yüklendi!", mTitle="Kullanıcı İşlem", TheCode="check")
                self.renewList(self.usfUSERLIST)

            else:
                return



        UserMenuFrameTitle = customtkinter.CTkLabel(master=UserMenuFrame,text="Kullanıcı Sayfası",text_color="#000000",font=("Default",35,"bold"))
        UserMenuFrameTitle.place(x=200,y=15)

        ExerciseFrame = customtkinter.CTkFrame(master=self.doctorPage,width=640,height=500,corner_radius=10,border_width=0,fg_color="#E7E7E7")
        ExerciseFrame.place(x=210,y=7)


        ExerciseFrameTitle =customtkinter.CTkLabel(master=ExerciseFrame,text="Egzersiz Sayfası",text_color="#000000",font=("Default",35,"bold"))
        ExerciseFrameTitle.place(x=185,y=15)

        UserManagementFrame = customtkinter.CTkFrame(master=ExerciseFrame, width=250, height=200,fg_color="#C4CAC9",corner_radius=15)
        UserManagementFrame.place(x=10,y=75)

        UserTitle =customtkinter.CTkLabel(master=UserManagementFrame,text="Kullanıcı Düzenleme",text_color="#111010",font=("Default",24,"bold"))
        UserTitle.place(x=10,y=5)

        AddNewUser = customtkinter.CTkButton(master=UserManagementFrame, text="Yeni Kullanıcı", fg_color="#2ECA3F",width=200, height=40,font=("Kanit",20,"bold"), text_color="#000000",
                                             command=CreateUser, hover_color="#30B940")
        AddNewUser.place(x=25,y=45)

        LoadUser = customtkinter.CTkButton(master=UserManagementFrame, text="Kullanıcı Yükle", fg_color="#CAC635",width=200, height=40,font=("Kanit",20,"bold"), text_color="#000000",
                                           command=LoadUser, hover_color="#B9B533")
        LoadUser.place(x=25,y=100)

        self.usfUSERLIST = CTkListbox(master=ExerciseFrame,width=300,height=325,corner_radius=15,border_width=0,fg_color="#CFCCCC",command=self.event_DeepUserManagement,hover_color="#8AE8D9",button_color="#B5E6E8")
        self.usfUSERLIST.place(x=290,y=75)
        RenewUserList_Exercise = customtkinter.CTkButton(master=ExerciseFrame,text="",image=CTkImage(light_image=Image.open("Assets\\Button\\renew.png"),size=(38,38)), width=300,height=40,
                                                fg_color="#2AE720",
                                                hover_color="#62E754",
                                                command=lambda:self.renewList(listF=self.usfUSERLIST))

        RenewUserList_Exercise.place(x=305,y=435)

        for user in self.usersData.keys():
            self.usfUSERLIST.insert(tkinter.END, user)

        def frameUpper(Widget):
            Widget.tkraise()

        MainMenuFrame.tkraise()

        # Left Frame and Widgets

        leftFrame = customtkinter.CTkFrame(master=self.doctorPage,width=200,height=500,corner_radius=10,border_width=0,fg_color="#E7E7E7")
        leftFrame.place(x=5,y=7)

        leftFrameTitle = customtkinter.CTkLabel(master=leftFrame,text="MEDA",text_color="#0B08AD",font=("Asimovian",45,"bold"))
        leftFrameTitle.place(x=30,y=10)


        MainMenuButton = customtkinter.CTkButton(master=leftFrame,text="Ana Sayfa",text_color="#000000",fg_color="#0DE09A",width=190,height=50,font=("Kanit",24,"bold"),
                                                 command=lambda:frameUpper(Widget=MainMenuFrame),
                                                 hover_color="#1BCA90")
        MainMenuButton.place(x=5,y=100)

        UserButton = customtkinter.CTkButton(master=leftFrame,text="Kullanıcı",text_color="#000000",fg_color="#0DDEE6",width=190,height=50,font=("Kanit",24,"bold"),
                                             command=lambda:frameUpper(Widget=UserMenuFrame),
                                             hover_color="#11C8CE")
        UserButton.place(x=5,y=160)

        ExerciseButton = customtkinter.CTkButton(master=leftFrame,text="Egzersiz",text_color="#000000",fg_color="#0D81E0",width=190,height=50,font=("Kanit",24,"bold"),
                                                 command=lambda:frameUpper(Widget=ExerciseFrame),
                                                hover_color="#1778C7")
        ExerciseButton.place(x=5,y=220)

        SettingsButton = customtkinter.CTkButton(master=leftFrame,text="Ayarlar",text_color="#000000",fg_color="#8A09C5",width=190,height=50,font=("Kanit",24,"bold"),
                                                 hover_color="#7C13AD", command=self.event_Settings)
        SettingsButton.place(x=5,y=280)


        CreditsButton = customtkinter.CTkButton(master=leftFrame,text="Hakkında",text_color="#000000",fg_color="#DFC908",width=190,height=50,font=("Kanit",24,"bold"),
                                                 hover_color="#BDAB0C")
        CreditsButton.place(x=5,y=340)

        VersionLabel = customtkinter.CTkLabel(master=leftFrame,text="1.1",font=("Kanit",15,"italic"),text_color="#A80909")
        VersionLabel.place(x=85,y=475)


        self.doctorPage.mainloop()


    def event_Settings(self):
        settingsPage = customtkinter.CTkToplevel(master=self.doctorPage,fg_color="#FFFFFF")
        settingsPage.geometry("300x400")
        settingsPage.title("MEDA | Ayarlar")
        settingsPage.grab_set()
        settingsPage.resizable(False,False)

        with open("Data\\Json\\Data.json", "r") as f:
            settingsJson = json.load(f)


        settingsFrame = customtkinter.CTkFrame(master=settingsPage,width=275,height=375,fg_color="#E9E8E8")
        settingsFrame.place(x=12,y=12)

        settingsTitle = customtkinter.CTkLabel(master=settingsFrame,text="Ayarlar", text_color="#000000",
                                               font=("Kanit", 24, "bold"))
        settingsTitle.place(x=100,y=10)

        cfVAR = tkinter.StringVar(value="NONE")
        CF1 = customtkinter.CTkCheckBox(master=settingsFrame,text="Başlangıca Ekle", checkmark_color="#1605FD",
                                        hover_color="#0ADFD4", text_color="#000000",fg_color="#02FAFA")
        CF1.place(x=10,y=45)

        CF2 = customtkinter.CTkCheckBox(master=settingsFrame,text="Mesaj Kutu Gecikmesi", checkmark_color="#1605FD",
                                        hover_color="#0ADFD4", text_color="#000000",fg_color="#02FAFA")
        CF2.place(x=10,y=75)

        CF3 = customtkinter.CTkCheckBox(master=settingsFrame,text="Bileşenleri Açılışta Yükle", checkmark_color="#1605FD",
                                        hover_color="#0ADFD4", text_color="#000000",fg_color="#02FAFA")
        CF3.place(x=10,y=105)


        try:
            liveconfig = configparser.ConfigParser()
            liveconfig.read("Config\\settings.ini")
            if liveconfig["MEDA Settings"]["start_on_windows"] == "TRUE":
                CF1.select()
            if liveconfig["MEDA Settings"]["msgbox_delay"] == "TRUE":
                CF2.select()
            if liveconfig["MEDA Settings"]["win_clock"] == "TRUE":
                CF3.select()
        except:
            pass

        nameLabel = customtkinter.CTkLabel(master=settingsFrame, text="Kullanıcı Adı", font=("Default", 18,"bold"), text_color="#000000")
        nameLabel.place(x=10,y=140)

        changeName = customtkinter.CTkEntry(master=settingsFrame,placeholder_text=f"{settingsJson['Username']}", text_color="#000000", width=150,height=30)
        changeName.place(x=10,y=165)

        passLabel = customtkinter.CTkLabel(master=settingsFrame, text="Şifre", font=("Default", 18,"bold"), text_color="#000000")
        passLabel.place(x=10,y=205)

        changePassword = customtkinter.CTkEntry(master=settingsFrame,placeholder_text=f"*********", text_color="#000000", width=150,height=30, show="*")
        changePassword.place(x=10,y=230)

        apiLabel = customtkinter.CTkLabel(master=settingsFrame, text="Api Anahtarı", font=("Default", 18,"bold"), text_color="#000000")
        apiLabel.place(x=10,y=270)

        changeApi = customtkinter.CTkEntry(master=settingsFrame,placeholder_text=f"{settingsJson['SMTPKEY']}", text_color="#000000", width=150,height=30, show="*")
        changeApi.place(x=10,y=295)

        saveOpt = customtkinter.CTkButton(master=settingsFrame,text="Kaydet", fg_color="#21EE06", hover_color="#24E70A", width=200,height=35, text_color="#000000", font=("Kanit", 18,"bold"))
        saveOpt.place(x=40,y=335)

    def event_DeepUserManagement(self, activeIndex : str = None):
        with open("Data/Profiles/Users.json", "r") as f:
            self.usersData = json.load(f)
        userSurname = self.usersData[activeIndex]["Surname"]
        userGender = self.usersData[activeIndex]["Gender"]
        userAge = self.usersData[activeIndex]["Age"]
        userTotalExercises = self.usersData[activeIndex]["Total_Exercises"]
        UserImageN = Image.open(self.usersData[activeIndex]["ProfilePic"])

        def round_corners(img: Image.Image, radius: int) -> Image.Image:
            img = img.convert("RGBA")

            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)
            img.putalpha(mask)
            return img

        UserImage = round_corners(UserImageN, radius=30)

        UserInfo = customtkinter.CTkToplevel(master=self.doctorPage,fg_color="#FFFFFF")
        UserInfo.title(f"MEDA | {activeIndex} Derin Kontrol")
        UserInfo.resizable(width=False,height=False)
        UserInfo.geometry("400x400")
        UserInfo.grab_set()

        pywinstyles.change_header_color(UserInfo, color="#0B08AD")


        UserConfigureFrame = customtkinter.CTkFrame(master=UserInfo, width=350, height=350,corner_radius=10,border_width=0, fg_color="#E8E8DE")
        UserConfigureFrame.place(x=25,y=25)

        ConfTitle = customtkinter.CTkLabel(master=UserConfigureFrame, text="Düzenle", text_color="#000000", font=("Default", 25, "bold"))
        ConfTitle.place(x=125,y=10)

        UserNameEntry = customtkinter.CTkEntry(master=UserConfigureFrame,placeholder_text="Kullanıcı Adı", border_width=0, text_color="#000000", width=200,height=40)

        UserSurNameEntry = customtkinter.CTkEntry(master=UserConfigureFrame, placeholder_text="Kullanıcı Soy Adı",
                                               border_width=0, text_color="#000000", width=150, height=40)

        UserAgeEntry = customtkinter.CTkEntry(master=UserConfigureFrame, placeholder_text="Yaş",
                                               border_width=0, text_color="#000000", width=40, height=40)

        gender_var = tkinter.StringVar(value=userGender)
        UserGenderRadio_he = customtkinter.CTkRadioButton(master=UserConfigureFrame,text="Bay", variable=gender_var,value="Bay",border_color="#38EBF1",text_color="#000000",hover_color="#38A6AC", fg_color="#E9E7E7")
        UserGenderRadio_she = customtkinter.CTkRadioButton(master=UserConfigureFrame,text="Bayan", variable=gender_var,value="Bayan",border_color="#38EBF1",text_color="#000000",hover_color="#38A6AC", fg_color="#E9E7E7")


        UserNameEntry.place(x=10,y=60)
        UserSurNameEntry.place(x=10,y=115)
        UserAgeEntry.place(x=170,y=115)
        UserGenderRadio_he.place(x=10,y=160)
        UserGenderRadio_she.place(x=70,y=160)

        UserFrame = customtkinter.CTkFrame(master=UserInfo,width=350,height=350,corner_radius=10,border_width=0,fg_color="#E8E8DE")
        UserFrame.place(x=25,y=25)


        def frameUpper(widget: tkinter.Frame):
            widget.tkraise()

        def deleteUser():
            if self.config['MEDA Settings']['msgbox_delay'] == "TRUE":
                fade_delay = 1

            elif self.config['MEDA Settings']['msgbox_delay'] == "FALSE":
                fade_delay = 0
            deleteResponse = CTkMessagebox(title="Kullanıcı İşlem",message="Kullanıcı silinecektir, bu işlem kullanıcıyı kalıcı olarak siler. Onaylıyor musunuz?", icon="info",option_1="Tamam",option_2="İptal", sound=True,fade_in_duration=fade_delay)
            if deleteResponse.get() == "Tamam":
                with open("Data/Profiles/Users.json", "r") as f:
                    deleteUserData = json.load(f)

                try:
                    os.remove(f"Data\\Logs\\Patients\\{activeIndex}.json")
                except:
                    pass

                del deleteUserData[activeIndex]

                with open("Data/Profiles/Users.json", "w") as f:
                    json.dump(deleteUserData, f, ensure_ascii=False, indent=4)

                UserInfo.destroy()
                self.event_MSGBOX(mTitle="Kullanıcı İşlem", mText="Kullanıcı silindi ve bir daha geri döndürülemez.", TheCode="check")
                self.renewList(listF=self.usfUSERLIST)
            elif deleteResponse.get() == "İptal":
                return

        def exportUser():
            with open("Data/Profiles/Users.json", "r") as f:
                exportData = json.load(f)

            exportDist = tkinter.filedialog.asksaveasfile(confirmoverwrite=True,title="Aktarma Dosyası",defaultextension=".json", filetypes=((".json Dosyaları","*.json"),), initialdir=os.path.join("Exports"), initialfile=f"{activeIndex}-EXPORTED.json")

            if exportDist:
                exportUserData = exportData.get(activeIndex)
                json.dump({activeIndex : exportUserData}, exportDist, ensure_ascii=False, indent=4)

        def reConfUser():
            with open("", "r") as f:
                reconfdata = json.load(f)

            


        IMGLabel = customtkinter.CTkLabel(master=UserFrame, text="",image=CTkImage(light_image=UserImage,size=(140,140)),fg_color="#E8E8DE")
        IMGLabel.place(x=205,y=15)
        UserInfoFrame = customtkinter.CTkFrame(master=UserFrame,width=185,height=250,corner_radius=10,border_width=0,fg_color="#FFFFFF")
        UserInfoFrame.place(x=15,y=15)
        InfoTitle = customtkinter.CTkLabel(master=UserInfoFrame,text="Kayıtlı Hasta", text_color="#000000",font=("Default",25,"bold"))
        InfoTitle.place(x=15,y=15)
        UserNameLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"İsim : {activeIndex}",
                                               font=("Ariel",15),text_color="#000000",fg_color="#1DE8AB",corner_radius=10)
        UserSurNameLabel = customtkinter.CTkLabel(master=UserInfoFrame, text=f"Soyisim : {userSurname}",
                                              font=("Ariel", 15), text_color="#000000", fg_color="#1DE8AB",corner_radius=10)
        UserAgeLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"Yaş : {userAge}", font=("Ariel", 15),fg_color="#1DE8AB",corner_radius=10,
                                              text_color="#000000")
        UserTotalExerciseLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"Toplam Egzersiz : {userTotalExercises}", font=("Ariel", 15),
                                                        text_color="#000000",fg_color="#0EE872",corner_radius=10)
        UserGenderLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"Cinsiyet : {userGender}", font=("Ariel", 15), text_color="#000000",fg_color="#0EE872",corner_radius=10)


        UserNameLabel.place(x=15,y=60)
        UserSurNameLabel.place(x=15,y=90)
        UserAgeLabel.place(x=15,y=120)
        UserTotalExerciseLabel.place(x=15,y=160)
        UserGenderLabel.place(x=15,y=190)

        ManageUser = customtkinter.CTkButton(master=UserFrame, text="Kullanıcı Düzenle", fg_color="#2EE1E7",font=("Kanit",18,"bold"), hover_color="#22D2E7",
                                             text_color="#000000", width=100, height=40, command=lambda:frameUpper(UserConfigureFrame))
        ManageUser.place(x=15,y=285)

        DeleteUser = customtkinter.CTkButton(master=UserFrame, text="Kullanıcı Sil", fg_color="#E7191F",font=("Kanit",18,"bold"), hover_color="#BA191F",
                                             text_color="#000000", width=125, height=40, command=deleteUser)
        DeleteUser.place(x=200,y=285)

        ExportUserDatas = customtkinter.CTkButton(master=UserFrame, text="", fg_color="#F1DD0B", hover_color="#C9B50B",
                                             text_color="#000000", width=125, height=40, image=CTkImage(light_image=Image.open("Assets\\Button\\export.png"), size=(76,76)),
                                                  command=exportUser)
        ExportUserDatas.place(x=210,y=175)

    def event_UserList(self,activeIndex : str = None):
        with open("Data/Profiles/Users.json", "r") as f:
            self.usersData = json.load(f)
        userSurname = self.usersData[activeIndex]["Surname"]
        userGender = self.usersData[activeIndex]["Gender"]
        userAge = self.usersData[activeIndex]["Age"]
        userTotalExercises = self.usersData[activeIndex]["Total_Exercises"]
        UserImageN = Image.open(self.usersData[activeIndex]["ProfilePic"])

        def round_corners(img: Image.Image, radius: int) -> Image.Image:
            img = img.convert("RGBA")

            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)
            img.putalpha(mask)
            return img

        UserImage = round_corners(UserImageN, radius=30)

        UserInfo = customtkinter.CTkToplevel(master=self.doctorPage,fg_color="#FFFFFF")
        UserInfo.title(f"MEDA | {activeIndex} Sayfası")
        UserInfo.resizable(width=False,height=False)
        UserInfo.geometry("400x400")
        UserInfo.grab_set()

        pywinstyles.change_header_color(UserInfo, color="#0B08AD")


        MailFrame_Send = customtkinter.CTkFrame(master=UserInfo,width=350,height=350,corner_radius=10,border_width=0,fg_color="#E8E8DE")
        MailFrame_Send.place(x=25,y=25)
        MailFrame_Get = customtkinter.CTkFrame(master=UserInfo,width=350,height=350,corner_radius=10,border_width=0,fg_color="#E8E8DE")
        MailFrame_Get.place(x=25,y=25)

        self.ExerciseList = {
            "Squat" : 0,
            "Kollar Yana" : 0,
            "Kollar Öne" : 0,
            "Topuk Kaldırma" : 0
        }

        # Sender Frame

        def InputDialog(exerciseType : str = "Squat"):
            ExersiceDialog = customtkinter.CTkInputDialog(text=f"Miktar: ", title=f"Egzersiz : {exerciseType}")
            self.ExerciseList[exerciseType] = int(ExersiceDialog.get_input())
            print(self.ExerciseList)

        def listExercise():
            message = "\n".join(f"{key}: {value}" for key, value in self.ExerciseList.items())
            self.event_MSGBOX(mTitle="Egzersiz Listesi", mText=message, TheCode="info")

        def sendmailtouser():
            print(["[I] Opening Datas..."])
            with open("Data\\Profiles\\Users.json", "r") as f:
                data = json.load(f)

            with open("Data\\Json\\Data.json", "r") as f:
                doctorData = json.load(f)

            print(["[OK] Completed!"])
            print(["[!] Sending Mail..."])

            try:
                mailApi.SendExercise(
                    smtp_server="smtp.gmail.com",
                    smtp_port=587,
                    smtp_user=doctorData["Mail"],
                    smtp_password=doctorData["SMTPKEY"],
                    senderUser=doctorData["Username"],
                    patient_email=data[activeIndex]["email"],
                    patient_name=activeIndex,
                    a=self.ExerciseList["Squat"],
                    b=self.ExerciseList["Kollar Yana"],
                    c=self.ExerciseList["Kollar Öne"],
                    d=self.ExerciseList["Topuk Kaldırma"],
                )
                print(["[OK] Mail gönderildi!"])
                self.event_MSGBOX(mTitle="Mail Gönderildi", mText="Mail Başarıyla Gönderilmiştir.", TheCode="check")
                exerciseApi.addLogs(Squat=self.ExerciseList["Squat"],Kollar=self.ExerciseList["Kollar Öne"], Yana=self.ExerciseList["Kollar Yana"], Topuk=self.ExerciseList["Topuk Kaldırma"])
                exerciseApi.addLogs(Squat=self.ExerciseList["Squat"], Kollar=self.ExerciseList["Kollar Öne"],
                                    Yana=self.ExerciseList["Kollar Yana"], Topuk=self.ExerciseList["Topuk Kaldırma"],Username=activeIndex)
                exerciseApi.addLogs(Squat=self.ExerciseList["Squat"], Kollar=self.ExerciseList["Kollar Öne"],
                                    Yana=self.ExerciseList["Kollar Yana"], Topuk=self.ExerciseList["Topuk Kaldırma"],Username=activeIndex, CreateUserLog=True)

            except Exception as e:
                import traceback
                print("E-posta gönderme hatası:", type(e), str(e))
                traceback.print_exc()

        SenderTitle = customtkinter.CTkLabel(master=MailFrame_Send,text="Egzersizler",text_color="#000000",font=("Kanit",25,"bold"))
        SenderTitle.place(x=110,y=20)


        SquatButton = customtkinter.CTkButton(master=MailFrame_Send,text="Squat", font=("Default",17,"bold"), fg_color="#457EE8",width=200,height=35,command=lambda:InputDialog(exerciseType="Squat"))
        SquatButton.place(x=75,y=60)

        ArmLeftRightButton = customtkinter.CTkButton(master=MailFrame_Send,text="Kolları Yana Aç", font=("Default",17,"bold"), fg_color="#457EE8",width=200,height=35,command=lambda:InputDialog(exerciseType="Kollar Yana"))
        ArmLeftRightButton.place(x=75,y=105)

        ArmFrontButton = customtkinter.CTkButton(master=MailFrame_Send,text="Kolları Öne Aç", font=("Default",17,"bold"), fg_color="#457EE8",width=200,height=35,command=lambda:InputDialog(exerciseType="Kollar Öne"))
        ArmFrontButton.place(x=75,y=150)

        feetUpButton = customtkinter.CTkButton(master=MailFrame_Send,text="Topuk Kaldırma", font=("Default",17,"bold"), fg_color="#457EE8",width=200,height=35, command=lambda:InputDialog(exerciseType="Topuk Kaldırma"))
        feetUpButton.place(x=75,y=195)

        listButton = customtkinter.CTkButton(master=MailFrame_Send,text="Liste", font=("Default",17,"bold"), fg_color="#17BED4",width=200,height=35,command=listExercise)
        listButton.place(x=75,y=250)

        SendMail = customtkinter.CTkButton(master=MailFrame_Send,text="Gönder", fg_color="#2DE82C", corner_radius=10,font=("Kanit",17,"bold"),text_color="#000000",width=150,height=40,
                                           command=lambda:threading.Thread(target=sendmailtouser()).start(), hover_color="#2DC02D")
        SendMail.place(x=25,y=300)
        Back = customtkinter.CTkButton(master=MailFrame_Send,text="Geri", fg_color="#E8E80C", corner_radius=10,font=("Kanit",17,"bold"),text_color="#000000",width=150,height=40,
                                       command=lambda:frameUpper(UserFrame), hover_color="#D3D314")
        Back.place(x=178,y=300)

        # Get Frame

        Back = customtkinter.CTkButton(master=MailFrame_Get,text="Geri", fg_color="#E8E80C", corner_radius=10,font=("Kanit",17,"bold"),text_color="#000000",width=150,height=40,
                                       command=lambda:frameUpper(UserFrame), hover_color="#D3D314")
        Back.place(x=178,y=300)

        UserFrame = customtkinter.CTkFrame(master=UserInfo,width=350,height=350,corner_radius=10,border_width=0,fg_color="#E8E8DE")
        UserFrame.place(x=25,y=25)

        def frameUpper(widget: tkinter.Frame):
            widget.tkraise()

        IMGLabel = customtkinter.CTkLabel(master=UserFrame, text="",image=CTkImage(light_image=UserImage,size=(140,140)),fg_color="#E8E8DE")
        IMGLabel.place(x=205,y=15)

        UserInfoFrame = customtkinter.CTkFrame(master=UserFrame,width=185,height=250,corner_radius=10,border_width=0,fg_color="#FFFFFF")
        UserInfoFrame.place(x=15,y=15)

        InfoTitle = customtkinter.CTkLabel(master=UserInfoFrame,text="Kayıtlı Hasta", text_color="#000000",font=("Default",25,"bold"))
        InfoTitle.place(x=15,y=15)

        UserNameLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"İsim : {activeIndex}",
                                               font=("Ariel",15),text_color="#000000",fg_color="#1DE8AB",corner_radius=10)
        UserSurNameLabel = customtkinter.CTkLabel(master=UserInfoFrame, text=f"Soyisim : {userSurname}",
                                              font=("Ariel", 15), text_color="#000000", fg_color="#1DE8AB",corner_radius=10)

        UserAgeLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"Yaş : {userAge}", font=("Ariel", 15),fg_color="#1DE8AB",corner_radius=10,
                                              text_color="#000000")

        UserTotalExerciseLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"Toplam Egzersiz : {userTotalExercises}", font=("Ariel", 15),
                                                        text_color="#000000",fg_color="#0EE872",corner_radius=10)
        UserGenderLabel = customtkinter.CTkLabel(master=UserInfoFrame,text=f"Cinsiyet : {userGender}", font=("Ariel", 15), text_color="#000000",fg_color="#0EE872",corner_radius=10)

        UserNameLabel.place(x=15,y=60)
        UserSurNameLabel.place(x=15,y=90)
        UserAgeLabel.place(x=15,y=120)


        UserTotalExerciseLabel.place(x=15,y=160)
        UserGenderLabel.place(x=15,y=190)

        SendMailToUser = customtkinter.CTkButton(master=UserFrame,text="Mail Gönder", fg_color="#2DE82C", corner_radius=10,font=("Kanit",17,"bold"),text_color="#000000",width=150,height=40,
                                                 command=lambda:frameUpper(MailFrame_Send), hover_color="#2DC02D")
        SendMailToUser.place(x=25,y=300)

        GetMailFromUser = customtkinter.CTkButton(master=UserFrame,text="Gelen Mail", fg_color="#E8E80C", corner_radius=10,font=("Kanit",17,"bold"),text_color="#000000",width=150,height=40,
                                                  command=lambda:frameUpper(MailFrame_Get),
                                                  hover_color="#D3D314")
        GetMailFromUser.place(x=178,y=300)


    def event_MSGBOX(self, mTitle, mText, TheCode, master : str = None):
        """
        Icons : Check -> Tick
        Icons : Cancel -> Cancel
        Icons : Warning -> Warn
        """

        if self.config['MEDA Settings']['msgbox_delay'] == "TRUE":
            fade_delay = 1

        elif self.config['MEDA Settings']['msgbox_delay'] == "FALSE":
            fade_delay = 0


        if master != None:
            CTkMessagebox(master=master,title=mTitle, message=mText, icon=TheCode, option_1="Tamam", sound=True, fade_in_duration=fade_delay)
        else:
            CTkMessagebox(title=mTitle,message=mText, icon=TheCode,option_1="Tamam", sound=True,fade_in_duration=fade_delay)

    def loadPFP(self):
        self.pfpPath = tkinter.filedialog.askopenfilename(title="Profil Fotoğrafı Seç",
                                                     filetypes=(("jpg Dosyaları", "*.jpg"), ("jpeg Dosyaları", "*.jpeg*"),
                                                                ("png Dosyaları", "*.png")))
        self.PFPLoadButton.configure(image=CTkImage(light_image=Image.open(self.pfpPath), size=(110, 110)))

    def renewList(self, listF):
        with open("Data/Profiles/Users.json", "r") as f:
            renewData = json.load(f)

        listF.delete(0,"end")

        for user in renewData.keys():
            listF.insert(tkinter.END, user)

class loadClient:
    def __init__(self):
        print("Client")

if __name__ == "__main__":
    app = LoadMEDA()