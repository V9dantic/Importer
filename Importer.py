from kivymd.app import MDApp
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import pandas as pd
import datetime as dt
import os
import re
import keyring

Window.size = (600, 400)
Window.minimum_width, Window.minimum_height = Window.size
sm = ScreenManager()

#keyring variables

CVR_USER = "CVR_USER"

wice_save_path = "wice_save_path"
wice_reports_path = "wice_reports_path"

close_save_path = "close_save_path"
close_imports_path = "close_imports_path"

cvr_master_path = "cvr_master_path"

# delete all passwords

# keyring.delete_password(CVR_USER, wice_save_path)
# keyring.delete_password(CVR_USER, wice_reports_path)
# keyring.delete_password(CVR_USER, close_save_path)
# keyring.delete_password(CVR_USER, close_imports_path)
# keyring.delete_password(CVR_USER, cvr_master_path)


global file
file = ""
global save
save = ""
global path_string
path_string = ""

global cvr_export

cvr_export = pd.DataFrame()

class Choose(Screen):
    pass

class Wice(Screen):
    
    def on_enter(self):
        # Überprüfen, ob der Pfad im Keyring gespeichert ist
        saved_path = keyring.get_password(CVR_USER, wice_save_path)
        if saved_path:
            self.ids.choose_dir.disabled = True
            self.ids.export_button.disabled = True
        else:
            self.reset_buttons()

    def reset_buttons(self):
        self.ids.choose_file.disabled = False
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = True

    def disable_first(self):
        self.ids.choose_file.disabled = True
        saved_path = keyring.get_password(CVR_USER, wice_save_path)
        if saved_path:
            self.ids.export_button.disabled = False
        else:
            self.ids.choose_dir.disabled = False

    def disable_second(self):
        self.ids.choose_file.disabled = True
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = False

    def save_data(self, key, data):
        keyring.set_password(CVR_USER, key, data)

    def save_path(self):
        global path_string
        saved_path = keyring.get_password(CVR_USER, wice_save_path)
        if not saved_path:
            self.save_data(wice_save_path, path_string)
        else:
            self.save_file()

    def save_file(self):
        global file
        global path_string
        file = path_string


class Close(Screen):
    
    def __init__(self, **kwargs):
        super(Close, self).__init__(**kwargs)
        self.close_save_path = "close_save_path"
        self.close_imports_path = "close_imports_path"
    
    # on enter, check if both close-paths are saved in the keyring module
    def on_enter(self):
        if keyring.get_password(CVR_USER, close_save_path) and keyring.get_password(CVR_USER, close_imports_path):
            self.ids.choose_dir.disabled = True
            self.ids.choose_file.disabled = True
            self.ids.export_button.disabled = False
    
    def disable_first(self):
        self.ids.choose_file.disabled = True
        self.ids.choose_dir.disabled = False
        self.ids.export_button.disabled = True
        
    def disable_second(self):
        self.ids.choose_file.disabled = True
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = False
        
    def disable_third(self):
        self.ids.choose_file.disabled = False
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = True
        
    def save_path(self, key):
        
        global path_string
        
        print(key)
        print(path_string)
        
        if not keyring.get_password(CVR_USER, key):
            print("Path not saved yet")
            keyring.set_password(CVR_USER, key, path_string)
        
class FinishW(Screen):
    
    def on_enter(self):
        saved_path = keyring.get_password(CVR_USER, wice_reports_path)
        if saved_path:
            self.ids.choose_dir.disabled = True
            self.ids.export_button.disabled = False
    
    def disable_first(self):
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = False
        
    def disable_third(self):
        self.ids.choose_dir.disabled = False
        self.ids.export_button.disabled = True
        
    def save_path(self):
        
        global path_string
        
        saved_path = keyring.get_password(CVR_USER, wice_reports_path)
        if saved_path:
            pass
        else:
            keyring.set_password(CVR_USER, wice_reports_path, path_string)
        
class FinishC(Screen):
    
    def on_enter(self):
        # Wenn der Pfad im Keyring gespeichert ist, deaktivieren Sie nur den choose_dir-Button
        if keyring.get_password(CVR_USER, cvr_master_path):
            self.ids.choose_dir.disabled = True
            self.ids.export_button.disabled = False
        else:
            self.reset_buttons()

    def reset_buttons(self):
        self.ids.choose_file.disabled = False
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = True

    def disable_first(self):
        if not keyring.get_password(CVR_USER, cvr_master_path):
            self.ids.choose_file.disabled = True
            self.ids.choose_dir.disabled = False
        else:
            self.ids.choose_file.disabled = True
            self.ids.choose_dir.disabled = True
            self.ids.export_button.disabled = False

    def disable_second(self):
        self.ids.choose_dir.disabled = True
        self.ids.export_button.disabled = False

    def save_data(self, key, data):
        keyring.set_password(CVR_USER, key, data)

    def save_path(self):       
        global path_string
        
        if not keyring.get_password(CVR_USER, cvr_master_path):
            self.save_data(cvr_master_path, path_string)
        else:
            self.save_file()

    def save_file(self):
        global file
        global path_string
        file = path_string
        
class Importer(MDApp):
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        self.second = False
        self.path = ""
        
        self.file_manager_obj = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager,
            search="all",
            sort_by="date",
        )
    
    def build(self):
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        
        sm.add_widget(Choose(name="Choose"))
        sm.add_widget(Wice(name="Wice"))
        sm.add_widget(FinishW(name="FinishW"))
        sm.add_widget(Close(name="Close"))
        sm.add_widget(FinishC(name="FinishC"))
        
        return sm
    
    def delete_passwords(self):
        # Liste der Passwörter, die gelöscht werden sollen
        passwords_to_delete = [wice_save_path, wice_reports_path, close_save_path, close_imports_path, cvr_master_path]

        for password in passwords_to_delete:
            try:
                keyring.delete_password(CVR_USER, password)
                print(f"Pfad für {password} wurde gelöscht.")
            except keyring.errors.PasswordDeleteError:
                print(f"Kein Pfad gefunden für {password}.")
        
        # Optional: Eine Benachrichtigung anzeigen, dass die Passwörter gelöscht wurden
        toast("Alle Pfade wurden gelöscht!", duration=5)

    
    def open_file_manager(self):
        
        # Öffnen des Dateimanagers auf dem PC internen Speicher
        self.file_manager_obj.show("C:/Users/")

    def select_path(self, path):
        
        global path_string
        
        path = path.replace("\\", "/")
        print(path)
        self.exit_manager()
        toast(path)
        self.path = path
        
        path_string = path

    def exit_manager(self, *args):

        self.manager_open = False
        self.file_manager_obj.close()

    def import_wice(self):
        try:
            global cvr_export
            global file
            # Check if files exist
            if not os.path.exists("Wice_Report_Master.xlsx") or not os.path.exists(file):
                raise FileNotFoundError("Required input files not found")
                
            save = keyring.get_password(CVR_USER, wice_save_path)
            
            # Load data with error handling
            try:
                export = pd.read_excel("Wice_Report_Master.xlsx")
                df = pd.read_csv(file, index_col=False, encoding="utf-8")
            except Exception as e:
                raise Exception(f"Error reading input files: {str(e)}")

            cvr_export = df

            # Verify required columns exist
            required_columns = [
                "last_activity_date", "lead_name", "description", "status_label",
                "primary_contact_first_name", "primary_contact_last_name",
                "primary_contact_title", "primary_contact_primary_phone",
                "primary_contact_other_phones", "primary_contact_primary_email",
                "custom.DUNS-Nummer", "custom.Quelle", "custom.Tag",
                "custom.Verantwortlich.name", "last_call_note", "next_task_text",
                "num_calls", "num_emails", "next_task_date"
            ]
            
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")

            # Process dates safely
            def parse_date(date_str):
                if pd.isna(date_str):
                    return None
                try:
                    # Handle different possible date formats
                    if 'T' in str(date_str):
                        date_part = str(date_str).split('T')[0]
                    else:
                        date_part = str(date_str)
                        
                    date_obj = pd.to_datetime(date_part)
                    return date_obj.strftime("%d.%m.%Y")
                except:
                    return None

            # Create a copy of df to avoid modification during iteration
            df_filtered = df.copy()
            
            # Process last activity dates
            df_filtered['parsed_date'] = df_filtered['last_activity_date'].apply(parse_date)
            df_filtered['date_obj'] = pd.to_datetime(df_filtered['parsed_date'], format='%d.%m.%Y', errors='coerce')
            
            # Filter dates
            today = dt.datetime.today()
            mask = (df_filtered['date_obj'].notna() & 
                    (df_filtered['date_obj'] <= today) & 
                    (today - df_filtered['date_obj'] <= pd.Timedelta(days=10)))
            
            df_filtered = df_filtered[mask]

            # Update export dataframe
            column_mapping = {
                'lead_name': 'lead_name',
                'description': 'description',
                'status_label': 'status_label',
                'primary_contact_first_name': 'primary_contact_first_name',
                'primary_contact_last_name': 'primary_contact_last_name',
                'primary_contact_title': 'primary_contact_title',
                'primary_contact_primary_phone': 'primary_contact_primary_phone',
                'primary_contact_other_phones': 'primary_contact_other_phones',
                'primary_contact_primary_email': 'primary_contact_primary_email',
                'custom.DUNS-Nummer': 'DUNS-Nummer',
                'custom.Quelle': 'custom.Quelle',
                'custom.Tag': 'custom.Tag',
                'custom.Verantwortlich.name': 'custom.Verantwortlich.name',
                'last_call_note': 'last_call_note',
                'next_task_text': 'next_task_text',
                'num_calls': 'num_calls',
                'num_emails': 'num_email'
            }

            # Update export dataframe with filtered data
            export['date_updated'] = df_filtered['parsed_date']
            for source, target in column_mapping.items():
                export[target] = df_filtered[source]

            # Process next task dates
            export['next_task_date'] = df_filtered['next_task_date'].apply(parse_date)

            # Remove rows with no date_updated
            export = export[export['date_updated'].notna()]

            # Save the result
            export_date = dt.datetime.today().strftime("%d_%m_%Y")
            output_path = os.path.join(save, f"Wice_Report_{export_date}.xlsx")
            
            export.to_excel(output_path, index=False)
            toast("Export abgeschlossen! Du findest ihn nun an dem von dir ausgewählten Speicherort!", duration=5)
            
            sm.transition.direction = "right"
            sm.current = "FinishW"
            
        except Exception as e:
            toast(f"Fehler beim Import: {str(e)}", duration=5)
            return None
        
    def import_wice_upload(self):
        
        global cvr_export
        
        export = pd.read_excel("Wice_Report_Master.xlsx")
        # df = pd.read_csv(file, index_col=False, encoding="utf-8")
        df = cvr_export
        
        export["lead_name"] = df["lead_name"]
        export["description"] = df["description"]
        export["status_label"] = df["status_label"]
        export["primary_contact_first_name"] = df["primary_contact_first_name"]
        export["primary_contact_last_name"] = df["primary_contact_last_name"]
        export["primary_contact_title"] = df["primary_contact_title"]
        export["primary_contact_primary_phone"] = df["primary_contact_primary_phone"]
        export["primary_contact_other_phones"] = df["primary_contact_other_phones"]
        export["primary_contact_primary_email"] = df["primary_contact_primary_email"]
        export["DUNS-Nummer"] = df["custom.DUNS-Nummer"]
        export["custom.Quelle"] = df["custom.Quelle"]
        export["custom.Tag"] = df["custom.Tag"]
        export["custom.Verantwortlich.name"] = df["custom.Verantwortlich.name"]
        export["last_call_note"] = df["last_call_note"]
        export["next_task_text"] = df["next_task_text"]
        export["num_calls"] = df["num_calls"]
        export["num_email"] = df["num_emails"]
        
        date1 = []

        for name in df["last_activity_date"]:
            
            if str(name) != "nan":
                
                a, b, c = str(name).split("-")
                c = c.split("T")[0] 
                out1 = str(c + "." + b + "." + a)
                out1 = dt.datetime.strptime(out1, "%d.%m.%Y")
                print(out1)
            
            date1.append(out1)
            
        export["date_updated"] = date1

        i = 0

        for name in df["next_task_date"]:
            
            if str(name) != "nan":
                
                a, b, c = str(name).split("-")
                c = c.split("T")[0]
                out2 = str(c + "." + b + "." + a)
                out2 = dt.datetime.strptime(out2, "%d.%m.%Y")
                export.iloc[i, 15] = out2
                
                print(out2)
                
            i = i + 1
        
        export.sort_values("date_updated", ascending=True, inplace=True)
        
        partner = pd.Series(export["custom.Quelle"].unique())

        dir = keyring.get_password(CVR_USER, wice_reports_path) + "/"

        for name in partner:
    
            try:
                
                print(name)
                tempPartner = export[export["custom.Quelle"]==name]
                tempPartner.sort_index(ascending=False, inplace=True)
                writer = pd.ExcelWriter(dir + str(name) + " CVR Report.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay')
                tempPartner.to_excel(writer, index=False, sheet_name='CVR Report', startrow=writer.sheets['CVR Report'].max_row, header=None)
                writer.close()

            except Exception as e:
                
                ### TODO: Fix No Report Cases
                
                print(dir + str(name))
                print(f"Fehler: {e}")
                print(f"Fehlertyp: {type(e)}")
                
        toast("Reports erfolgreich aktualisiert!!!", duration=5)    
        sm.transition.direction = "left"
        sm.current = "Choose"
                
    def import_close(self):
        
        dir = keyring.get_password(CVR_USER, close_imports_path) + "/"
        
        close_import = pd.DataFrame()

        for files in os.listdir(dir):
            
            if files.endswith(".xlsx") and not files.startswith("A_Import"):

                print(dir+files)
                
                try:

                    df = pd.read_excel(dir+files)
                    writer = pd.ExcelWriter(dir+files, engine='openpyxl', mode='a', if_sheet_exists='overlay')
                    workbook=writer.book
                    
                    eP = str(files).split("_")[0] + " " + str(files).split("_")[1]
                    
                    df_out = df[df["CVR Media Import"].isna()]
                    df_out = df_out[df_out["Telefon Zentrale"].notna()]
                    df_out = df_out[df_out["Organisation (Unternehmen)"].notna()]
                    df_out["ERA-Partner"] = eP

                    close_import = pd.concat([close_import, df_out])

                    df["CVR Media Import"] = df["CVR Media Import"].fillna(dt.datetime.today().strftime("%d.%m.%Y"))

                    df.to_excel(writer, sheet_name='Import', index=False)
                    writer.close()
                    
                except Exception as e:
                    # Hier erfassen wir den Fehler und geben Informationen darüber aus
                    print(files + " fehlgeschlagen!!!")
                    print(f"Fehler: {e}")
                    print(f"Fehlertyp: {type(e)}")
                    
        for spalte in close_import.columns:

            if str(spalte).startswith("Spalte") or str(spalte).startswith("Unnamed") or str(spalte).startswith("Straße.1") or str(spalte).startswith("nicht mehr CVR"):

                close_import.drop(columns=spalte, inplace=True)

        close_import["Status"] = "Neu" 
        close_import["Importiert"] = dt.datetime.today().strftime("%d.%m.%Y")
        # close_import.drop(columns="TM", inplace=True)

        columns = pd.read_excel("Usage/A_Import-Master.xlsx", index_col=False)
        close_import.columns = columns.columns

        close_import["Quelle"] = close_import["Phone (formatted)"]
        close_import["Country"] = "Germany"
        
                # Konvertieren Sie die Datumsfelder in ein datetime-Objekt
        close_import["Lieferdatum"] = pd.to_datetime(close_import["Lieferdatum"], errors='coerce')

        # Ersetzen Sie NaN-Werte durch das vorherige gültige Datum
        close_import["Lieferdatum"].fillna(method='ffill', inplace=True)

        # Konvertieren Sie die Datumsfelder zurück in einen String mit einem einheitlichen Format
        close_import["Lieferdatum"] = close_import["Lieferdatum"].dt.strftime("%d.%m.%Y")


        close_import.reset_index(inplace=True, drop=True)

        for index, row in close_import.iterrows():

            if row["Quelle"] == "Markus Lang":

                close_import.iloc[index, 22] = "Dr. Markus Lang"

            if row["Quelle"] == "Reinhard Rolf":

                close_import.iloc[index, 22] = "Dr. Reinhard Rolf"

            if row["Quelle"] == "Stefan Leppelmann":

                close_import.iloc[index, 22] = "Dr. Stefan Leppelmann"
                
            if row["Quelle"] == "Harald Matthias":

                close_import.iloc[index, 22] = "Harald Matthias Meyer"
                
            if row["Quelle"] == "Michels Wagenblast":

                close_import.iloc[index, 22] = "Dr. Joachim Wagenblast"
                
            if row["Quelle"] == "Volker Worringer":

                close_import.iloc[index, 22] = "Antonio Sousa de Brito"
                
            if row["Quelle"] == "Geist Wieland":

                close_import.iloc[index, 22] = "Volker Wieland"
                
            if row["Quelle"] == "CVR Import":
                    
                    close_import.iloc[index, 22] = "Thomas Müller"

            if row["Quelle"] == "Claas Seefeld":
                    
                    close_import.iloc[index, 22] = "Prof. Dr. Claas Ole Seefeld"

        cals = pd.read_excel("Usage/Partner_Kalender_Duos.xlsx", index_col=False)

        close_import = pd.merge(close_import, cals, left_on="Quelle", right_on="Alle ERA Partner", how="left")
        close_import["Kalender"] = close_import["ERA Calendar"]
        close_import.drop(columns="ERA Calendar", inplace=True)
        close_import.drop(columns="Alle ERA Partner", inplace=True)

        def clean_phone_number(num, default_country_code='49'):
            if pd.isna(num):
                return ''
            
            # Schritt 1: Entferne unerwünschte Präfixe und Zeichen
            num = str(num).strip().replace('tel:', '').replace(' ', '').replace('-', '').replace('/', '').replace('–', '').replace('.', '')
            
            # Schritt 2: Überprüfe und entferne '(0)', wenn vorhanden
            if '(0)' in num:
                num = num.replace('(0)', '')
                zero_present = True
            else:
                zero_present = False
            
            # Schritt 3: Definiere Ländervorwahlen mit ihrem Standardformat
            country_codes = {
                '49': '+49 (0) ',
                '43': '+43 (0) ',
                '41': '+41 (0) ',
                # Weitere Ländervorwahlen können hier hinzugefügt werden
            }
            
            # Schritt 4: Funktion zur Erkennung der Ländervorwahl
            def find_country_code(n):
                for code in sorted(country_codes.keys(), key=lambda x: -len(x)):
                    if n.startswith(code):
                        return code
                return None
            
            # Schritt 5: Verarbeitung basierend auf dem Präfix der Telefonnummer
            if num.startswith('+'):
                # Entferne das '+' Zeichen
                num_body = num[1:]
                code = find_country_code(num_body)
                if code:
                    rest = num_body[len(code):]
                    formatted_number = f"{country_codes[code]}{rest}"
                    return formatted_number
                else:
                    # Unbekannte Ländervorwahl, behalte das ursprüngliche Format bei
                    return num
            elif num.startswith('00'):
                # Ersetze '00' durch '+' und rekursiver Aufruf
                num = '+' + num[2:]
                return clean_phone_number(num, default_country_code)
            elif num.startswith('0'):
                # Nationale Nummer, ersetze '0' durch die Standard-Ländervorwahl
                rest = num[1:]
                formatted_number = f"{country_codes.get(default_country_code, f'+{default_country_code} (0) ')}{rest}"
                return formatted_number
            else:
                # Testen, ob die Nummer ohne Präfix eine Ländervorwahl enthält
                code = find_country_code(num)
                if code:
                    rest = num[len(code):]
                    formatted_number = f"{country_codes[code]}{rest}"
                    return formatted_number
                else:
                    # Keine Präfix, füge die Standard-Ländervorwahl hinzu
                    formatted_number = f"{country_codes.get(default_country_code, f'+{default_country_code} (0) ')}{num}"
                    return formatted_number

        # Apply the function to both phone number columns and store in new columns
        phone_columns = ["Phone(unformatted)", "Directphone", "Directphone.1"]
        formatted_columns = ["Phone (formatted)", "Directphone", "Directphone.1"]

        for original_col, formatted_col in zip(phone_columns, formatted_columns):
            close_import[formatted_col] = close_import[original_col].apply(clean_phone_number)
                
        # Funktion zur Bereinigung der URL
        def clean_url(url):
            if pd.isna(url):
                return ''
            url = url.strip()
            
            # Entferne 'https://' oder 'http://' am Anfang
            if url.lower().startswith('https://'):
                url = url[8:]
            elif url.lower().startswith('http://'):
                url = url[7:]
            
            # Ersetze ', ' durch ', http://'
            url = url.replace(', ', ', http://')
            url = url.strip()
            
            # Füge 'http://' am Anfang hinzu
            url = 'http://' + url
            return url

        # Funktion zum Extrahieren des ersten Wertes und Validierung der E-Mail
        def get_first_valid_email(cell):
            if pd.isna(cell):
                return ''
            # Teile die Zelle bei ','
            values = str(cell).split(',')
            if not values:
                return ''
            first_email = values[0].strip()
            # Überprüfe, ob '@' in der E-Mail vorhanden ist
            if '@' in first_email and first_email.count('@') == 1:
                return first_email
            else:
                return ''

        # Funktion zum Extrahieren des ersten Wertes und Validierung der URL
        def get_first_valid_url(cell):
            if pd.isna(cell):
                return ''
            # Teile die Zelle bei ','
            values = str(cell).split(',')
            if not values:
                return ''
            first_url = values[0].strip()
            # Liste erlaubter Domain-Endungen
            allowed_tlds = ['.de', '.com', '.net', '.org', '.info', '.biz', '.eu', '.co.uk']
            # Überprüfe, ob die URL mit einer erlaubten TLD endet
            first_url_lower = first_url.lower()
            if any(first_url_lower.endswith(tld) for tld in allowed_tlds):
                return first_url
            else:
                return ''

        # Anwendung der Bereinigungsfunktion auf die 'URL' Spalte
        close_import['URL'] = close_import['URL'].apply(clean_url)

        # Anwendung der Funktion zum Extrahieren des ersten Wertes auf die 'Email' und 'URL' Spalten
        close_import['Email'] = close_import['Email'].apply(get_first_valid_email)
        close_import['Email.1'] = close_import['Email.1'].apply(get_first_valid_email)
        close_import['URL'] = close_import['URL'].apply(get_first_valid_url)

        def determine_country_from_phone(phone_number):
            """Determines country based on phone number prefix"""
            if pd.isna(phone_number):
                return 'Germany'  # Default value
                
            phone = str(phone_number).strip()
            
            # Check for different formats of country codes
            if '+49' in phone or '(49)' in phone:
                return 'Germany'
            elif '+43' in phone or '(43)' in phone:
                return 'Austria'
            elif '+41' in phone or '(41)' in phone:
                return 'Switzerland'
            
            return 'Germany'  # Default if no match

        # Add this line after the phone number formatting section:
        close_import['Country'] = close_import['Phone (formatted)'].apply(determine_country_from_phone)
      
        export_date = dt.datetime.today()
        export_date = export_date.strftime("%d_%m_%Y")
        
        save = keyring.get_password(CVR_USER, close_save_path)
        
        close_import.to_excel(f"{save}/close_import_{export_date}.xlsx", index=False)
        
        toast("Import abgeschlossen! Du findest ihn nun an dem von dir ausgewählten Speicherort!", duration=5)
        
        sm.transition.direction = "left"
        sm.current = "FinishC"
        
    def import_close_upload(self):
        
        master = keyring.get_password(CVR_USER, cvr_master_path)
        
        close_import = pd.read_excel(file, index_col=False, sheet_name="Sheet1")
        
        # Check if "Importiert" column is in datetime format, if not convert it
        if not isinstance(close_import['Importiert'].iloc[0], pd.Timestamp):
            close_import['Importiert'] = pd.to_datetime(close_import['Importiert'], errors='coerce')
        
        # Drop column "Phone (unformatted)" so that the columns are the same as in the master
        
        close_import.drop(columns="Phone(unformatted)", inplace=True)
        
        # Add new columns for the month and calendar week derived from the "Importiert" column
        close_import['Monat'] = close_import['Importiert'].dt.month
        close_import['Kalenderwoche'] = close_import['Importiert'].dt.isocalendar().week

        aggregated_data = close_import.groupby(['Quelle', 'Monat', 'Kalenderwoche'])['Company'].nunique().reset_index(name='Anzahl Firmen')
        
        toast("Das Hochladen des Imports kann einige Minuten dauern...", duration=5)
        
        writer = pd.ExcelWriter(master, if_sheet_exists="overlay", mode="a", engine="openpyxl")
        workbook=writer.book
        close_import.to_excel(writer, index=False, sheet_name='Leads', startrow=writer.sheets["Leads"].max_row, header=None)
        aggregated_data.to_excel(writer, index=False, sheet_name='Daten', startrow=writer.sheets["Daten"].max_row, header=None)
        writer.close()
        
        toast("Import hochgeladen! Du findest ihn nun an dem von dir ausgewählten Speicherort!", duration=5)
        
Importer().run()