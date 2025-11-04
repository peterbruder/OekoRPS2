import streamlit as st
from datetime import date
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="OekoRPS")

# Custom CSS to hide the + and - buttons
hide_buttons_css = """
    <style>
    .stNumberInput button.step-up, .stNumberInput button.step-down {
        display: none;
    }
    </style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(hide_buttons_css, unsafe_allow_html=True)

# Funktion zur Initialisierung der Session State Variablen
def initialize_session_state():
    if 'vehicle_list' not in st.session_state:
        st.session_state['vehicle_list'] = []

# Funktion zur Anzeige der Sidebar
def show_sidebar():
    st.sidebar.image("Logo_of_Fachhochschule_Münster.png", use_container_width=True)
    st.sidebar.markdown("""
        <style>
            .css-18e3th9 {  
                width: 50x;  
                position: fixed;
                right: 0;
                top: 0;
                height: 100%;
                margin-top: 0;
            }
            .css-1l02zno {  
                margin-left: auto;
            }
        </style>
    """, unsafe_allow_html=True)

# Funktion zur Validierung der Eingaben
def validate_input(text):
    return text.isdigit()

def validate_input_int(text):
    try:
        value = int(text)
        return 0 <= value <= 100
    except ValueError:
        return False

# Funktion zur Darstellung der Methodik-Sektion
def show_methodik_section():
    st.subheader("Methodik der Ökobilanzierung")
    with st.expander("**Methodik**"):
        st.write("Die methodische Vorgehensweise dieser Studie besteht darin, zunächst zu ermitteln, wie viele Fahrgäste das Ridepooling-System transportiert und wie viel Energie dabei verbraucht wird. Dieser Energieverbrauch wird auf eine vergleichbare Einheit umgerechnet, den Energieverbrauch pro Personenkilometer. Anschließend wird die Transportleistung des Ridepooling-Systems mit dem Mobilitätsverhalten verglichen, welches ohne ein Ridepooling-System auftreten würde, also mit den alternativ genutzten Verkehrsmitteln. Diese Vorgehensweise ermöglicht es, die ökologische Effizienz des Ridepooling-Systems objektiv bewerten zu können. Der Prozess wird in der untenstehenden Abbildung veranschaulicht.")
        st.image('Abbildung_Methodik.png', use_container_width=True)
        st.info("**Hinweis:** Bitte gehen Sie bei der Bearbeitung sukzessiv vor. Die Reihenfolge der Schritte ist vorgegeben und kann nicht verändert werden. Nähere Informationen zur Bearbeitung können Sie folgendem Dokument entnehmen: [FH Münster](https://www.fh-muenster.de/)")

# Funktion zur Darstellung der Allgemeinen Informationen
# Funktion zur Darstellung der Allgemeinen Informationen
def show_general_info():
    with st.expander("**1. Allgemeine Informationen**"):
        st.info("**Hinweis:** Bitte geben Sie zunächst allgemeine Informationen zum Ridepooling-System an. Bitte berücksichtigen Sie den Betrachtungszeitraum, auf welchen sich die folgenden Angaben beziehen.")
        name_ridepooling_system = st.text_input("Name des Ridepooling-Systems:")
        start_date = st.date_input("Beginn Betrachtungszeitraum:", date(2022, 1, 1))
        end_date = st.date_input("Ende Betrachtungszeitraum:", date(2022, 12, 31))

        st.session_state.update({
            'name_ridepooling_system': name_ridepooling_system,
            'start_date': start_date,
            'end_date': end_date
        })
        # Das Startdatum muss vor dem Enddatum liegen
        if start_date > end_date:
            st.error("Das Startdatum muss vor dem Enddatum liegen.")
        # Weder Start-Datum noch End-Datum dürfen in der Zukunft liegen
        elif end_date > date.today():
            st.error("Das Enddatum darf nicht in der Zukunft liegen.")
        else:
            st.session_state.update({
                'name_ridepooling_system': name_ridepooling_system,
                'start_date': start_date,
                'end_date': end_date
            })
    


# Funktion zur Darstellung der Systemleistungs-Sektion
def show_system_performance():
    with st.expander("**2. Beförderungsleistung**"):
        st.info("**Hinweis:** Bitte geben Sie die Beförderungsleistung des Ridepooling-Systems an. Hierzu zählen die Anzahl der abgeschlossenen Buchungen und die Anzahl der transportierten Fahrgäste im Betrachtungszeitraum. Optional können Sie auch ein Ridepooling-System auswählen, um vorausgefüllte Daten zu erhalten.")
        
        # Daten für das Dropdown-Menü
        ridepooling_data = {
            "Eigene Angaben": {"Fahrten": 0, "Transportierte Fahrgäste": 0},
            "bussi": {"Fahrten": 8475, "Transportierte Fahrgäste": 13876, "vehicle_type": "LEVC TX (Volvo XC 90 Recharge T8 AWD)", "Benzinverbrauch (l/100km)": 1.2, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 20.5, "Kilometer leer": 50422.31, "Kilometer besetzt": 40063.44},
            "G-Mobil": {"Fahrten": 60043, "Transportierte Fahrgäste": 74561},
            "kommit-Shuttle": {"Fahrten": 21908, "Transportierte Fahrgäste": 26280},
            "LOOPmünster": {"Fahrten": 151415, "Transportierte Fahrgäste": 187309},
        }

        # Dropdown-Menü zum Auswählen des Ridepooling-Systems
        selected_system = st.selectbox('Wählen Sie ein Ridepooling-System (Optional):', list(ridepooling_data.keys()))

        # Eingabefelder mit vorausgefüllten Daten basierend auf der Auswahl
        abgeschlossene_buchungen = st.number_input("Abgeschlossene Buchungen im Betrachtungszeitraum:", value=ridepooling_data[selected_system]["Fahrten"], min_value=0)
        transportierte_fahrgaeste = st.number_input("Transportierte Fahrgäste im Betrachtungszeitraum:", value=ridepooling_data[selected_system]["Transportierte Fahrgäste"], min_value=0)

        # Speichern der globalen Variablen
        st.session_state.update({
            'abgeschlossene_buchungen': abgeschlossene_buchungen,
            'transportierte_fahrgaeste': transportierte_fahrgaeste
        })

# Funktion zur Darstellung der Fahrzeugflotten- und Fahrtleistungs-Sektion
def show_vehicle_fleet_performance():
    with st.expander("**3. Fahrzeugflotte & Fahrtleistung**"):
        # Vordefinierte Fahrzeugtypen und deren Verbrauchsdaten
        vehicle_types = {
            "LEVC TX (Volvo XC 90 Recharge T8 AWD)": {"Benzinverbrauch (l/100km)": 1.35, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 21.55, "Kilometer leer": 0, "Kilometer besetzt": 0},
            "Mercedes Vito lang 114 CDI": {"Benzinverbrauch (l/100km)": 0.0, "Dieselverbrauch (l/100km)": 8.4, "Stromverbrauch (kWh/100km)": 0.0, "Kilometer leer": 0, "Kilometer besetzt": 0},
            "Mercedes eVito Tourer PRO lang (90 kWh)": {"Benzinverbrauch (l/100km)": 0.0, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 29.8, "Kilometer leer": 0, "Kilometer besetzt": 0},
            "Mercedes EQV 300 extra lang": {"Benzinverbrauch (l/100km)": 0.0, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 30.2, "Kilometer leer": 0, "Kilometer besetzt": 0},
            "Nissan e NV 200": {"Benzinverbrauch (l/100km)": 0.0, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 20.6, "Kilometer leer": 0, "Kilometer besetzt": 0},
            "Anderer Fahrzeugtyp": {"Benzinverbrauch (l/100km)": 0.0, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 0.0, "Kilometer leer": 0, "Kilometer besetzt": 0}
        }

        # Initialisierung der Fahrzeugliste im Session State, falls noch nicht vorhanden
        if 'vehicle_list' not in st.session_state:
            st.session_state['vehicle_list'] = []

        # Fahrzeugdaten durch Nutzereingaben modifizieren
        with st.container():
            st.info("**Hinweis:** Bitte geben Sie an, welche Fahrzeugtypen in Ihrer Flotte vorhanden sind. Bitte geben Sie für jeden Fahrzeugtyp die gefahrenen Kilometerleistungen (leer, besetzt) flottenbezogen an. Bitte beziehen Sie sich auf den Betrachtungszeitraum. Die vorgegebenen Verbrauchsdaten beziehen sich auf die WLTP-Methode (Deutsche Automobil Treuhand GmbH, Leitfaden CO2 (2022)). Passen Sie ggf. Verbrauchsdaten an. Klicken Sie anschließend auf 'Daten übernehmen & berechnen'. Sie können andere Fahrzeugtypen abbilden, indem Sie ein 'andere Fahrzeugtypen' auswählen und die entsprechende Bezeichnung, sowie Kilometer- & Verbrauchsdaten eingeben.")

        with st.form("vehicle_form", clear_on_submit=True):
            new_vehicle_type = st.selectbox("Wählen Sie einen Fahrzeugtyp", list(vehicle_types.keys()))
            add_vehicle = st.form_submit_button("Fahrzeug hinzufügen")
        if add_vehicle:
            data = vehicle_types[new_vehicle_type].copy() if new_vehicle_type in vehicle_types else {"Benzinverbrauch (l/100km)": 0.0, "Dieselverbrauch (l/100km)": 0.0, "Stromverbrauch (kWh/100km)": 0.0, "Kilometer leer": 0, "Kilometer besetzt": 0}
            data['Fahrzeugtyp'] = new_vehicle_type  # Füge den Fahrzeugtyp hinzu
            vehicle_id = len(st.session_state['vehicle_list']) + 1
            st.session_state[f'vehicle_{vehicle_id}'] = data
            st.session_state['vehicle_list'].append(data)

        for i, vehicle in enumerate(st.session_state['vehicle_list'], start=1):
            cols = st.columns((3, 1, 1, 1, 1, 1))
            vehicle['Fahrzeugtyp'] = cols[0].text_input(f"Fahrzeugtyp {i}", vehicle['Fahrzeugtyp'])
            vehicle['Benzinverbrauch (l/100km)'] = cols[1].number_input(f"Benzin {i} (l/100km)", value=vehicle['Benzinverbrauch (l/100km)'], min_value=0.0, format='%f')
            vehicle['Dieselverbrauch (l/100km)'] = cols[2].number_input(f"Diesel {i} (l/100km)", value=vehicle['Dieselverbrauch (l/100km)'], min_value=0.0, format='%f')
            vehicle['Stromverbrauch (kWh/100km)'] = cols[3].number_input(f"Strom {i} (kWh/100km)", value=vehicle['Stromverbrauch (kWh/100km)'], min_value=0.0, format='%f')
            vehicle['Kilometer leer'] = cols[4].number_input(f"KM leer {i}", value=vehicle['Kilometer leer'], min_value=0, format='%d')
            vehicle['Kilometer besetzt'] = cols[5].number_input(f"KM besetzt {i}", value=vehicle['Kilometer besetzt'], min_value=0, format='%d')
            # Speichern der globalen Variablen
            st.session_state['Benzinverbrauch (l/100km)'] = vehicle['Benzinverbrauch (l/100km)'],
            st.session_state['Dieselverbrauch (l/100km)'] = vehicle['Dieselverbrauch (l/100km)'],
            st.session_state['Stromverbrauch (kWh/100km)'] = vehicle['Stromverbrauch (kWh/100km)']

        if st.button('Letztes Fahrzeug entfernen'):
            if st.session_state['vehicle_list']:
                removed_vehicle_id = len(st.session_state['vehicle_list'])
                st.session_state.pop(f'vehicle_{removed_vehicle_id}', None)  # Remove the global variable
                st.session_state['vehicle_list'].pop()

        # Berechne die Kilometer leer und besetzt für die gesamte Flotte
        fahrzeugkilometer_leer = sum(vehicle['Kilometer leer'] for vehicle in st.session_state['vehicle_list'])
        fahrzeugkilometer_besetzt = sum(vehicle['Kilometer besetzt'] for vehicle in st.session_state['vehicle_list'])

        if st.button('Daten übernehmen & berechnen'):
            try:
                abgeschlossene_buchungen = float(st.session_state['abgeschlossene_buchungen'])
                transportierte_fahrgaeste = float(st.session_state['transportierte_fahrgaeste'])
                fahrzeugkilometer_leer = float(fahrzeugkilometer_leer)
                fahrzeugkilometer_besetzt = float(fahrzeugkilometer_besetzt)
                fahrzeugkilometer_gesamt = round(fahrzeugkilometer_leer + fahrzeugkilometer_besetzt, 2)
                durchschnittliche_fahrtdistanz_mit_lk = round(fahrzeugkilometer_gesamt / abgeschlossene_buchungen, 2) if abgeschlossene_buchungen > 0 else 0
                durchschnittliche_fahrtdistanz_mit_bk = round(fahrzeugkilometer_besetzt / abgeschlossene_buchungen, 2) if abgeschlossene_buchungen > 0 else 0
                personenkilometer_gefahren = round((fahrzeugkilometer_besetzt / abgeschlossene_buchungen) * transportierte_fahrgaeste, 2) if abgeschlossene_buchungen > 0 else 0

                # Berechnungen der neuen Kennzahlen
                leerkilometeranteil = round((fahrzeugkilometer_leer / fahrzeugkilometer_gesamt) *100, 2) if fahrzeugkilometer_gesamt > 0 else 0
                buendelungsquote = round(personenkilometer_gefahren / fahrzeugkilometer_gesamt, 2) if fahrzeugkilometer_gesamt > 0 else 0
                besetzungsquote = round(personenkilometer_gefahren / fahrzeugkilometer_besetzt, 2) if fahrzeugkilometer_besetzt > 0 else 0

                # Speichern des Werts in den Sitzungszustand
                st.session_state.update({
                    'fahrzeugkilometer_leer': fahrzeugkilometer_leer,
                    'fahrzeugkilometer_besetzt': fahrzeugkilometer_besetzt,
                    'fahrzeugkilometer_gesamt': fahrzeugkilometer_gesamt,
                    'durchschnittliche_fahrtdistanz_mit_lk': durchschnittliche_fahrtdistanz_mit_lk,
                    'durchschnittliche_fahrtdistanz_mit_bk': durchschnittliche_fahrtdistanz_mit_bk,
                    'personenkilometer_gefahren': personenkilometer_gefahren,
                    'leerkilometeranteil': leerkilometeranteil,
                    'buendelungsquote': buendelungsquote,
                    'besetzungsquote': besetzungsquote,

                })

                benzinverbrauch_gesamt = sum(vehicle['Benzinverbrauch (l/100km)'] * ((vehicle['Kilometer besetzt'] + vehicle['Kilometer leer']) / 100) for vehicle in st.session_state['vehicle_list'])
                dieselverbrauch_gesamt = sum(vehicle['Dieselverbrauch (l/100km)'] * ((vehicle['Kilometer besetzt'] + vehicle['Kilometer leer']) / 100) for vehicle in st.session_state['vehicle_list'])
                stromverbrauch_gesamt = sum(vehicle['Stromverbrauch (kWh/100km)'] * ((vehicle['Kilometer besetzt'] + vehicle['Kilometer leer']) / 100) for vehicle in st.session_state['vehicle_list'])

                with st.container():
                    
                    st.write("**Fahrzeugleistung und -nutzung**")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Kilometer (leer):")
                    with col2:
                        st.write(f"{fahrzeugkilometer_leer} km")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Kilometer (besetzt):")
                    with col2:
                        st.write(f"{fahrzeugkilometer_besetzt} km")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Fahrzeugkilometer (gesamt):")
                    with col2:
                        st.write(f"{fahrzeugkilometer_gesamt} km")

                    st.write("**Durchschnittliche Fahrtdistanzen**")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Durchschnittliche Fahrtdistanz je Buchung (einschl. Leerkilometer):")
                    with col2:
                        st.write(f"{durchschnittliche_fahrtdistanz_mit_lk} km")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Durchschnittliche Fahrtdistanz je Buchung (mit Fahrgast):")
                    with col2:
                        st.write(f"{durchschnittliche_fahrtdistanz_mit_bk} km")

                    st.write("**Personenkilometer**")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Personenkilometer (gefahren):")
                    with col2:
                        st.write(f"{personenkilometer_gefahren} km")

                    st.write("**Leistungs-Kennzahlen**")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Leerkilometeranteil:")
                    with col2:
                        st.write(f"{leerkilometeranteil} %")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Bündelungsquote (nach § 50 Absatz 3 PBefG):")
                    with col2:
                        st.write(f"{buendelungsquote:.2f}")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Besetzungsquote (nach H Kripoo, 2021)")
                    with col2:
                        st.write(f"{besetzungsquote}")

                    st.write("**Verbrauchsdaten**")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Benzinverbrauch des Ridepooling-Systems:")
                    with col2:
                        st.write(f"{benzinverbrauch_gesamt:.2f} l")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Dieselverbrauch des Ridepooling-Systems:")
                    with col2:
                        st.write(f"{dieselverbrauch_gesamt:.2f} l")

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write("Stromverbrauch des Ridepooling-Systems:")
                    with col2:
                        st.write(f"{stromverbrauch_gesamt:.2f} kWh")

                # Save the total consumptions to the session state
                st.session_state.update({
                    'benzinverbrauch_gesamt': benzinverbrauch_gesamt,
                    'dieselverbrauch_gesamt': dieselverbrauch_gesamt,
                    'stromverbrauch_gesamt': stromverbrauch_gesamt
                })

                # Speichern der berechneten Werte im Sitzungszustand
                st.session_state.update({
                    'fahrzeugkilometer_leer': fahrzeugkilometer_leer,
                    'fahrzeugkilometer_besetzt': fahrzeugkilometer_besetzt,
                    'fahrzeugkilometer_gesamt': fahrzeugkilometer_gesamt,
                    'durchschnittliche_fahrtdistanz_mit_lk': durchschnittliche_fahrtdistanz_mit_lk,
                    'durchschnittliche_fahrtdistanz_mit_bk': durchschnittliche_fahrtdistanz_mit_bk,
                    'personenkilometer_gefahren': personenkilometer_gefahren,
                    'leerkilometeranteil': leerkilometeranteil,
                    'buendelungsquote': buendelungsquote,
                    'besetzungsquote': besetzungsquote
                })


                #Zeige den Sitzungszustand
                #st.write(st.session_state)

                st.info("""
                    **Hinweis:**
                    Die folgenden Formeln wurden zur Berechnung der Fahrzeugflotten- und Fahrtleistungsdaten verwendet:
                    - **Fahrzeugkilometer gesamt** = Kilometer leer + Kilometer besetzt
                    - **Durchschnittliche Fahrtdistanz je Buchung (einschl. Leerkilometer)** = Fahrzeugkilometer gesamt / Abgeschlossene Buchungen
                    - **Durchschnittliche Fahrtdistanz je Buchung (ohne Leerkilometer)** = Kilometer besetzt / Abgeschlossene Buchungen
                    - **Personenkilometer gefahren** = (Kilometer besetzt / Abgeschlossene Buchungen) * Transportierte Fahrgäste      
                    - **Leerkilometeranteil** = Kilometer leer / Fahrzeugkilometer gesamt
                    - **Bündelungsquote (nach § 50 Absatz 3 PBefG)** = Personenkilometer gefahren / Fahrzeugkilometer gesamt
                    - **Besetzungsquote (nach H Kripoo, 2021)** = Personenkilometer / Kilometer besetzt
                    - **Benzinverbrauch des Ridepooling-Systems** = Σ (Benzinverbrauch * (Kilometer besetzt + Kilometer leer) / 100)
                    - **Dieselverbrauch des Ridepooling-Systems** = Σ (Dieselverbrauch * (Kilometer besetzt + Kilometer leer) / 100)
                    - **Stromverbrauch des Ridepooling-Systems** = Σ (Stromverbrauch * (Kilometer besetzt + Kilometer leer) / 100)
                   
                """)

            except ValueError:
                st.error("Bitte geben Sie gültige Zahlenwerte ein.")
            

def show_emissions_data():
    with st.expander("**4. Emissionsdaten**"):
        st.info("**Hinweis:** Bitte geben Sie die CO2-Emissionsdaten für Benzin, Diesel und Strom an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen. Optional können Sie auch den Anteil an selbst erzeugtem Strom aus Photovoltaikanlagen angeben, um den adjustierten CO2eq-Emissionsfaktor für Strom zu berechnen. Bitte berücksichtigen Sie die Betrachtungsweise/Analyseprinzip. Dieses Programm nutzt die Well-to-Wheel-Betrachtung (WTW).")

        # CO2-Emissionsdaten (Benzin)
        benzin_emissionsdaten_auswahl = st.selectbox("CO2eq-Emissionsdaten (Benzin):", 
                                                      ["DIN EN 16258:2013, Tabelle A.2 [CO2eq]", "Helmholtz-Gemeinschaft Deutscher Forschungszentren [CO2eq]", "Eigene Angaben"])
        if benzin_emissionsdaten_auswahl == "DIN EN 16258:2013, Tabelle A.2 [CO2eq]":
            benzin_emissionsdaten = 2880  # g/l
        elif benzin_emissionsdaten_auswahl == "Helmholtz-Gemeinschaft Deutscher Forschungszentren [CO2eq]":
            benzin_emissionsdaten = 3030  # g/l
        else:  # Eigene Angaben
            benzin_emissionsdaten = st.number_input("Geben Sie die CO2-Emissionsdaten (Benzin) [g/l] ein:", min_value=0, format='%d', step=1)

        # CO2-Emissionsdaten (Diesel)
        diesel_emissionsdaten_auswahl = st.selectbox("CO2eq-Emissionsdaten (Diesel):", 
                                                      ["DIN EN 16258:2013, Tabelle A.4 [CO2eq]","Helmholtz-Gemeinschaft Deutscher Forschungszentren [CO2eq]", "Eigene Angaben"])
        if diesel_emissionsdaten_auswahl == "DIN EN 16258:2013, Tabelle A.4 [CO2eq]":
            diesel_emissionsdaten = 3170  # g/l
        elif diesel_emissionsdaten_auswahl == "Helmholtz-Gemeinschaft Deutscher Forschungszentren [CO2eq]":
            diesel_emissionsdaten = 3410  # g/l
        else:  # Eigene Angaben
            diesel_emissionsdaten = st.number_input("Geben Sie die CO2-Emissionsdaten (Diesel) [g/l] ein:", min_value=0, format='%d', step=1)

        # CO2-Emissionsdaten (Strom)
        strom_emissionsdaten_auswahl = st.selectbox("CO2eq-Emissionsdaten (Strom):", 
                                                     ["LANUK Emissionsfaktoren der Klimaneutralen Landesverwaltung: Strommix DE, 2022 [CO2eq]",
                                                      "LANUK Emissionsfaktoren der Klimaneutralen Landesverwaltung: Ökostrom DE, 2022 [CO2eq]", 
                                                      "Umweltbundesamt: CO2-Emissionsfaktor Strommix (2024) [CO2eq]", 
                                                      "Eigene Angaben"])
        if strom_emissionsdaten_auswahl == "LANUK Emissionsfaktoren der Klimaneutralen Landesverwaltung: Strommix DE, 2022 [CO2eq]":
            strom_emissionsdaten = 498  # g/kWh
        elif strom_emissionsdaten_auswahl == "LANUK Emissionsfaktoren der Klimaneutralen Landesverwaltung: Ökostrom DE, 2022 [CO2eq]":
            strom_emissionsdaten = 56  # g/kWh
        elif strom_emissionsdaten_auswahl == "Umweltbundesamt: CO2-Emissionsfaktor Strommix (2024) [CO2eq]":
            strom_emissionsdaten = 363  # g/kWh
        else:  # Eigene Angaben
            strom_emissionsdaten = st.number_input("Geben Sie die CO2-Emissionsdaten (Strom) [g CO2eq/kWh] ein:", min_value=0, format='%d', step=1)

        # Anteil an selbst erzeugtem Strom aus Photovoltaikanlagen
        
        st.info( "Optional: Ein Teil des Strombezugs kann aus einer sekundären Quelle (z. B. PV-Eigenerzeugung, zertifizierter Ökostrom, PPA) stammen. Der gewichtete Emissionsfaktor wird entsprechend berechnet.")
        oekostrom_anteil = st.slider("Optional: Geben Sie den Anteil einer **sekundären Stromquelle** am Stromverbrauch an [%]:", 0, 100, 0)
        pv_emissionsdaten = st.number_input("Geben Sie den Emissionsfaktor der **sekundären Stromquelle** an [g CO2e/kWh]:", value=50.0, min_value=0.0, format='%f', step=1.0)
        strom_emissionsdaten = round(strom_emissionsdaten * (1 - oekostrom_anteil / 100.0) + pv_emissionsdaten * (oekostrom_anteil / 100.0), 2)

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**CO2-Emissionsdaten (Benzin) ausgewählt:**")
        with col2:
            st.write(f"**{benzin_emissionsdaten} g CO2eq/l**")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**CO2-Emissionsdaten (Diesel) ausgewählt:**")
        with col2:
            st.write(f"**{diesel_emissionsdaten} g CO2eq/l**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Adjustierter CO2-Emissionsdaten (Strom) basierend auf {oekostrom_anteil}% der sekundären Stromquelle:**")
        with col2:
            st.write(f"**{strom_emissionsdaten} g CO2eq/kWh**")


        # Speichern der globalen Variablen
        st.session_state.update({
            'benzin_emissionsdaten': benzin_emissionsdaten,
            'diesel_emissionsdaten': diesel_emissionsdaten,
            'strom_emissionsdaten': strom_emissionsdaten,
            'oekostrom_anteil': oekostrom_anteil,
            'pv_emissionsdaten': pv_emissionsdaten
        })

# Funktion zur Darstellung der Berechnung der Umweltwirkung des Ridepooling-Systems
def show_environmental_impact_calculation():

    with st.expander("**5. Berechnung Umweltwirkung Ridepooling-System**"):
        st.info("**Hinweis:** Im Folgenden ist die Umweltwirkung des Ridepooling-Systems dargestellt. In der Abbildung wird der spezifische CO2-Ausstoß des Ridepooling-Systems denen anderer Verkehrsmittel gegenübergestellt. Die Daten der anderen Verkehrsmittel stammen vom Umweltbundesamt, Umweltfreundlich mobil! (2022).")

        # Stellen Sie sicher, dass alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['fahrzeugkilometer_gesamt', 'personenkilometer_gefahren', 'benzin_emissionsdaten', 'diesel_emissionsdaten', 'strom_emissionsdaten', 'oekostrom_anteil']
        missing_keys = [key for key in required_keys if key not in st.session_state]
        
        if missing_keys:
            st.error(f"Die folgenden Schlüssel fehlen: {', '.join(missing_keys)}")
        else:
            # Abrufen der Werte aus dem Sitzungszustand
            fahrzeugkilometer_gesamt = st.session_state['fahrzeugkilometer_gesamt']
            personenkilometer_gefahren = st.session_state['personenkilometer_gefahren']
            benzinverbrauch_gesamt = float(st.session_state['benzinverbrauch_gesamt'])
            dieselverbrauch_gesamt = float(st.session_state['dieselverbrauch_gesamt'])
            stromverbrauch_gesamt = float(st.session_state['stromverbrauch_gesamt'])
            benzin_emissionsdaten = st.session_state['benzin_emissionsdaten']
            diesel_emissionsdaten = st.session_state['diesel_emissionsdaten']
            strom_emissionsdaten = st.session_state['strom_emissionsdaten']
            oekostrom_anteil = st.session_state['oekostrom_anteil']

            benzin_emissionen = (benzinverbrauch_gesamt * benzin_emissionsdaten) / 1000  # kg CO2
            diesel_emissionen = (dieselverbrauch_gesamt * diesel_emissionsdaten) / 1000  # kg CO2
            strom_emissionen = (stromverbrauch_gesamt * strom_emissionsdaten) / 1000  # kg CO2
            strom_emissionen *= (1 - oekostrom_anteil / 100)  # Anpassung für Ökostrom

            # Speichern als globale Variablen
            st.session_state.update({
                'benzin_emissionen': benzin_emissionen,
                'diesel_emissionen': diesel_emissionen,
                'strom_emissionen': strom_emissionen
            })

            co2_emissionen_gesamt_rps = round(benzin_emissionen + diesel_emissionen + strom_emissionen, 4)
            co2_emissionen_pro_personenkilometer_rps = round(co2_emissionen_gesamt_rps / personenkilometer_gefahren, 4) if personenkilometer_gefahren else 0

            # Speichern der berechneten Werte im Sitzungszustand
            st.session_state.update({
                'co2_emissionen_gesamt_rps': co2_emissionen_gesamt_rps,
                'co2_emissionen_pro_personenkilometer_rps': co2_emissionen_pro_personenkilometer_rps
            })

            # Emissionen pro pkm für verschiedene Verkehrsträger
            emissionen_data = {
                st.session_state['name_ridepooling_system']: co2_emissionen_pro_personenkilometer_rps * 1000,
                'Pkw - MIV (Fahrer) & MIV (Mitfahrer)': 152.86,
                '(Nahlinien-)Bus': 80.54,
                'Straßen-/Stadt-/U-Bahn': 59.30,
                'Schienen(nah)verkehr/Bahn/Zug': 58.79,
                'Motorrad': 173.3,
                'E-Bike/Pedelec/E-Lastenrad': 3.9,
                'Fahrrad/Lastenrad': 0.0,
                'Zu Fuß': 0.0
            }

            # Erstellung des ersten Diagramms
            fig1 = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig1.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig1.update_layout(
                barmode='group',
                title='Gegenüberstellung der Emissionen pro Personenkilometer nach Verkehrsmittel - Well-to-Wheel (WTW)*',
                legend=dict(
                orientation="v",  # vertikale Anordnung
                y=0.6,  # Positionierung der Legende
                x=1.02,  # Legende rechts vom Diagramm
                xanchor='left',
                yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2eq/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig1)

            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Gesamte CO2-Emissionen des Ridepooling-Systems:**")
            with col2:
                st.write(f"**{co2_emissionen_gesamt_rps:.2f} kg CO2eq**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**CO2-Emissionen pro Personenkilometer:**")
            with col2:
                st.write(f"**{co2_emissionen_pro_personenkilometer_rps:.3f} kg CO2eq/pkm**")
                



# Initialisiere Session State Variablen
initialize_session_state()

# Zeige Sidebar an
show_sidebar()

# Grundlegende Konfiguration
st.title("ÖkoRPS - Ökologische Bewertung von Ridepooling-Systemen")

# Zeige Methodik-Sektion an
show_methodik_section()

st.subheader("Berechnung der Umweltwirkung des Ridepooling-Systems")
# Zeige Allgemeine Informationen an
show_general_info()

# Zeige Systemleistungs-Sektion an
show_system_performance()

# Zeige Fahrzeugflotten- und Fahrtleistungs-Sektion an
show_vehicle_fleet_performance()

# Zeige Emissionsdaten-Sektion an
show_emissions_data()

# Zeige Berechnung Umweltwirkung Ridepooling-System an
show_environmental_impact_calculation()

st.subheader("THG-Bilanzierung der Referenzmobilität im Bediengebiet (alternativ genutzter Verkehrsmittel ohne Ridepooling-Verkehr)")
st.info("""**Hinweis:**  
Die Berechnung der Verkehrsleistung der Referenzmobilität im Bediengebiet kann auf unterschiedlichen methodischen Ansätzen basieren.  
Abhängig von der Datenverfügbarkeit ist eine geeignete Methodik auszuwählen und durch Annahmen zu ergänzen.""")



####################################################################################################
# Erstelle 4 Buttons für die Auswahl der Methodik zur Berechnung der Umweltwirkung der alternativen Verkehrsmittel

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Modal Split (Wege)"):
        st.session_state['methodik'] = "Modal Split (Wege)"
        st.session_state['methodik_selected'] = True
        st.session_state['methodik_selected_pkm'] = False

with col2:
    if st.button("Modal Split (Pkm)"):
        st.session_state['methodik'] = "Modal Split (Pkm)"
        st.session_state['methodik_selected'] = True
        st.session_state['methodik_selected_pkm'] = True

with col3:
    if st.button("Umfrage (Wege)"):
        st.session_state['methodik'] = "Umfrage (Wege)"
        st.session_state['methodik_selected'] = True
        st.session_state['methodik_selected_pkm'] = False

with col4:
    if st.button("Umfrage (Pkm)"):
        st.session_state['methodik'] = "Umfrage (Pkm)"
        st.session_state['methodik_selected'] = True
        st.session_state['methodik_selected_pkm'] = True


# Überprüfe, ob eine Methode ausgewählt wurde
if 'methodik_selected' in st.session_state and st.session_state['methodik_selected']:
    st.success(f"Die Methode **'{st.session_state['methodik']}'** wurde ausgewählt. Bitte fahren Sie mit der Eingabe der Daten fort.")
else:
    st.warning("Zur Berechnung der THG-Bilanz der Referenzmobilität im Bediengebiet ist ein geeigneter methodischer Ansatz auszuwählen.")

####################################################################################################
# Modal Split (Wege)
# Sollte Button "Modal Split (Wege)" ausgewählt sein, dann zeige folgende Expander an
if 'methodik' in st.session_state and st.session_state['methodik'] == "Modal Split (Wege)":
    with st.expander("**6. Verkehrsmittelverteilung alternativ genutzer Verkehrsmittel (ohne Ridepooling-Verkehr)**"):
        st.info("""**Hinweis:** Bitte geben Sie die Annahmen für die Modal-Split-Verteilung (Wege) der Fahrgäste an.                     
                    **Vorauswahl des Modal Split (Wege):**
    Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Modal-Split-Verteilung automatisch auszufüllen. Diese Werte sind anpassbar.
        """)
        # Dropdown-Menü für Modal-Split-Optionen
        modal_split_options = {
            "Eigene Angaben (Wege)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Modal Split (Wege) MiD 2017": [42, 16, 3, 3, 2, 1, 1, 10, 22, 0],
            "Modal Split (Wege) Essen (2019)": [46, 8, 6, 8, 5, 1, 1, 6, 19, 0],
            "Modal Split (Wege) Senden (2000)": [48, 10, 4.5, 0, 1.5, 0, 0, 21, 14, 1],
            "Modal Split (Wege) Gronau (2020)": [47, 8, 1, 0, 1, 0, 0, 30, 13, 0],
            "Modal Split (Wege) Münster, Hiltrup (2022)": [31, 9, 7, 0, 2, 0, 10, 24, 17, 0]
        }
        selected_modal_split = st.selectbox("Vorauswahl Modal Split (Optional):", list(modal_split_options.keys()))

        # Speichern der globalen Variablen
        st.session_state['selected_modal_split'] = selected_modal_split

        # Anzeigen der Anteile basierend auf der ausgewählten Vorauswahl
        default_values = modal_split_options[selected_modal_split]

        # Eingabefelder für die Anteile
        transport_modes = ["MIV (Fahrer)", "MIV (Mitfahrer)", "(Nahlinien-)Bus", "Straßen-/Stadt-/U-Bahn", "Schienen(nah)verkehr/Bahn/Zug", "Motorrad", "E-Bike/Pedelec/E-Lastenrad", "Fahrrad/Lastenrad", "zu Fuß", "Sonstiges"]
        entries_modal_split = {}
        for i, mode in enumerate(transport_modes):
            entries_modal_split[mode] = st.number_input(
                f"Anteil der Fahrgäste, die {mode} genutzt hätten (%):", 
                min_value=0.0, 
                max_value=100.0, 
                value=round(float(default_values[i]), 1),  # Round the default value to 1 decimal place
                step=0.1, 
                format="%.1f"  # Display with 1 decimal place
            )

        # Überprüfung der Gesamtsumme der eingegebenen Werte
        total_percentage = sum(entries_modal_split.values())
        if total_percentage > 100:
            st.error("Die Summe der Modal-Split-Anteile überschreitet 100%.")
        elif total_percentage < 100:
            st.warning("Die Summe der Modal-Split-Anteile liegt unter 100%.")

        # Außerhalb des Expanders
        st.write("**Berechnung der Wegehäufigkeit der alternativen Verkehrsmittel:**")
        st.info("**Hinweis:** Um die Wegehäufigkeit der alternativen Verkehrsmittel zu berechnen, wird die Anzahl der Fahrgäste mit dem ensprechenden Modal-Split-Anteil (Wege) multipliziert.")
        #Speichern der globalen Variablen
        st.session_state['entries_modal_split'] = entries_modal_split

        if 'transportierte_fahrgaeste' in st.session_state and 'entries_modal_split' in st.session_state:
            transportierte_fahrgaeste = int(st.session_state['transportierte_fahrgaeste'])
            st.write(f"Von den **{int(st.session_state['transportierte_fahrgaeste'])}** transportierten Fahrgästen hätten entsprechend viele Personen folgende alternative Verkehrsmittel genutzt:")
            entries_modal_split = st.session_state['entries_modal_split']
            
            for verkehrsmittel, anteil in entries_modal_split.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{verkehrsmittel}:**")
                with col2:
                    berechneter_wert = transportierte_fahrgaeste * anteil / 100
                    st.write(f"**{berechneter_wert:.0f} Personen**")
                    
        else:
            st.warning("Bitte stellen Sie sicher, dass die Gesamtzahl der transportierten Fahrgäste und die Modal-Split-Annahmen festgelegt wurden.")

    ####################################################################################################
    with st.expander("**7. Wegeentfernung alternativer Verkehrsmittel**"):
        # Initializations
        if 'durchschnittliche_fahrtdistanz_mit_bk' not in st.session_state:
            st.session_state['durchschnittliche_fahrtdistanz_mit_bk'] = 0
        if 'durchschnittliche_fahrtdistanz_mit_lk' not in st.session_state:
            st.session_state['durchschnittliche_fahrtdistanz_mit_lk'] = 0
        if 'transportierte_fahrgaeste' not in st.session_state:
            st.session_state['transportierte_fahrgaeste'] = 0
        if 'entries_modal_split' not in st.session_state:
            st.session_state['entries_modal_split'] = {}
        st.info("""**Hinweis:** Bitte geben Sie die Annahmen zur Wegeentfernung der alternativ genutzten Verkehrsmittel an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen. Die durschnittliche Fahrtdistanz je Buchung (einschließlich Leerkilometern) und die durschnittliche Fahrtdistanz je Buchung (mit Fahrgast) sind Angaben, die sich auf das Ridepooling-System beziehen. Wahlweise können auch Daten der durchschnittlichen Reiseweiten nach MiD 2017 verwendet werden.""")
        
        vorauswahl_optionen = {
            "Durchschnittliche Fahrtdistanz je Buchung (mit Fahrgast)": st.session_state['durchschnittliche_fahrtdistanz_mit_bk'],
            "Durchschnittliche Fahrtdistanz je Buchung (einschließlich Leerkilometern)": st.session_state['durchschnittliche_fahrtdistanz_mit_lk'],
            "Durchschnittliche Reiseweiten nach MID 2017": {
                "MIV (Fahrer)": 16.0,
                "MIV (Mitfahrer)": 18.0,
                "(Nahlinien-)Bus": 23.0,
                "Straßen-/Stadt-/U-Bahn": 23.0,
                "Schienen(nah)verkehr/Bahn/Zug": 23.0,
                "Motorrad": 16.0,
                "E-Bike/Pedelec/E-Lastenrad": 4.0,
                "Fahrrad/Lastenrad": 4.0,
                "Zu Fuss": 2.0,
                "Sonstiges": 0.0
            }
        }

        selected_vorauswahl = st.selectbox("Vorauswahl der Wegeentfernung:", list(vorauswahl_optionen.keys()))

        if selected_vorauswahl == "Durchschnittliche Fahrtdistanz je Buchung (mit Fahrgast)":
            default_distances = {mode: st.session_state['durchschnittliche_fahrtdistanz_mit_bk'] for mode in transport_modes}
        elif selected_vorauswahl == "Durchschnittliche Fahrtdistanz je Buchung (einschließlich Leerkilometern)":
            default_distances = {mode: st.session_state['durchschnittliche_fahrtdistanz_mit_lk'] for mode in transport_modes}
        else:
            default_distances = vorauswahl_optionen[selected_vorauswahl]

        mode_to_key = {
            "MIV (Fahrer)": "miv_fahrer",
            "MIV (Mitfahrer)": "miv_mitfahrer",
            "(Nahlinien-)Bus": "nahlinien_bus",
            "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
            "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
            "Motorrad": "motorrad",
            "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
            "Fahrrad/Lastenrad": "fahrrad_lastenrad",
            "zu Fuß": "zu_fuss",  # Corrected key to match 'zu Fuß'
            "Sonstiges": "sonstiges"
        }

        for mode in transport_modes:
            key = mode_to_key[mode]
            distance = st.number_input(
                f"Wegeentfernung {mode} [km]:", 
                min_value=0.0, 
                value=round(float(default_distances.get(mode, 0)), 2),  # Round the default value to 2 decimal places
                format="%.2f",  # Display with 2 decimal places
                step=0.01
            )
            st.session_state[f'entfernung_{key}'] = round(distance, 2)  # Round the input value to 2 decimal places

        st.write("**Berechnung der Personenkilometer für Referenzmobiliität im Bediengebiet (alternativ genutzte Verkehrsmittel):**")
        st.info("**Hinweis:** Die Berechnung der Personenkilometer basiert auf der Anzahl der transportierten Fahrgäste und der jeweiligen durchschnittlichen Fahrtdistanz. Die Formel zur Berechnung der Personenkilometer (PKM) lautet: PKM = Anzahl der transportierten Fahrgäste * Durchschnittliche Fahrtdistanz.")

        # Berechnung und Anzeige der Personenkilometer für jedes Verkehrsmittel
        st.write("Die Berechnung der Personenkilometer für die verschiedenen alternativ genutzten Verkehrsmittel ergibt folgende Werte:")
        for mode in transport_modes:
            key = mode_to_key[mode]
            transportierte_fahrgaeste = st.session_state['transportierte_fahrgaeste']
            personen = int(transportierte_fahrgaeste) * float(st.session_state['entries_modal_split'].get(mode, 0)) / 100
            entfernung = st.session_state.get(f'entfernung_{key}', 0)
            personenkilometer = round(personen * entfernung, 2)
            st.session_state[f'personenkilometer_{key}'] = personenkilometer
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{mode}**:")
            with col2:
                st.write(f"**{personenkilometer} Pkm**")

        # Berechnung der Gesamt-Personenkilometer für alternative Verkehrsmittel
        personenkilometer_gesamt_av = round(sum(
            st.session_state.get(f'personenkilometer_{mode_to_key[mode]}', 0)
            for mode in transport_modes), 2)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Gesamte Personenkilometer für alternativ genutzte Verkehrsmittel:**")
        with col2:
            st.write(f"**{personenkilometer_gesamt_av} Pkm**")



    with st.expander("**8. Emissionsdaten alternativ genutzter Verkehrsmittel (Nutzung [TTW] und Energie [WTT])**"):
        st.info("""**Hinweis:** Bitte geben Sie die CO2-Emissionsdaten für die alternativ genutzten Verkehrsmittel an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen.
                    **Vorauswahl der Emissionsdaten:**
                    Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Emissionsdaten automatisch auszufüllen. Diese Werte sind anpassbar.""")


        transport_modes = ["MIV (Fahrer)", "MIV (Mitfahrer)", "(Nahlinien-)Bus", "Straßen-/Stadt-/U-Bahn", "Schienen(nah)verkehr/Bahn/Zug", "Motorrad", "E-Bike/Pedelec/E-Lastenrad", "Fahrrad/Lastenrad", "zu Fuß", "Sonstiges"]

        mode_to_key = {
            "MIV (Fahrer)": "miv_fahrer",
            "MIV (Mitfahrer)": "miv_mitfahrer",
            "(Nahlinien-)Bus": "nahlinien_bus",
            "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
            "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
            "Motorrad": "motorrad",
            "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
            "Fahrrad/Lastenrad": "fahrrad_lastenrad",
            "zu Fuß": "zu_fuss",
            "Sonstiges": "sonstiges"
        }

        # Vorauswahl der Emissionsdaten
        vorauswahl_emissionsdaten_optionen = ["Umweltbundesamt, Umweltfreundlich mobil! (2022)", "Eigene Angaben"]
        selected_vorauswahl_emissionsdaten = st.selectbox("Vorauswahl der Emissionsdaten:", vorauswahl_emissionsdaten_optionen)

        # Definieren der Standardemissionswerte basierend auf der Vorauswahl
        if selected_vorauswahl_emissionsdaten == "Umweltbundesamt, Umweltfreundlich mobil! (2022)":
            emissionsdaten_defaults = {
                "miv_fahrer": 152.86,
                "miv_mitfahrer": 152.86,
                "nahlinien_bus": 80.54,
                "strassen_stadt_u_bahn": 58.79,
                "schienen_nah_verkehr_bahn_zug": 58.79,
                "motorrad": 90.0,
                "e_bike_pedelec_e_lastenrad": 3.9,
                "fahrrad_lastenrad": 0.0,
                "zu_fuss": 0.0,
                "sonstiges": 0.0
            }
        else:
            emissionsdaten_defaults = {key: 0 for key in mode_to_key.values()}

        for mode in transport_modes:
            key = mode_to_key[mode]
            emission = st.number_input(
                f"Annahmen Emissionsdaten {mode} [gCO2eq/pkm]:", 
                min_value=0.0, 
                value=round(float(emissionsdaten_defaults.get(key, 0)), 2),  # Round the default value
                format="%.2f",  # Limit the display to 2 decimal places
                step=0.01
            )
            st.session_state[f'emission_{key}'] = round(emission, 2)  # Round the input value to 2 decimal places

        # Direkte Berechnung und Anzeige der Emissionen pro Verkehrsmittel
        
        for mode in transport_modes:
            key = mode_to_key[mode]
            personenkilometer = st.session_state.get(f'personenkilometer_{key}', 0)
            emission = st.session_state.get(f'emission_{key}', 0)
            emissionen_av = round(personenkilometer * emission / 1000, 2)  # Umrechnung von gCO2eq in kg CO2eq
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Emissionen für {mode}:**")
            with col2:
                st.write(f"**{emissionen_av} kg CO2eq**")

        # Berechnung und Speicherung der Gesamtemissionen für alternative Verkehrsmittel
        gesamtemissionen_av = round(sum(
            st.session_state.get(f'personenkilometer_{mode_to_key[mode]}', 0) *
            st.session_state.get(f'emission_{mode_to_key[mode]}', 0) / 1000
            for mode in transport_modes
        ), 2)
        st.session_state['gesamtemissionen_av'] = gesamtemissionen_av
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Gesamtemissionen für Referenzmobilität im Bediengebiet (alternativ genutzte Verkehrsmittel):**")
        with col2:
            st.write(f"**{gesamtemissionen_av} kg CO2eq**")

        #Berechnen der Personenkilometer für alternative Verkehrsmittel
        personenkilometer_gesamt_av = round(sum(
            st.session_state.get(f'personenkilometer_{mode_to_key[mode]}', 0)
            for mode in transport_modes
        ), 2)
        st.session_state['personenkilometer_gesamt_av'] = personenkilometer_gesamt_av


    # 8. Registerkarte: Berechnung der Umweltwirkung alternativer Verkehrsmittel
    with st.expander("**9. Berechnung der Umweltwirkung der Referenzmobilität im Bedienegbet**"):
        st.info("""**Hinweis:** Im Folgenden wird die Umweltwirkung der Referenzmobiltät im Raum anhand des Modal Split (Wege) dargestellt. In der Abbildung wird der spezifische CO2-Ausstoß pro Pkm der zunächst alternativ genutzten Verkehrsmittel gegenübergestellt.""")
        
        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['gesamtemissionen_av', 'personenkilometer_gesamt_av']
        if all(key in st.session_state for key in required_keys):
            gesamtemissionen_av = st.session_state['gesamtemissionen_av']
            personenkilometer_gesamt_av = st.session_state['personenkilometer_gesamt_av']

            # Berechnung der Emissionen pro Personenkilometer
            emissionen_pro_personenkilometer_av = gesamtemissionen_av / personenkilometer_gesamt_av if personenkilometer_gesamt_av > 0 else 0

            # Speichere die berechneten Werte im Sitzungszustand
            st.session_state['emissionen_pro_personenkilometer_av'] = emissionen_pro_personenkilometer_av

            emissionen_data = {
                'THG-Bilanz Referenzmobilität im Bediengebiet': emissionen_pro_personenkilometer_av * 1000,
                'Pkw - MIV (Fahrer) & MIV (Mitfahrer)': 152.86,
                '(Nahlinien-)Bus': 80.54,
                'Straßen-/Stadt-/U-Bahn': 59.30,
                'Schienen(nah)verkehr/Bahn/Zug': 58.79,
                'Motorrad': 173.3,
                'E-Bike/Pedelec/E-Lastenrad': 3.9,
                'Fahrrad/Lastenrad': 0.0,
                'Zu Fuß': 0.0
            }

            # Diagramm erstellen
            fig = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig.update_layout(
                barmode='group',
                title='Gegenüberstellung der Emissionen pro Personenkilometer nach Verkehrsmittel - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [kg CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte Well-to-Wheel CO2e-Emissionen der Referenzmobilität im Bedieengebiet:**")
            with col2:
                st.write(f"**{gesamtemissionen_av} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2e-Emissionen der Referenzmobilität im Bediengebiet (alternativ genutzter Verkehrsmittel) pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av:.3f} kg CO2/pkm**")

        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um die THG-Bilanz der Referenzmobilität im Bediengebiet zu berechnen.")

    
    st.subheader("Vergleich der spezifischen CO2-Emissionen pro Personenkilometer für das Ridepooling-System und Referenzmobilität im Bediengebiet")
    with st.expander("**10. Vergleich**"):
        st.info("""**Hinweis:** Im Folgenden wird der spezifische CO2-Ausstoß pro Personenkilometer des Ridepooling-Systems mit dem der Referenzmobilität im Bediengebiet.""")

        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['co2_emissionen_pro_personenkilometer_rps', 'emissionen_pro_personenkilometer_av', 'gesamtemissionen_av', 'co2_emissionen_gesamt_rps']

        if all(key in st.session_state for key in required_keys):
            co2_emissionen_pro_personenkilometer_rps = st.session_state['co2_emissionen_pro_personenkilometer_rps']
            emissionen_pro_personenkilometer_av = st.session_state['emissionen_pro_personenkilometer_av']

            # Erstellung des Diagramms
            emissionen_data = {
                st.session_state['name_ridepooling_system']: co2_emissionen_pro_personenkilometer_rps * 1000,
                'Referenzmobilität im Bediengebiet': emissionen_pro_personenkilometer_av * 1000
            }

            fig2 = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig2.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig2.update_layout(
                barmode='group',
                title='Gegenüberstellung der spezifischen CO2-Emissionen pro Personenkilometer - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig2)

            #Get co2_emissionen_gesamt_rps, start_date, end_date, gesamtemissionen_av, und runde auf 2 Dezimalstellen
            co2_emissionen_gesamt_rps = round(st.session_state['co2_emissionen_gesamt_rps'], 2)
            gesamtemissionen_av = st.session_state['gesamtemissionen_av']
            start_date = st.session_state['start_date']
            end_date = st.session_state['end_date']

            # Erstellung eines Textfeldes, in welchem die spezifischen CO2-Emissionen pro Personenkilometer des Ridepooling-Systems und der alternativ genutzten Verkehrsmittel verglichen werden
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen des Ridepooling-Systems:**")
            with col2:
                st.write(f"**{co2_emissionen_gesamt_rps:.2f} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen des Ridepooling-Systems pro Personenkilometer:**")
            with col2:
                st.write(f"**{co2_emissionen_pro_personenkilometer_rps:.3f} kg CO2/pkm**")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
            with col2:
                st.write(f"**{gesamtemissionen_av} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av:.3f} kg CO2/pkm**")
                         
            # Erstelle ein Textfeld, in welchem je nach Ausgang des Vergleichs eine entsprechende Meldung ausgegeben wird
            if emissionen_pro_personenkilometer_av != 0:
                if co2_emissionen_pro_personenkilometer_rps < emissionen_pro_personenkilometer_av:
                    percentage_difference = round((emissionen_pro_personenkilometer_av - co2_emissionen_pro_personenkilometer_rps) / emissionen_pro_personenkilometer_av * 100, 2)
                    total_difference = round((gesamtemissionen_av - co2_emissionen_gesamt_rps), 2)
                    st.success(f"Das Ridepooling-System weist im Vergleich zu den alternativ genutzten Verkehrsmitteln eine geringere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % niedriger als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Einsparung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                elif co2_emissionen_pro_personenkilometer_rps > emissionen_pro_personenkilometer_av:
                    percentage_difference = round((co2_emissionen_pro_personenkilometer_rps - emissionen_pro_personenkilometer_av) / emissionen_pro_personenkilometer_av * 100, 2)
                    total_difference = round((co2_emissionen_gesamt_rps - gesamtemissionen_av), 2)
                    st.error(f"Das Ridepooling-System weist im Vergleich zu den den alternativ genutzten Verkehrsmitteln eine höhere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % höher als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Erhöhung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                else:
                    st.warning("Das Ridepooling-System und die alternativen Verkehrsmittel weisen die gleiche spezifische CO2-Emission pro Personenkilometer auf.")
        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um den Vergleich der spezifischen CO2-Emissionen pro Personenkilometer durchzuführen.")

    # Erstelle ein Textfeld, in welchem je nach Ausgang des Vergleichs eine entsprechende Meldung ausgegeben wird

    with st.expander("**11. Export der Eingabedaten und Ergebnisse**"):
        # Stellen Sie sicher, dass alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = [
            'name_ridepooling_system', 'start_date', 'end_date', 'abgeschlossene_buchungen',
            'transportierte_fahrgaeste', 'vehicle_list', 'fahrzeugkilometer_leer', 'fahrzeugkilometer_besetzt',
            'fahrzeugkilometer_gesamt', 'durchschnittliche_fahrtdistanz_mit_lk', "durchschnittliche_fahrtdistanz_mit_bk",
            'personenkilometer_gefahren', 'benzinverbrauch_gesamt', 'dieselverbrauch_gesamt', 'stromverbrauch_gesamt',
            'oekostrom_anteil', 'benzin_emissionsdaten', 'diesel_emissionsdaten', 'strom_emissionsdaten',
            'co2_emissionen_gesamt_rps', 'co2_emissionen_pro_personenkilometer_rps', 'personenkilometer_gesamt_av',
            'gesamtemissionen_av', 'emissionen_pro_personenkilometer_av', 'entries_modal_split'
        ]
        missing_keys = [key for key in required_keys if key not in st.session_state]
        if missing_keys:
            st.error(f"Die folgenden Schlüssel fehlen: {', '.join(missing_keys)}")
        else:
            st.write("Die Eingabedaten und Ergebnisse können als CSV-Datei exportiert werden.")
            if st.button("Exportieren"):
                # Erstellen eines DataFrames mit den Eingabedaten und Ergebnissen des Ridepooling-Systems
                data_rps = {
                    "Merkmal": ["Wert"],
                    "Ridepooling-System": [st.session_state['name_ridepooling_system']],
                    "Betrachtungszeitraum (Start)": [f"{st.session_state['start_date']}"],
                    "Betrachtungszeitraum (Ende)": [f"{st.session_state['end_date']}"],
                    "Anzahl abgeschlossener Buchungen": [st.session_state['abgeschlossene_buchungen']],
                    "Transportierte Fahrgäste": [st.session_state['transportierte_fahrgaeste']],
                    "Flotte - Fahrzeugkilometer (leer)": [st.session_state['fahrzeugkilometer_leer']],
                    "Flotte - Fahrzeugkilometer (besetzt)": [st.session_state['fahrzeugkilometer_besetzt']],
                    "Flotte - Fahrzeugkilometer (gesamt)": [st.session_state['fahrzeugkilometer_gesamt']],
                    "Flotte - Personenkilometer (gefahren)": [st.session_state['personenkilometer_gefahren']],
                    "Durchschnittliche Fahrtdistanz (mit Fahrgast)": [st.session_state['durchschnittliche_fahrtdistanz_mit_bk']],
                    "Durchschnittliche Fahrtdistanz (ohne Fahrgast)": [st.session_state['durchschnittliche_fahrtdistanz_mit_lk']],
                    "Flotte - Benzinverbrauch (gesamt)": [st.session_state['benzinverbrauch_gesamt']],
                    "Flotte - Dieselverbrauch (gesamt)": [st.session_state['dieselverbrauch_gesamt']],
                    "Flotte - Stromverbrauch (gesamt)": [st.session_state['stromverbrauch_gesamt']],
                    "Ökostromanteil (%)": [st.session_state['oekostrom_anteil']],
                    "CO2-Emissionsdaten (Benzin)": [st.session_state['benzin_emissionsdaten']],
                    "CO2-Emissionsdaten (Diesel)": [st.session_state['diesel_emissionsdaten']],
                    "CO2-Emissionsdaten (Strom)": [st.session_state['strom_emissionsdaten']],
                    "CO2-Emissionen (gesamt)": [st.session_state['co2_emissionen_gesamt_rps']],
                    "CO2-Emissionen pro Personenkilometer": [st.session_state['co2_emissionen_pro_personenkilometer_rps']]
                }

                df_rps = pd.DataFrame(data_rps).transpose()
                df_rps.columns = df_rps.iloc[0]
                df_rps = df_rps[1:]

                # Erstellen eines DataFrames mit den Fahrzeugdaten
                if 'vehicle_list' in st.session_state and st.session_state['vehicle_list']:
                    vehicle_data = {
                        "Fahrzeugtyp": [],
                        "Benzinverbrauch (l/100km)": [],
                        "Dieselverbrauch (l/100km)": [],
                        "Stromverbrauch (kWh/100km)": [],
                        "Kilometer leer": [],
                        "Kilometer besetzt": []
                    }
                    for vehicle in st.session_state['vehicle_list']:
                        if isinstance(vehicle, dict) and all(key in vehicle for key in ['Fahrzeugtyp', 'Kilometer leer', 'Kilometer besetzt']):
                            vehicle_data["Fahrzeugtyp"].append(vehicle['Fahrzeugtyp'])
                            vehicle_data["Benzinverbrauch (l/100km)"].append(vehicle['Benzinverbrauch (l/100km)'])
                            vehicle_data["Dieselverbrauch (l/100km)"].append(vehicle['Dieselverbrauch (l/100km)'])
                            vehicle_data["Stromverbrauch (kWh/100km)"].append(vehicle['Stromverbrauch (kWh/100km)'])
                            vehicle_data["Kilometer leer"].append(vehicle['Kilometer leer'])
                            vehicle_data["Kilometer besetzt"].append(vehicle['Kilometer besetzt'])

                    df_vehicles = pd.DataFrame(vehicle_data)
                else:
                    st.error("No vehicles in the session state or 'vehicle_list' is not set.")
                    df_vehicles = pd.DataFrame()

                # Erstellen eines DataFrames mit den Emissionsdaten der alternativ genutzten Verkehrsmittel, Modal Split, Emissions
                mode_to_key = {
                    "MIV (Fahrer)": "miv_fahrer",
                    "MIV (Mitfahrer)": "miv_mitfahrer",
                    "(Nahlinien-)Bus": "nahlinien_bus",
                    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
                    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
                    "Motorrad": "motorrad",
                    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
                    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
                    "zu Fuß": "zu_fuss",
                    "Sonstiges": "sonstiges"
                }

                data_av = {
                    "Merkmal": ["Wert"],
                    "Gesamtemissionen alternative Verkehrsmittel (kg CO2eq)": [st.session_state['gesamtemissionen_av']],
                    "Personenkilometer alternative Verkehrsmittel (km)": [st.session_state['personenkilometer_gesamt_av']],
                    "CO2-Emissionen pro Personenkilometer alternative Verkehrsmittel (g CO2eq/pkm)": [st.session_state['emissionen_pro_personenkilometer_av']]
                }

                # Hinzufügen der Modal Split Daten
                for verkehrsmittel, anteil in st.session_state['entries_modal_split'].items():
                    key = mode_to_key.get(verkehrsmittel, verkehrsmittel)
                    data_av[f"Modal Split Anteil für {verkehrsmittel} (%)"] = [anteil]

                # Hinzufügen der Wegehäufigkeit, Durchschnittliche Fahrtdistanz, Personenkilometer und Emissionsdaten für alternative Verkehrsmittel
                for mode in st.session_state['entries_modal_split']:
                    key = mode_to_key.get(mode, mode)
                    personenkilometer = st.session_state.get(f'personenkilometer_{key}', 0)
                    durchschnittliche_fahrtdistanz = st.session_state.get(f'entfernung_{key}', 0)
                    emissionsdaten = st.session_state.get(f'emission_{key}', 0)
                    data_av[f"Wegehäufigkeit für {mode} (Personenkilometer)"] = [personenkilometer]
                    data_av[f"Durchschnittliche Fahrtdistanz für {mode} (km)"] = [durchschnittliche_fahrtdistanz]
                    data_av[f"Emissionsdaten für {mode} (g CO2eq/pkm)"] = [emissionsdaten]

                df_av = pd.DataFrame(data_av).transpose()
                df_av.columns = df_av.iloc[0]
                df_av = df_av[1:]

                # Zusammenführen der DataFrames
                df_combined = pd.concat([df_rps, df_vehicles, df_av], axis=0)
                df_combined = df_combined.replace('', np.nan)
                st.write(df_combined)

                # Export als CSV-Datei
                csv = df_combined.to_csv(index=True)
                st.download_button(label="CSV-Datei herunterladen", data=csv, file_name='eingabedaten_und_ergebnisse.csv', mime='text/csv')


#########################################################################################
# Modal Split (Pkm)


mode_to_key_pkm = {
    "MIV (Fahrer)": "miv_fahrer",
    "MIV (Mitfahrer)": "miv_mitfahrer",
    "(Nahlinien-)Bus": "nahlinien_bus",
    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
    "Motorrad": "motorrad",
    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
    "zu Fuß": "zu_fuss",
    "Sonstiges": "sonstiges"
}

# Sollte Button "Modal Split (Pkm)" ausgewählt sein, dann zeige folgende Expander an
if 'methodik' in st.session_state and st.session_state['methodik'] == "Modal Split (Pkm)":
    with st.expander("**6. Verkehrsmittelverteilung alternativer Verkehrsmittel**"):
        st.info("""**Hinweis:** Bitte geben Sie die Annahmen für die Modal-Split-Verteilung (Personenkilometer) der Fahrgäste an.
                    **Vorauswahl des Modal Split (Personenkilometer):**
    Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Modal-Split-Verteilung automatisch auszufüllen. Diese Werte sind anpassbar.
        """)
        # Dropdown-Menü für Modal-Split-Optionen
        modal_split_options_pkm = {
            "Eigene Angaben Modal Split (Personenkilometer)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Modal Split (Personenkilometer) MiD 2017": [77, 0, 2, 4, 10, 0, 1, 3, 3, 0],
            "Modal Split (Personenkilometer) Essen (2019)": [61, 7, 7.3, 9.7, 6, 0, 0, 4, 5, 0],
            "Modal Split (Personenkilometer) Münster (2022)": [43, 5, 19, 0, 6, 0, 6, 17, 3, 1]
        }
        selected_modal_split_pkm = st.selectbox("Vorauswahl Modal Split (Optional):", list(modal_split_options_pkm.keys()))

        # Speichern der globalen Variablen
        st.session_state['selected_modal_split'] = selected_modal_split_pkm

        # Anzeigen der Anteile basierend auf der ausgewählten Vorauswahl
        default_values = modal_split_options_pkm[selected_modal_split_pkm]

        # Eingabefelder für die Anteile
        transport_modes_pkm = ["MIV (Fahrer)", "MIV (Mitfahrer)", "(Nahlinien-)Bus", "Straßen-/Stadt-/U-Bahn", "Schienen(nah)verkehr/Bahn/Zug", "Motorrad", "E-Bike/Pedelec/E-Lastenrad", "Fahrrad/Lastenrad", "zu Fuß", "Sonstiges"]

        entries_modal_split_pkm = {}

        for i, mode in enumerate(transport_modes_pkm):
            entries_modal_split_pkm[mode] = st.number_input(f"Anteil der Fahrgäste, die {mode} genutzt hätten (%):",
                                            min_value=0.0, max_value=100.0,
                                            value=float(default_values[i]), step=0.1,  format="%f")

        # Überprüfung der Gesamtsumme der eingegebenen Werte
        total_percentage = sum(entries_modal_split_pkm.values())

        if total_percentage > 100:
            st.error("Die Summe der Modal-Split-Anteile überschreitet 100%.")
        elif total_percentage < 100:
            st.warning("Die Summe der Modal-Split-Anteile liegt unter 100%.")

        # Speichern der globalen Variablen
        st.session_state['entries_modal_split'] = entries_modal_split_pkm

        st.write("**Berechnung der Personenkilometer der alternativen Verkehrsmittel**")
        st.info("**Hinweis:** Um die Anzahl der Personenkilometer der alternativen Verkehrsmittel zu berechnen, werden die mit dem Ridepooling zurückgelegten Personenkilometer mit dem entsprechenden Modal-Split-Anteil (Personenkilometer) multipliziert.")

        if 'personenkilometer_gefahren' in st.session_state and 'entries_modal_split' in st.session_state:
            personenkilometer_gefahren = int(st.session_state['personenkilometer_gefahren'])
            st.write(f"Von den zurückgelegten **{personenkilometer_gefahren}** Personenkilometer des Ridepooling-Systems würden entsprechend viele auf folgende alternative Verkehrsmittel entfallen:")
            entries_modal_split_pkm = st.session_state['entries_modal_split']

            berechnete_werte = {}
            for verkehrsmittel, anteil in entries_modal_split_pkm.items():
                berechneter_wert = personenkilometer_gefahren * anteil / 100
                berechnete_werte[mode_to_key_pkm[verkehrsmittel]] = berechneter_wert
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{verkehrsmittel}:**")
                with col2:
                    st.write(f"**{berechneter_wert:.1f} Pkm**")

            st.session_state['berechnete_werte'] = berechnete_werte

            # Berechnung der Gesamtpersonenkilometer für alternative Verkehrsmittel
            personenkilometer_gesamt_av_pkm = round(sum(berechnete_werte.values()), 0)
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write("**Gesamte Personenkilometer für alternative Verkehrsmittel:**")
            with col2:
                st.write(f"**{personenkilometer_gesamt_av_pkm:.1f} Pkm**")

            # Speichern der globalen Variablen
            st.session_state['personenkilometer_gesamt_av_pkm'] = personenkilometer_gesamt_av_pkm

        else:
            st.warning("Bitte stellen Sie sicher, dass die Personenkilometer gefahren und die Modal-Split-Annahmen festgelegt wurden.")

    with st.expander("**7. Emissionsdaten alternativer Verkehrsmittel (Nutzung [TTW] und Energie [WTT])**"):
        st.info("""**Hinweis:** Bitte geben Sie die CO2-Emissionsdaten für die alternativ genutzten Verkehrsmittel an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen.
                    **Vorauswahl der Emissionsdaten:**
                    Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Emissionsdaten automatisch auszufüllen. Diese Werte sind anpassbar.""")

        # Vorauswahl der Emissionsdaten
        vorauswahl_emissionsdaten_optionen_pkm = ["Umweltbundesamt, Umweltfreundlich mobil! (2022)", "Eigene Angaben"]
        selected_vorauswahl_emissionsdaten_pkm = st.selectbox("Vorauswahl der Emissionsdaten:", vorauswahl_emissionsdaten_optionen_pkm)

        # Definieren der Standardemissionswerte basierend auf der Vorauswahl
        if selected_vorauswahl_emissionsdaten_pkm == "Umweltbundesamt, Umweltfreundlich mobil! (2022)":
            emissionsdaten_defaults_pkm = {
                "miv_fahrer": 152.86,
                "miv_mitfahrer": 152.86,
                "nahlinien_bus": 80.54,
                "strassen_stadt_u_bahn": 58.79,
                "schienen_nah_verkehr_bahn_zug": 58.79,
                "motorrad": 90.0,
                "e_bike_pedelec_e_lastenrad": 3.9,
                "fahrrad_lastenrad": 0.0,
                "zu_fuss": 0.0,
                "sonstiges": 0.0
            }
        else:
            emissionsdaten_defaults_pkm = {key: 0 for key in mode_to_key_pkm.values()}

        # Eingabefelder für die Emissionsdaten
        for mode in transport_modes_pkm:
            key = mode_to_key_pkm[mode]
            emission = st.number_input(f"Annahmen Emissionsdaten {mode} [gCO2eq/pkm]:", min_value=0.0, value=float(emissionsdaten_defaults_pkm.get(key, 0)), format='%f')
            st.session_state[f'emission_{key}'] = emission

        st.write("**Berechnung der Emissionen für alternative Verkehrsmittel:**")
        st.info("**Hinweis:** Die Emissionen für die alternativ genutzten Verkehrsmittel werden anhand der Personenkilometer berechnet. Die Formel zur Berechnung der Emissionen lautet: Emissionen = Personenkilometer * Emissionsdaten.")

        st.write("Die Emissionsdaten für die alternativ genutzten Verkehrsmittel betragen:")
        for mode in transport_modes_pkm:
            key = mode_to_key_pkm[mode]
            personenkilometer = st.session_state.get(f'berechnete_werte', {}).get(key, 0)
            emission = st.session_state.get(f'emission_{key}', 0)
            emissionen_av_pkm = round(personenkilometer * emission / 1000, 2)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Emissionen für {mode}:**")
            with col2:
                st.write(f"**{emissionen_av_pkm} kg CO2eq**")

        # Berechnung und Speicherung der Gesamtemissionen für alternative Verkehrsmittel
        gesamtemissionen_av_pkm = round(sum(
            st.session_state.get(f'berechnete_werte', {}).get(mode_to_key_pkm[mode], 0) *
            st.session_state.get(f'emission_{mode_to_key_pkm[mode]}', 0) / 1000
            for mode in transport_modes_pkm
        ), 2)
        st.session_state['gesamtemissionen_av_pkm'] = gesamtemissionen_av_pkm

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Gesamtemissionen für alternative Verkehrsmittel:**")
        with col2:
            st.write(f"**{gesamtemissionen_av_pkm} kg CO2eq**")

        #Speichere gesamtemissionen_av_pkm in globalen Variablen
        st.session_state['gesamtemissionen_av_pkm'] = gesamtemissionen_av_pkm

        # Berechnen der Personenkilometer für alternative Verkehrsmittel
        personenkilometer_gesamt_av_pkm = round(sum(
            st.session_state.get(f'berechnete_werte', {}).get(mode_to_key_pkm[mode], 0)
            for mode in transport_modes_pkm
        ), 2)
        st.session_state['personenkilometer_gesamt_av_pkm'] = personenkilometer_gesamt_av_pkm
        #Speichere die globalen Variablen
        st.session_state['emissionen_pro_personenkilometer_av_pkm'] = gesamtemissionen_av_pkm / personenkilometer_gesamt_av_pkm if personenkilometer_gesamt_av_pkm > 0 else 0

    ### 7. Berechnung Umweltwirkung alternativer Verkehrsmittel
    with st.expander("**8. Berechnung der Umweltwirkung alternativer Verkehrsmittel**"):
        st.info("**Hinweis:** Im Folgenden wird die Umweltwirkung der alternativ genutzten Verkehrsmittel anhand der Mobilitätslage im Raum (Modal Split Pkm) dargestellt. In der Abbildung wird der spezifische CO2-Ausstoß pro Pkm der zunächst alternativen Verkehrsmittel gegenübergestellt.")

        #get co2_emissionen_pro_personenkilometer_rps
        if 'co2_emissionen_pro_personenkilometer_rps' in st.session_state:
            co2_emissionen_pro_personenkilometer_rps = st.session_state['co2_emissionen_pro_personenkilometer_rps']

        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['co2_emissionen_pro_personenkilometer_rps', 'personenkilometer_gesamt_av_pkm', 'gesamtemissionen_av_pkm', 'emissionen_pro_personenkilometer_av_pkm']

        if all(key in st.session_state for key in required_keys):
            personenkilometer_gesamt_av_pkm = st.session_state['personenkilometer_gesamt_av_pkm']
            gesamtemissionen_av_pkm = st.session_state['gesamtemissionen_av_pkm']
            emissionen_pro_personenkilometer_av_pkm = st.session_state['emissionen_pro_personenkilometer_av_pkm']

            emissionen_data = {
                            'Alternative Verkehrsmittel': emissionen_pro_personenkilometer_av_pkm * 1000,
                            'Pkw - MIV (Fahrer) & MIV (Mitfahrer)': 152.86,
                            '(Nahlinien-)Bus': 80.54,
                            'Straßen-/Stadt-/U-Bahn': 59.30,
                            'Schienen(nah)verkehr/Bahn/Zug': 58.79,
                            'Motorrad': 173.3,
                            'E-Bike/Pedelec/E-Lastenrad': 3.9,
                            'Fahrrad/Lastenrad': 0.0,
                            'Zu Fuß': 0.0
                        }

            # Diagramm erstellen
            fig3 = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig3.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig3.update_layout(
                barmode='group',
                title='Gegenüberstellung der Emissionen pro Personenkilometer nach Verkehrsmittel - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig3)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
            with col2:
                st.write(f"**{gesamtemissionen_av_pkm} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av_pkm:.3f} g CO2/pkm**")

        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um den Vergleich der spezifischen CO2-Emissionen pro Personenkilometer durchzuführen.")
            
    #### 8. Vergleich
    st.subheader("Vergleich der spezifischen CO2-Emissionen pro Personenkilometer für das Ridepooling-System und alternative Verkehrsmittel")
    
    # Zeige den Expander Inhalt an, wenn alle erforderlichen Werte vorhanden sind
    with st.expander("**9. Vergleich**"):
        st.info("""**Hinweis:** Im Folgenden wird der spezifische CO2-Ausstoß pro Personenkilometer des Ridepooling-Systems mit denen der alternativ genutzten Verkehrsmittel verglichen.""")
        required_keys = ['co2_emissionen_pro_personenkilometer_rps', 'emissionen_pro_personenkilometer_av_pkm']

        if all(key in st.session_state for key in required_keys):
                co2_emissionen_pro_personenkilometer_rps = st.session_state['co2_emissionen_pro_personenkilometer_rps']
                emissionen_pro_personenkilometer_av_pkm = st.session_state['emissionen_pro_personenkilometer_av_pkm']

                # Erstellung des Diagramms
                emissionen_data = {
                    st.session_state['name_ridepooling_system']: co2_emissionen_pro_personenkilometer_rps * 1000,
                    'Alternative Verkehrsmittel': emissionen_pro_personenkilometer_av_pkm * 1000
                }

                fig2 = go.Figure()
                for verkehrsmittel, emissionen in emissionen_data.items():
                    fig2.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
                fig2.update_layout(
                    barmode='group',
                    title='Gegenüberstellung der spezifischen CO2-Emissionen pro Personenkilometer - Well-to-Wheel (WTW)*',
                    legend=dict(
                        orientation="v",  # vertikale Anordnung
                        y=0.6,  # Positionierung der Legende
                        x=1.02,  # Legende rechts vom Diagramm
                        xanchor='left',
                        yanchor='top'
                    ),
                    width=650,
                    height=650,
                    yaxis_title='Emissionen [g CO2/pkm]',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig2)

                #Get co2_emissionen_gesamt_rps, start_date, end_date, gesamtemissionen_av, und runde auf 2 Dezimalstellen
                co2_emissionen_gesamt_rps = round(st.session_state['co2_emissionen_gesamt_rps'], 2)
                gesamtemissionen_av_pkm = st.session_state['gesamtemissionen_av_pkm']
                start_date = st.session_state['start_date']
                end_date = st.session_state['end_date']

                # Erstellung eines Textfeldes, in welchem die spezifischen CO2-Emissionen pro Personenkilometer des Ridepooling-Systems und der alternativ genutzten Verkehrsmittel verglichen werden
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Gesamte CO2-Emissionen des Ridepooling-Systems:**")
                with col2:
                    st.write(f"**{co2_emissionen_gesamt_rps:.2f} kg CO2**")

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**CO2-Emissionen des Ridepooling-Systems pro Personenkilometer:**")
                with col2:
                    st.write(f"**{co2_emissionen_pro_personenkilometer_rps:.3f} kg CO2/pkm**")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
                with col2:
                    st.write(f"**{gesamtemissionen_av_pkm} kg CO2**")

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
                with col2:
                    st.write(f"**{emissionen_pro_personenkilometer_av_pkm:.3f} kg CO2/pkm**")
                            
                # Erstelle ein Textfeld, in welchem je nach Ausgang des Vergleichs eine entsprechende Meldung ausgegeben wird
                if emissionen_pro_personenkilometer_av_pkm != 0:
                    if co2_emissionen_pro_personenkilometer_rps < emissionen_pro_personenkilometer_av_pkm:
                        percentage_difference = round((emissionen_pro_personenkilometer_av_pkm - co2_emissionen_pro_personenkilometer_rps) / emissionen_pro_personenkilometer_av_pkm * 100, 2)
                        total_difference = round((gesamtemissionen_av_pkm - co2_emissionen_gesamt_rps), 2)
                        st.success(f"Das Ridepooling-System weist im Vergleich zu den alternativ genutzten Verkehrsmitteln eine geringere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % niedriger als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Einsparung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                    elif co2_emissionen_pro_personenkilometer_rps > emissionen_pro_personenkilometer_av_pkm:
                        percentage_difference = round((co2_emissionen_pro_personenkilometer_rps - emissionen_pro_personenkilometer_av_pkm) / emissionen_pro_personenkilometer_av_pkm * 100, 2)
                        total_difference = round((co2_emissionen_gesamt_rps - gesamtemissionen_av_pkm), 2)
                        st.error(f"Das Ridepooling-System weist im Vergleich zu den den alternativ genutzten Verkehrsmitteln eine höhere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % höher als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Erhöhung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                    else:
                        st.warning("Das Ridepooling-System und die alternativen Verkehrsmittel weisen die gleiche spezifische CO2-Emission pro Personenkilometer auf.")
        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um den Vergleich der spezifischen CO2-Emissionen pro Personenkilometer durchzuführen.")
                
    # Export
    with st.expander("**10. Export der Eingabedaten und Ergebnisse**"):
        st.info("**Hinweis:** Im Folgenden wird der spezifische CO2-Ausstoß pro Personenkilometer des Ridepooling-Systems mit denen der alternativ genutzten Verkehrsmittel verglichen.")
        # Stellen Sie sicher, dass alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = [
            'name_ridepooling_system', 'start_date', 'end_date', 'abgeschlossene_buchungen',
            'transportierte_fahrgaeste', 'vehicle_list', 'fahrzeugkilometer_leer', 'fahrzeugkilometer_besetzt',
            'fahrzeugkilometer_gesamt', 'durchschnittliche_fahrtdistanz_mit_lk', "durchschnittliche_fahrtdistanz_mit_bk",
            'personenkilometer_gefahren', 'benzinverbrauch_gesamt', 'dieselverbrauch_gesamt', 'stromverbrauch_gesamt',
            'oekostrom_anteil', 'benzin_emissionsdaten', 'diesel_emissionsdaten', 'strom_emissionsdaten',
            'co2_emissionen_gesamt_rps', 'co2_emissionen_pro_personenkilometer_rps', 'personenkilometer_gesamt_av',
            'gesamtemissionen_av', 'emissionen_pro_personenkilometer_av', 'entries_modal_split'
        ]
        missing_keys = [key for key in required_keys if key not in st.session_state]
        if missing_keys:
            st.error(f"Die folgenden Schlüssel fehlen: {', '.join(missing_keys)}")
        else:
            st.write("Die Eingabedaten und Ergebnisse können als CSV-Datei exportiert werden.")
            if st.button("Exportieren"):
                # Erstellen eines DataFrames mit den Eingabedaten und Ergebnissen des Ridepooling-Systems
                data_rps = {
                    "Merkmal": ["Wert"],
                    "Ridepooling-System": [st.session_state['name_ridepooling_system']],
                    "Betrachtungszeitraum (Start)": [f"{st.session_state['start_date']}"],
                    "Betrachtungszeitraum (Ende)": [f"{st.session_state['end_date']}"],
                    "Anzahl abgeschlossener Buchungen": [st.session_state['abgeschlossene_buchungen']],
                    "Transportierte Fahrgäste": [st.session_state['transportierte_fahrgaeste']],
                    "Flotte - Fahrzeugkilometer (leer)": [st.session_state['fahrzeugkilometer_leer']],
                    "Flotte - Fahrzeugkilometer (besetzt)": [st.session_state['fahrzeugkilometer_besetzt']],
                    "Flotte - Fahrzeugkilometer (gesamt)": [st.session_state['fahrzeugkilometer_gesamt']],
                    "Durchschnittliche Fahrtdistanz (mit Fahrgast)": [st.session_state['durchschnittliche_fahrtdistanz_mit_bk']],
                    "Durchschnittliche Fahrtdistanz (ohne Fahrgast)": [st.session_state['durchschnittliche_fahrtdistanz_mit_lk']],
                    "Flotte - Benzinverbrauch (gesamt)": [st.session_state['benzinverbrauch_gesamt']],
                    "Flotte - Dieselverbrauch (gesamt)": [st.session_state['dieselverbrauch_gesamt']],
                    "Flotte - Stromverbrauch (gesamt)": [st.session_state['stromverbrauch_gesamt']],
                    "Ökostromanteil (%)": [st.session_state['oekostrom_anteil']],
                    "CO2-Emissionsdaten (Benzin)": [st.session_state['benzin_emissionsdaten']],
                    "CO2-Emissionsdaten (Diesel)": [st.session_state['diesel_emissionsdaten']],
                    "CO2-Emissionsdaten (Strom)": [st.session_state['strom_emissionsdaten']],
                    "CO2-Emissionen (gesamt)": [st.session_state['co2_emissionen_gesamt_rps']],
                    "CO2-Emissionen pro Personenkilometer": [st.session_state['co2_emissionen_pro_personenkilometer_rps']]
                }

                df_rps = pd.DataFrame(data_rps).transpose()
                df_rps.columns = df_rps.iloc[0]
                df_rps = df_rps[1:]

                # Erstellen eines DataFrames mit den Fahrzeugdaten
                if 'vehicle_list' in st.session_state and st.session_state['vehicle_list']:
                    vehicle_data = {
                        "Fahrzeugtyp": [],
                        "Benzinverbrauch (l/100km)": [],
                        "Dieselverbrauch (l/100km)": [],
                        "Stromverbrauch (kWh/100km)": [],
                        "Kilometer leer": [],
                        "Kilometer besetzt": []
                    }
                    for vehicle in st.session_state['vehicle_list']:
                        if isinstance(vehicle, dict) and all(key in vehicle for key in ['Fahrzeugtyp', 'Kilometer leer', 'Kilometer besetzt']):
                            vehicle_data["Fahrzeugtyp"].append(vehicle['Fahrzeugtyp'])
                            vehicle_data["Benzinverbrauch (l/100km)"].append(vehicle['Benzinverbrauch (l/100km)'])
                            vehicle_data["Dieselverbrauch (l/100km)"].append(vehicle['Dieselverbrauch (l/100km)'])
                            vehicle_data["Stromverbrauch (kWh/100km)"].append(vehicle['Stromverbrauch (kWh/100km)'])
                            vehicle_data["Kilometer leer"].append(vehicle['Kilometer leer'])
                            vehicle_data["Kilometer besetzt"].append(vehicle['Kilometer besetzt'])

                    df_vehicles = pd.DataFrame(vehicle_data)
                else:
                    st.error("No vehicles in the session state or 'vehicle_list' is not set.")
                    df_vehicles = pd.DataFrame()

                # Erstellen eines DataFrames mit den Emissionsdaten der alternativ genutzten Verkehrsmittel, Modal Split, Emissions
                mode_to_key_pkm = {
                    "MIV (Fahrer)": "miv_fahrer",
                    "MIV (Mitfahrer)": "miv_mitfahrer",
                    "(Nahlinien-)Bus": "nahlinien_bus",
                    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
                    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
                    "Motorrad": "motorrad",
                    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
                    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
                    "zu Fuß": "zu_fuss",
                    "Sonstiges": "sonstiges"
                }

                data_av_pkm = {
                    "Merkmal": ["Wert"],
                    "Gesamtemissionen alternative Verkehrsmittel (kg CO2eq)": [st.session_state['gesamtemissionen_av_pkm']],
                    "Personenkilometer alternative Verkehrsmittel (km)": [st.session_state['personenkilometer_gesamt_av_pkm']],
                    "CO2-Emissionen pro Personenkilometer alternative Verkehrsmittel (g CO2eq/pkm)": [st.session_state['emissionen_pro_personenkilometer_av_pkm']]
                }

                # Hinzufügen der Modal Split Daten  
                for verkehrsmittel, anteil in st.session_state['entries_modal_split'].items():
                    key = mode_to_key_pkm.get(verkehrsmittel, verkehrsmittel)
                    data_av_pkm[f"Modal Split Anteil für {verkehrsmittel} (%)"] = [anteil]

                # Hinzufügen der Emissionsdaten für alternative Verkehrsmittel
                for mode in st.session_state['entries_modal_split']:
                    key = mode_to_key_pkm.get(mode, mode)
                    personenkilometer = st.session_state.get(f'berechnete_werte', {}).get(key, 0)
                    emission = st.session_state.get(f'emission_{key}', 0)
                    data_av_pkm[f"Wegehäufigkeit für {mode} (Personenkilometer)"] = [personenkilometer]
                    data_av_pkm[f"Emissionsdaten für {mode} (g CO2eq/pkm)"] = [emission]
                
                df_av_pkm = pd.DataFrame(data_av_pkm).transpose()
                df_av_pkm.columns = df_av_pkm.iloc[0]
                df_av_pkm = df_av_pkm[1:]

                # Zusammenführen der DataFrames
                df_combined = pd.concat([df_rps, df_vehicles, df_av_pkm], axis=0)
                df_combined = df_combined.replace('', np.nan)
                st.write(df_combined)

#########################################################################################
# Umfrage (Wege)

mode_to_key_umfrage_wege = {
    "Verkehrsinduktion": "verkehrsinduktion",
    "MIV (Fahrer)": "miv_fahrer",
    "MIV (Mitfahrer)": "miv_mitfahrer",
    "(Nahlinien-)Bus": "nahlinien_bus",
    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
    "Motorrad": "motorrad",
    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
    "zu Fuß": "zu_fuß",
    "Sonstiges": "sonstiges"
}

### Verkehrsmittelverteilung Umfrage (Wege)
if 'methodik' in st.session_state and st.session_state['methodik'] == "Umfrage (Wege)":
    with st.expander("**6. Verkehrsmittelverteilung alternativer Verkehrsmittel**"):
        st.info("""**Hinweis:** Bitte geben Sie die Annahmen für die Verteilung der alternativen Verkehrsmittelverteilung der Fahrgäste an.
                    **Vorauswahl der Umfrage (Wege):** Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Verteilung automatisch auszufüllen. Diese Werte sind anpassbar.""")
        # Dropdown-Menü für Umfrage_wege
        umfrage_wege_options = {
            "Eigene Angaben": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Umfrage LOOPmünster (2021, 2022, 2022)": [0, 31, 9, 7, 0, 2, 0, 10, 24, 17, 0]
        }

        selected_modal_split_umfrage_wege = st.selectbox("Vorauswahl Umfrage (Wege) (Optional):", list(umfrage_wege_options.keys()))

        # Speichern der globalen Variablen
        st.session_state['selected_modal_split_umfrage_wege'] = selected_modal_split_umfrage_wege

        # Anzeigen der Anteile basierend auf der ausgewählten Vorauswahl
        default_values_umfrage_wege = umfrage_wege_options[selected_modal_split_umfrage_wege]

        # Eingabefelder für die Anteile
        transport_modes_umfrage_wege = ["Verkehrsinduktion", "MIV (Fahrer)", "MIV (Mitfahrer)", "(Nahlinien-)Bus", "Straßen-/Stadt-/U-Bahn", "Schienen(nah)verkehr/Bahn/Zug", "Motorrad", "E-Bike/Pedelec/E-Lastenrad", "Fahrrad/Lastenrad", "zu Fuß", "Sonstiges"]
        entries_umfrage_wege = {}
        for i, mode_umfrage_wege in enumerate(transport_modes_umfrage_wege):
            entries_umfrage_wege[mode_umfrage_wege] = st.number_input(f"Anteil der Fahrgäste, die {mode_umfrage_wege} genutzt hätten (%):", 
                                            min_value=0.0, max_value=100.0, 
                                            value=float(default_values_umfrage_wege[i]), step=0.1, format="%f")

        # Überprüfung der Gesamtsumme der eingegebenen Werte
        total_percentage = sum(entries_umfrage_wege.values())
        if total_percentage > 100:
            st.error("Die Summe der Modal-Split-Anteile überschreitet 100%.")
        elif total_percentage < 100:
            st.warning("Die Summe der Modal-Split-Anteile liegt unter 100%.")

        # Außerhalb des Expanders
        st.write("**Berechnung der Personenkilometer der alternativen Verkehrsmittel**")
        st.info("**Hinweis:** Um die Anzahl der Personenkilometer der alternativen Verkehrsmittel zu berechnen, werden die mit dem Ridepooling beförderten Fahrgäste mit den entsprechenden Verkehrsmittelverteilung-Anteilen (Umfrage, Wege) multipliziert.")

        #Speichern der globalen Variablen
        st.session_state['entries_umfrage_wege'] = entries_umfrage_wege

        if 'transportierte_fahrgaeste' in st.session_state and 'entries_umfrage_wege' in st.session_state:
            transportierte_fahrgaeste = int(st.session_state['transportierte_fahrgaeste'])
            st.write(f"Von den **{int(st.session_state['transportierte_fahrgaeste'])}** transportierten Fahrgästen hätten entsprechend viele Personen folgende alternative Verkehrsmittel genutzt:")
            entries_umfrage_wege = st.session_state['entries_umfrage_wege']
            
            for verkehrsmittel, anteil_umfrage_wege in entries_umfrage_wege.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{verkehrsmittel}:**")
                with col2:
                    berechneter_wert = transportierte_fahrgaeste * anteil_umfrage_wege / 100
                    st.write(f"**{berechneter_wert:.0f} Personen**")
                    
        else:
            st.warning("Bitte stellen Sie sicher, dass die Gesamtzahl der transportierten Fahrgäste und die Modal-Split-Annahmen festgelegt wurden.")

    ######## 7. Annahmen für die Wegeentfernung alternativer Verkehrsmitteln

    # Initialisierung der benötigten Variablen, falls nicht vorhanden
    if 'durchschnittliche_fahrtdistanz_mit_bk' not in st.session_state:
        st.session_state['durchschnittliche_fahrtdistanz_mit_bk'] = 0.0
    if 'durchschnittliche_fahrtdistanz_mit_lk' not in st.session_state: 
        st.session_state['durchschnittliche_fahrtdistanz_mit_lk'] = 0.0
    if 'transportierte_fahrgaeste' not in st.session_state:
        st.session_state['transportierte_fahrgaeste'] = 0
    if 'entries_umfrage_wege' not in st.session_state:
        st.session_state['entries_umfrage_wege'] = {}

    mode_to_key_umfrage_wege = {
        "Verkehrsinduktion": "verkehrsinduktion",
        "MIV (Fahrer)": "miv_fahrer",
        "MIV (Mitfahrer)": "miv_mitfahrer",
        "(Nahlinien-)Bus": "nahlinien_bus",
        "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
        "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
        "Motorrad": "motorrad",
        "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
        "Fahrrad/Lastenrad": "fahrrad_lastenrad",
        "Zu Fuß": "zu_fuss",
        "Sonstiges": "sonstiges"
    }

    # Sicherstellen, dass die Transportmodi konsistent benannt sind
    transport_modes_umfrage_wege = list(mode_to_key_umfrage_wege.keys())

    with st.expander("**7. Wegeentfernung alternativer Verkehrsmittel**"):
        st.info("""**Hinweis:** Bitte geben Sie die Annahmen zur Wegeentfernung der alternativ genutzten Verkehrsmittel an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen.""")

        
        
        vorauswahl_optionen_umfrage_wege = {
            "Durchschnittliche Fahrtdistanz je Buchung (mit Fahrgast)": st.session_state['durchschnittliche_fahrtdistanz_mit_bk'],
            "Durchschnittliche Fahrtdistanz je Buchung (mit Leerkilometern)": st.session_state['durchschnittliche_fahrtdistanz_mit_lk'],
            "Durchschnittliche Reiseweiten nach MID 2017": {
                "Verkehrsinduktion": 0.0,
                "MIV (Fahrer)": 16.0,
                "MIV (Mitfahrer)": 18.0,
                "(Nahlinien-)Bus": 23.0,
                "Straßen-/Stadt-/U-Bahn": 23.0,
                "Schienen(nah)verkehr/Bahn/Zug": 23.0,
                "Motorrad": 16.0,
                "E-Bike/Pedelec/E-Lastenrad": 4.0,
                "Fahrrad/Lastenrad": 4.0,
                "Zu Fuß": 2.0,
                "Sonstiges": 0.0
            }
        }

        selected_vorauswahl_umfrage_wege = st.selectbox("Vorauswahl der Wegeentfernung:", list(vorauswahl_optionen_umfrage_wege.keys()))

        if selected_vorauswahl_umfrage_wege in ["Durchschnittliche Fahrtdistanz je Buchung (mit Fahrgast)", "Durchschnittliche Fahrtdistanz je Buchung (mit Leerkilometern)"]:
            default_distance = vorauswahl_optionen_umfrage_wege[selected_vorauswahl_umfrage_wege]
            default_distances_umfrage_wege = {mode: default_distance for mode in transport_modes_umfrage_wege}
        else:
            default_distances_umfrage_wege = vorauswahl_optionen_umfrage_wege[selected_vorauswahl_umfrage_wege]

        for mode in transport_modes_umfrage_wege:
            key = mode_to_key_umfrage_wege[mode]
            distance_umfrage_wege = st.number_input(f"Wegeentfernung {mode} [km]:", min_value=0.0, value=float(default_distances_umfrage_wege.get(mode, 0)), format='%f')
            st.session_state[f'entfernung_{key}'] = distance_umfrage_wege

        st.write("**Berechnung der Personenkilometer der alternativen Verkehrsmittel**")
        st.info("**Hinweis:** Die Personenkilometer der alternativ genutzten Verkehrsmittel werden basierend auf den Annahmen zur Wegeentfernung und der Verkehrsmittelverteilung der Fahrgäste berechnet.")

        # Berechnung und Speicherung der Personenkilometer für jedes Verkehrsmittel
        st.write("Die Berechnung der Personenkilometer für die verschiedenen alternativen Verkehrsmittel ergibt folgende Werte:")
        for mode in transport_modes_umfrage_wege:
            key = mode_to_key_umfrage_wege[mode]
            transportierte_fahrgaeste = int(st.session_state['transportierte_fahrgaeste'])
            modal_split = float(st.session_state['entries_umfrage_wege'].get(mode, 0))
            personen = transportierte_fahrgaeste * (modal_split / 100)
            entfernung = float(st.session_state.get(f'entfernung_{key}', 0))
            personenkilometer = round(personen * entfernung, 2)
            st.session_state[f'personenkilometer_{key}'] = personenkilometer
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{mode}**:")
            with col2:
                st.write(f"**{personenkilometer} Pkm**")

        # Berechnung der Gesamt-Personenkilometer für alternative Verkehrsmittel
        personenkilometer_gesamt_av_umfrage_wege = round(sum(
                    float(st.session_state.get(f'personenkilometer_{mode_to_key_umfrage_wege[mode]}', 0))
                    for mode in transport_modes_umfrage_wege if mode != "Verkehrsinduktion"), 0)
        col1, col2 = st.columns([3, 1])
        with col1:
                    st.write("**Gesamte Personenkilometer für alternative Verkehrsmittel:**")
        with col2:
                    st.write(f"**{personenkilometer_gesamt_av_umfrage_wege} Pkm**")

        st.info("**Hinweis:** Die Verkehrsinduktion wird bei der Berechnung der Gesamt-Personenkilometer nicht berücksichtigt.")

        # Speichern der globalen Variablen
        st.session_state['personenkilometer_gesamt_av'] = personenkilometer_gesamt_av_umfrage_wege

        ##### 7. Emissionsdaten alternativer Verkehrsmittel (Nutzung [TTW] und Energie [WTT])
    with st.expander("**8. Emissionsdaten alternativer Verkehrsmittel (Nutzung [TTW] und Energie [WTT])**"):
        st.info("**Hinweis:** Bitte geben Sie die CO2-Emissionsdaten für die alternativ genutzten Verkehrsmittel an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen. **Vorauswahl der Emissionsdaten:** Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Emissionsdaten automatisch auszufüllen. Diese Werte sind anpassbar.")
        # Vorauswahl der Emissionsdaten
        vorauswahl_emissionsdaten_optionen_umfrage_wege = ["Eigene Angaben", "Umweltbundesamt, Umweltfreundlich mobil! (2022)"]
        selected_vorauswahl_emissionsdaten_umfrage_wege = st.selectbox("Vorauswahl der Emissionsdaten:", vorauswahl_emissionsdaten_optionen_umfrage_wege)

        # Definieren der Standardemissionswerte basierend auf der Vorauswahl
        if selected_vorauswahl_emissionsdaten_umfrage_wege == "Umweltbundesamt, Umweltfreundlich mobil! (2022)":
                emissionsdaten_defaults_umfrage_wege = {
                    "verkehrsinduktion": 0.0,
                    "miv_fahrer": 152.86,
                    "miv_mitfahrer": 152.86,
                    "nahlinien_bus": 80.54,
                    "strassen_stadt_u_bahn": 58.79,
                    "schienen_nah_verkehr_bahn_zug": 58.79,
                    "motorrad": 90.0,
                    "e_bike_pedelec_e_lastenrad": 3.9,
                    "fahrrad_lastenrad": 0.0,
                    "zu_fuß": 0.0,
                    "sonstiges": 0.0
                }
        else:
                emissionsdaten_defaults_umfrage_wege = {key: 0 for key in mode_to_key_umfrage_wege.values()}

            # Eingabefelder für die Emissionsdaten
        for mode in transport_modes_umfrage_wege:
                key = mode_to_key_umfrage_wege[mode]
                emission_umfrage_wege = st.number_input(f"Annahmen Emissionsdaten {mode} [gCO2eq/pkm]:", min_value=0.0, value=float(emissionsdaten_defaults_umfrage_wege.get(key, 0)), format='%f')
                st.session_state[f'emission_{key}'] = emission_umfrage_wege

        st.write("**Berechnung der Personenkilometer für alternative Verkehrsmittel**")
        st.info("**Hinweis:** Die Personenkilometer der alternativ genutzten Verkehrsmittel werden basierend auf den Annahmen zur Wegeentfernung und den Emissionsdaten berechnet.")
        st.write("Die Emissionsdaten für die alternativ genutzten Verkehrsmittel betragen:")

        for mode in transport_modes_umfrage_wege:
                key = mode_to_key_umfrage_wege[mode]
                personenkilometer_umfrage_wege = st.session_state.get(f'personenkilometer_{key}', 0)
                emission_umfrage_wege = st.session_state.get(f'emission_{key}', 0)
                emissionen_av_umfrage_wege = round(personenkilometer_umfrage_wege * emission_umfrage_wege / 1000, 2)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Emissionen für {mode}:**")
                with col2:
                    st.write(f"**{emissionen_av_umfrage_wege} kg CO2eq**")

            # Berechnung und Speicherung der Gesamtemissionen für alternative Verkehrsmittel
        gesamtemissionen_av_umfrage_wege = round(sum(
                st.session_state.get(f'personenkilometer_{mode_to_key_umfrage_wege[mode]}', 0) *
                st.session_state.get(f'emission_{mode_to_key_umfrage_wege[mode]}', 0) / 1000
                for mode in transport_modes_umfrage_wege if mode != "Verkehrsinduktion"
            ), 2)

        st.session_state['gesamtemissionen_av_umfrage_wege'] = gesamtemissionen_av_umfrage_wege

        col1, col2 = st.columns([3, 1])
        with col1:
                st.write("**Gesamtemissionen für alternative Verkehrsmittel:**")
        with col2:
                st.write(f"**{gesamtemissionen_av_umfrage_wege} kg CO2eq**")

        # Berechnen der Personenkilometer für alternative Verkehrsmittel


        personenkilometer_gesamt_av_umfrage_wege = round(sum(
                st.session_state.get(f'personenkilometer_{mode_to_key_umfrage_wege[mode]}', 0)
                for mode in transport_modes_umfrage_wege if mode != "Verkehrsinduktion"
            ), 2)
        st.session_state['personenkilometer_gesamt_av_umfrage_wege'] = personenkilometer_gesamt_av_umfrage_wege
            #Speichere die globalen Variablen
        st.session_state['emissionen_pro_personenkilometer_av'] = gesamtemissionen_av_umfrage_wege / personenkilometer_gesamt_av_umfrage_wege if personenkilometer_gesamt_av_umfrage_wege > 0 else 0
        #Speichere die globalen Variablen
        st.session_state['gesamtemissionen_av_umfrage_wege'] = gesamtemissionen_av_umfrage_wege

    ######## 9. Berechnung der Umweltwirkung alternativer Verkehrsmittel
    with st.expander("**9. Berechnung der Umweltwirkung alternativer Verkehrsmittel**"):
        st.info("""**Hinweis:** Im Folgenden wird die Umweltwirkung der alternativ genutzten Verkehrsmittel anhand von Umfragedaten im Raum (Umfragedaten, Wege) dargestellt. In der Abbildung wird der spezifische CO2-Ausstoß pro alternativen Verkehrsmittel denen anderer Verkehrsmittel gegenübergestellt.""")
        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['gesamtemissionen_av_umfrage_wege', 'personenkilometer_gesamt_av_umfrage_wege']
        if all(key in st.session_state for key in required_keys):
            gesamtemissionen_av_umfrage_wege = st.session_state['gesamtemissionen_av_umfrage_wege']
            personenkilometer_gesamt_av_umfrage_wege = st.session_state['personenkilometer_gesamt_av_umfrage_wege']

            # Berechnung der Emissionen pro Personenkilometer
            emissionen_pro_personenkilometer_av_umfrage_wege = gesamtemissionen_av_umfrage_wege / personenkilometer_gesamt_av_umfrage_wege if personenkilometer_gesamt_av_umfrage_wege > 0 else 0

            # Speichere die berechneten Werte im Sitzungszustand
            st.session_state['emissionen_pro_personenkilometer_av_umfrage_wege'] = emissionen_pro_personenkilometer_av_umfrage_wege

            emissionen_data = {
                'Alternative Verkehrsmittel': emissionen_pro_personenkilometer_av_umfrage_wege * 1000,
                'Pkw - MIV (Fahrer) & MIV (Mitfahrer)': 152.86,
                '(Nahlinien-)Bus': 80.54,
                'Straßen-/Stadt-/U-Bahn': 59.30,
                'Schienen(nah)verkehr/Bahn/Zug': 58.79,
                'Motorrad': 173.3,
                'E-Bike/Pedelec/E-Lastenrad': 3.9,
                'Fahrrad/Lastenrad': 0.0,
                'Zu Fuß': 0.0
            }

            # Diagramm erstellen
            fig = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig.update_layout(
                barmode='group',
                title='Gegenüberstellung der Emissionen pro Personenkilometer nach Verkehrsmittel - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
            with col2:
                st.write(f"**{gesamtemissionen_av_umfrage_wege} kg CO2**")
            st.session_state['gesamtemissionen_av_umfrage_wege'] = gesamtemissionen_av_umfrage_wege

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av_umfrage_wege:.3f} g CO2/pkm**")

            # SPEICHERN DER GLOBALEN VARIABLEN
            st.session_state['emissionen_pro_personenkilometer_av_umfrage_wege'] = emissionen_pro_personenkilometer_av_umfrage_wege

        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um die Umweltwirkung der alternativen Verkehrsmittel zu berechnen.")
    
    st.subheader("Vergleich der spezifischen CO2-Emissionen pro Personenkilometer für das Ridepooling-System und alternative Verkehrsmittel")

    ######## 10. Vergleich
    with st.expander("**10. Vergleich**"):
        st.info("""**Hinweis:** Im Folgenden wird der spezifische CO2-Ausstoß pro Personenkilometer des Ridepooling-Systems mit denen der alternativ genutzten Verkehrsmittel verglichen.""")

        'initialisierung der benötigten Variablen, falls nicht vorhanden'
        if 'co2_emissionen_pro_personenkilometer_rps_umfrage_wege' not in st.session_state:
            st.session_state['co2_emissionen_pro_personenkilometer_rps_umfrage_wege'] = 0.0
        if 'emissionen_pro_personenkilometer_av_umfrage_wege' not in st.session_state:
            st.session_state['emissionen_pro_personenkilometer_av_umfrage_wege'] = 0.0
        if 'co2_emissionen_gesamt_rps_umfrage_wege' not in st.session_state:
            st.session_state['co2_emissionen_gesamt_rps_umfrage_wege'] = 0.0
        if 'gesamtemissionen_av_umfrage_wege' not in st.session_state:
            st.session_state['gesamtemissionen_av_umfrage_wege'] = 0.0
        if 'start_date' not in st.session_state:
            st.session_state['start_date'] = ""
        if 'end_date' not in st.session_state:
            st.session_state['end_date'] = ""


        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['emissionen_pro_personenkilometer_av_umfrage_wege', 'co2_emissionen_pro_personenkilometer_rps', 'gesamtemissionen_av_umfrage_wege', 'start_date', 'end_date']

        if all(key in st.session_state for key in required_keys):
            co2_emissionen_pro_personenkilometer_rps = st.session_state['co2_emissionen_pro_personenkilometer_rps']
            emissionen_pro_personenkilometer_av_umfrage_wege = st.session_state['emissionen_pro_personenkilometer_av_umfrage_wege']

            # Erstellung des Diagramms
            emissionen_data = {
                st.session_state['name_ridepooling_system']: co2_emissionen_pro_personenkilometer_rps * 1000,
                'Alternative Verkehrsmittel': emissionen_pro_personenkilometer_av_umfrage_wege * 1000
            }

            fig5 = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig5.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig5.update_layout(
                barmode='group',
                title='Gegenüberstellung der spezifischen CO2-Emissionen pro Personenkilometer - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig5)

            #Get co2_emissionen_gesamt_rps, start_date, end_date, gesamtemissionen_av, und runde auf 2 Dezimalstellen
            co2_emissionen_gesamt_rps = round(st.session_state['co2_emissionen_gesamt_rps'], 2)
            gesamtemissionen_av_umfrage_wege = st.session_state['gesamtemissionen_av_umfrage_wege']
            start_date = st.session_state['start_date']
            end_date = st.session_state['end_date']

            # Erstellung eines Textfeldes, in welchem die spezifischen CO2-Emissionen pro Personenkilometer des Ridepooling-Systems und der alternativ genutzten Verkehrsmittel verglichen werden
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen des Ridepooling-Systems:**")
            with col2:
                st.write(f"**{co2_emissionen_gesamt_rps:.2f} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen des Ridepooling-Systems pro Personenkilometer:**")
            with col2:
                st.write(f"**{co2_emissionen_pro_personenkilometer_rps:.3f} kg CO2/pkm**")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
            with col2:
                st.write(f"**{gesamtemissionen_av_umfrage_wege} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av_umfrage_wege:.3f} kg CO2/pkm**")
                         
            # Erstelle ein Textfeld, in welchem je nach Ausgang des Vergleichs eine entsprechende Meldung ausgegeben wird
            if emissionen_pro_personenkilometer_av_umfrage_wege != 0:
                if co2_emissionen_pro_personenkilometer_rps < emissionen_pro_personenkilometer_av_umfrage_wege:
                    percentage_difference = round((emissionen_pro_personenkilometer_av_umfrage_wege - co2_emissionen_pro_personenkilometer_rps) / emissionen_pro_personenkilometer_av_umfrage_wege * 100, 2)
                    total_difference = round((gesamtemissionen_av_umfrage_wege - co2_emissionen_gesamt_rps), 2)
                    st.success(f"Das Ridepooling-System weist im Vergleich zu den alternativ genutzten Verkehrsmitteln eine geringere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % niedriger als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Einsparung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                elif co2_emissionen_pro_personenkilometer_rps > emissionen_pro_personenkilometer_av_umfrage_wege:
                    percentage_difference = round((co2_emissionen_pro_personenkilometer_rps - emissionen_pro_personenkilometer_av_umfrage_wege) / emissionen_pro_personenkilometer_av_umfrage_wege * 100, 2)
                    total_difference = round((co2_emissionen_gesamt_rps - gesamtemissionen_av_umfrage_wege), 2)
                    st.error(f"Das Ridepooling-System weist im Vergleich zu den den alternativ genutzten Verkehrsmitteln eine höhere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % höher als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Erhöhung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                else:
                    st.warning("Das Ridepooling-System und die alternativen Verkehrsmittel weisen die gleiche spezifische CO2-Emission pro Personenkilometer auf.")
        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um den Vergleich der spezifischen CO2-Emissionen pro Personenkilometer durchzuführen.")
    
        
    with st.expander("**11. Export der Eingabedaten und Ergebnisse**"):
        # Stellen Sie sicher, dass alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = [
            'name_ridepooling_system', 'start_date', 'end_date', 'abgeschlossene_buchungen',
            'transportierte_fahrgaeste', 'vehicle_list', 'fahrzeugkilometer_leer', 'fahrzeugkilometer_besetzt',
            'fahrzeugkilometer_gesamt', 'durchschnittliche_fahrtdistanz_mit_bk', "durchschnittliche_fahrtdistanz_mit_lk",
            'personenkilometer_gefahren', 'benzinverbrauch_gesamt', 'dieselverbrauch_gesamt', 'stromverbrauch_gesamt',
            'oekostrom_anteil', 'benzin_emissionsdaten', 'diesel_emissionsdaten', 'strom_emissionsdaten',
            'co2_emissionen_gesamt_rps', 'co2_emissionen_pro_personenkilometer_rps', 'personenkilometer_gesamt_av_umfrage_wege',
            'gesamtemissionen_av_umfrage_wege', 'emissionen_pro_personenkilometer_av_umfrage_wege', 'entries_umfrage_wege'
        ]
        missing_keys = [key for key in required_keys if key not in st.session_state]
        if missing_keys:
            st.error(f"Die folgenden Schlüssel fehlen: {', '.join(missing_keys)}")
        else:
            st.write("Die Eingabedaten und Ergebnisse können als CSV-Datei exportiert werden.")
            if st.button("Exportieren"):
                # Erstellen eines DataFrames mit den Eingabedaten und Ergebnissen des Ridepooling-Systems
                data_rps = {
                    "Merkmal": ["Wert"],
                    "Ridepooling-System": [st.session_state['name_ridepooling_system']],
                    "Betrachtungszeitraum (Start)": [f"{st.session_state['start_date']}"],
                    "Betrachtungszeitraum (Ende)": [f"{st.session_state['end_date']}"],
                    "Anzahl abgeschlossener Buchungen": [st.session_state['abgeschlossene_buchungen']],
                    "Transportierte Fahrgäste": [st.session_state['transportierte_fahrgaeste']],
                    "Flotte - Fahrzeugkilometer (leer)": [st.session_state['fahrzeugkilometer_leer']],
                    "Flotte - Fahrzeugkilometer (besetzt)": [st.session_state['fahrzeugkilometer_besetzt']],
                    "Flotte - Fahrzeugkilometer (gesamt)": [st.session_state['fahrzeugkilometer_gesamt']],
                    "Flotte - Personenkilometer (gefahren)": [st.session_state['personenkilometer_gefahren']],
                    "Durchschnittliche Fahrtdistanz (mit Fahrgast)": [st.session_state['durchschnittliche_fahrtdistanz_mit_bk']],
                    "Durchschnittliche Fahrtdistanz (ohne Fahrgast)": [st.session_state['durchschnittliche_fahrtdistanz_mit_lk']],
                    "Flotte - Benzinverbrauch (gesamt)": [st.session_state['benzinverbrauch_gesamt']],
                    "Flotte - Dieselverbrauch (gesamt)": [st.session_state['dieselverbrauch_gesamt']],
                    "Flotte - Stromverbrauch (gesamt)": [st.session_state['stromverbrauch_gesamt']],
                    "Ökostromanteil (%)": [st.session_state['oekostrom_anteil']],
                    "CO2-Emissionsdaten (Benzin)": [st.session_state['benzin_emissionsdaten']],
                    "CO2-Emissionsdaten (Diesel)": [st.session_state['diesel_emissionsdaten']],
                    "CO2-Emissionsdaten (Strom)": [st.session_state['strom_emissionsdaten']],
                    "CO2-Emissionen (gesamt)": [st.session_state['co2_emissionen_gesamt_rps']],
                    "CO2-Emissionen pro Personenkilometer": [st.session_state['co2_emissionen_pro_personenkilometer_rps']]
                }

                df_rps = pd.DataFrame(data_rps).transpose()
                df_rps.columns = df_rps.iloc[0]
                df_rps = df_rps[1:]

                # Erstellen eines DataFrames mit den Fahrzeugdaten
                if 'vehicle_list' in st.session_state and st.session_state['vehicle_list']:
                    vehicle_data = {
                        "Fahrzeugtyp": [],
                        "Benzinverbrauch (l/100km)": [],
                        "Dieselverbrauch (l/100km)": [],
                        "Stromverbrauch (kWh/100km)": [],
                        "Kilometer leer": [],
                        "Kilometer besetzt": []
                    }
                    for vehicle in st.session_state['vehicle_list']:
                        if isinstance(vehicle, dict) and all(key in vehicle for key in ['Fahrzeugtyp', 'Kilometer leer', 'Kilometer besetzt']):
                            vehicle_data["Fahrzeugtyp"].append(vehicle['Fahrzeugtyp'])
                            vehicle_data["Benzinverbrauch (l/100km)"].append(vehicle['Benzinverbrauch (l/100km)'])
                            vehicle_data["Dieselverbrauch (l/100km)"].append(vehicle['Dieselverbrauch (l/100km)'])
                            vehicle_data["Stromverbrauch (kWh/100km)"].append(vehicle['Stromverbrauch (kWh/100km)'])
                            vehicle_data["Kilometer leer"].append(vehicle['Kilometer leer'])
                            vehicle_data["Kilometer besetzt"].append(vehicle['Kilometer besetzt'])

                    df_vehicles = pd.DataFrame(vehicle_data)
                else:
                    st.error("No vehicles in the session state or 'vehicle_list' is not set.")
                    df_vehicles = pd.DataFrame()

                # Erstellen eines DataFrames mit den Emissionsdaten der alternativ genutzten Verkehrsmittel, Modal Split, Emissions
                mode_to_key_umfrage_wege = {
                    "Verkehrsinduktion": "verkehrsinduktion",
                    "MIV (Fahrer)": "miv_fahrer",
                    "MIV (Mitfahrer)": "miv_mitfahrer",
                    "(Nahlinien-)Bus": "nahlinien_bus",
                    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
                    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
                    "Motorrad": "motorrad",
                    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
                    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
                    "zu Fuß": "zu_fuss",
                    "Sonstiges": "sonstiges"
                }

                data_av_umfrage_wege = {
                    "Merkmal": ["Wert"],
                    "Gesamtemissionen alternative Verkehrsmittel (kg CO2eq)": [st.session_state['gesamtemissionen_av_umfrage_wege']],
                    "Personenkilometer alternative Verkehrsmittel (km)": [st.session_state['personenkilometer_gesamt_av_umfrage_wege']],
                    "CO2-Emissionen pro Personenkilometer alternative Verkehrsmittel (g CO2eq/pkm)": [st.session_state['emissionen_pro_personenkilometer_av_umfrage_wege']]
                }

                # Hinzufügen der Modal Split Daten
                for verkehrsmittel, anteil in st.session_state['entries_umfrage_wege'].items():
                    key = mode_to_key_umfrage_wege.get(verkehrsmittel, verkehrsmittel)
                    data_av_umfrage_wege[f"Modal Split Anteil für {verkehrsmittel} (%)"] = [anteil]

                # Hinzufügen der Wegehäufigkeit, Durchschnittliche Fahrtdistanz, Personenkilometer und Emissionsdaten für alternative Verkehrsmittel
                for mode in st.session_state['entries_umfrage_wege']:
                    key = mode_to_key_umfrage_wege.get(mode, mode)
                    personenkilometer = st.session_state.get(f'personenkilometer_{key}', 0)
                    durchschnittliche_fahrtdistanz = st.session_state.get(f'entfernung_{key}', 0)
                    emissionsdaten = st.session_state.get(f'emission_{key}', 0)
                    data_av_umfrage_wege[f"Wegehäufigkeit für {mode} (Personenkilometer)"] = [personenkilometer]
                    data_av_umfrage_wege[f"Durchschnittliche Fahrtdistanz für {mode} (km)"] = [durchschnittliche_fahrtdistanz]
                    data_av_umfrage_wege[f"Emissionsdaten für {mode} (g CO2eq/pkm)"] = [emissionsdaten]

                df_av_umfrage_wege = pd.DataFrame(data_av_umfrage_wege).transpose()
                df_av_umfrage_wege.columns = df_av_umfrage_wege.iloc[0]
                df_av_umfrage_wege = df_av_umfrage_wege[1:]

                # Zusammenführen der DataFrames
                df_combined = pd.concat([df_rps, df_vehicles, df_av_umfrage_wege], axis=0)
                df_combined = df_combined.replace('', np.nan)
                st.write(df_combined)

                # Export als CSV-Datei
                csv = df_combined.to_csv(index=True)
                st.download_button(label="CSV-Datei herunterladen", data=csv, file_name='eingabedaten_und_ergebnisse_umfrage_wege.csv', mime='text/csv')

#########################################################################################
# Umfrage (Pkm)

#Sobald der Nutzer die Umfrage (Pkm) als Methodik ausgewählt hat, wird der Inhalt des Dashboards entsprechend angepasst.

mode_to_key_umfrage_pkm = {
    "Verkehrsinduktion": "verkehrsinduktion",
    "MIV (Fahrer)": "miv_fahrer",
    "MIV (Mitfahrer)": "miv_mitfahrer",
    "(Nahlinien-)Bus": "nahlinien_bus",
    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
    "Motorrad": "motorrad",
    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
    "Zu Fuß": "zu_fuss",
    "Sonstiges": "sonstiges"
}

if 'methodik' in st.session_state and st.session_state['methodik'] == "Umfrage (Pkm)":
    with st.expander("**6. Verkehrsmittelverteilung alternativer Verkehrsmittel**"):
        st.info("""**Hinweis:** Bitte geben Sie die Annahmen für die Verteilung der alternativen Verkehrsmittelverteilung der Fahrgäste an.
                    **Vorauswahl der Umfrage (Pkm):** Wählen Sie ein vordefiniertes Szenario aus, um die Standardwerte für die Verteilung automatisch auszufüllen. Diese Werte sind anpassbar.""")
        # Dropdown-Menü für Umfrage_pkm
        umfrage_pkm_options = {
            "Eigene Angaben": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Umfrage LOOPmünster (2021, 2022, 2022)": [0, 31, 9, 7, 0, 2, 0, 10, 24, 17, 0]
        }

        selected_modal_split_umfrage_pkm = st.selectbox("Vorauswahl Umfrage (Pkm) (Optional):", list(umfrage_pkm_options.keys()))

        # Speichern der globalen Variablen
        st.session_state['selected_modal_split_umfrage_pkm'] = selected_modal_split_umfrage_pkm

        # Anzeigen der Anteile basierend auf der ausgewählten Vorauswahl
        default_values_umfrage_pkm = umfrage_pkm_options[selected_modal_split_umfrage_pkm]

        # Eingabefelder für die Anteile
        transport_modes_umfrage_pkm = ["Verkehrsinduktion", "MIV (Fahrer)", "MIV (Mitfahrer)", "(Nahlinien-)Bus", "Straßen-/Stadt-/U-Bahn", "Schienen(nah)verkehr/Bahn/Zug", "Motorrad", "E-Bike/Pedelec/E-Lastenrad", "Fahrrad/Lastenrad", "Zu Fuß", "Sonstiges"]
        entries_umfrage_pkm = {}
        for i, mode_umfrage_pkm in enumerate(transport_modes_umfrage_pkm):
            entries_umfrage_pkm[mode_umfrage_pkm] = st.number_input(f"Anteil der Fahrgäste, die {mode_umfrage_pkm} genutzt hätten (%):",
                                            min_value=0.0, max_value=100.0,
                                            value=float(default_values_umfrage_pkm[i]), step=0.1, format="%f")
            
        # Überprüfung der Gesamtsumme der eingegebenen Werte
        total_percentage = sum(entries_umfrage_pkm.values())

        if total_percentage > 100:
            st.error("Die Summe der Modal-Split-Anteile überschreitet 100%.")
        elif total_percentage < 100:
            st.warning("Die Summe der Modal-Split-Anteile liegt unter 100%.")

        # Außerhalb des Expanders
        st.subheader("Berechnung der Personenkilometer der alternativen Verkehrsmittel")

        st.info("Die folgenden Daten beziehen sich auf die transportierten Fahrgäste des Ridepooling-Systems.")

        # Speichern der globalen Variablen
        st.session_state['entries_umfrage_pkm'] = entries_umfrage_pkm

        if 'personenkilometer_gefahren' in st.session_state and 'entries_umfrage_pkm' in st.session_state:
            personenkilometer_gefahren = int(st.session_state['personenkilometer_gefahren'])
            st.write(f"Von den zurückgelegten **{int(st.session_state['personenkilometer_gefahren'])}** Personenkilometern des Ridepooling-Systems würden entsprechend viele auf folgende alternative Verkehrsmittel entfallen:")
            entries_umfrage_pkm = st.session_state['entries_umfrage_pkm']

            for verkehrsmittel, anteil_umfrage_pkm in entries_umfrage_pkm.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{verkehrsmittel}:**")
                with col2:
                    berechneter_wert = personenkilometer_gefahren * anteil_umfrage_pkm / 100
                    st.session_state[f'personenkilometer_{mode_to_key_umfrage_pkm[verkehrsmittel]}'] = berechneter_wert
                    st.write(f"**{berechneter_wert:.0f} Pkm**")

        else:
            st.warning("Bitte stellen Sie sicher, dass die Gesamtzahl der gefahrenen Personenkilometer und die Modal-Split-Annahmen festgelegt wurden.")

    ######## 6. Annahmen für die Emissonen alternativer Verkehrsmittel
        # Initialisierung der benötigten Variablen, falls nicht vorhanden
    if 'transportierte_fahrgaeste' not in st.session_state:
        st.session_state['transportierte_fahrgaeste'] = 0
    if 'entries_umfrage_pkm' not in st.session_state:
        st.session_state['entries_umfrage_pkm'] = {}

    mode_to_key_umfrage_pkm = {
        "Verkehrsinduktion": "verkehrsinduktion",
        "MIV (Fahrer)": "miv_fahrer",
        "MIV (Mitfahrer)": "miv_mitfahrer",
        "(Nahlinien-)Bus": "nahlinien_bus",
        "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
        "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
        "Motorrad": "motorrad",
        "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
        "Fahrrad/Lastenrad": "fahrrad_lastenrad",
        "Zu Fuß": "zu_fuss",
        "Sonstiges": "sonstiges"
    }


    with st.expander("**7. Emissionsdaten alternativer Verkehrsmittel (Nutzung [TTW] und Energie [WTT])**"):
        st.info("""**Hinweis:** Bitte geben Sie die CO2-Emissionsdaten für die alternativ genutzten Verkehrsmittel an. Sie können vorausgewählte Optionen wählen oder eigene Angaben tätigen.""")
        # Vorauswahl der Emissionsdaten
        vorauswahl_emissionsdaten_optionen_umfrage_pkm = ["Eigene Angaben", "Umweltbundesamt, Umweltfreundlich mobil! (2022)"]
        selected_vorauswahl_emissionsdaten_umfrage_pkm = st.selectbox("Vorauswahl der Emissionsdaten:", vorauswahl_emissionsdaten_optionen_umfrage_pkm)

        # Definieren der Standardemissionswerte basierend auf der Vorauswahl
        if selected_vorauswahl_emissionsdaten_umfrage_pkm == "Umweltbundesamt, Umweltfreundlich mobil! (2022)":
            emissionsdaten_defaults_umfrage_pkm = {
                "verkehrsinduktion": 0.0,
                "miv_fahrer": 152.86,
                "miv_mitfahrer": 152.86,
                "nahlinien_bus": 80.54,
                "strassen_stadt_u_bahn": 58.79,
                "schienen_nah_verkehr_bahn_zug": 58.79,
                "motorrad": 90.0,
                "e_bike_pedelec_e_lastenrad": 3.9,
                "fahrrad_lastenrad": 0.0,
                "zu_fuss": 0.0,
                "sonstiges": 0.0
            }
        else:
            emissionsdaten_defaults_umfrage_pkm = {key: 0 for key in mode_to_key_umfrage_pkm.values()}

        # Eingabefelder für die Emissionsdaten
        for mode in transport_modes_umfrage_pkm:
            key = mode_to_key_umfrage_pkm[mode]
            emission_umfrage_pkm = st.number_input(f"Annahmen Emissionsdaten {mode} [gCO2eq/pkm]:", min_value=0.0, value=float(emissionsdaten_defaults_umfrage_pkm.get(key, 0)))
            st.session_state[f'emission_{key}'] = emission_umfrage_pkm

        st.write("Die Emissionsdaten für die alternativ genutzten Verkehrsmittel betragen:")

        for mode in transport_modes_umfrage_pkm:
            key = mode_to_key_umfrage_pkm[mode]
            personenkilometer = st.session_state.get(f'personenkilometer_{key}', 0)
            emission_umfrage_pkm = st.session_state.get(f'emission_{key}', 0)
            emissionen_umfrage_pkm = round(personenkilometer * emission_umfrage_pkm / 1000, 2)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Emissionen für {mode}:**")
            with col2:
                st.write(f"**{emissionen_umfrage_pkm} kg CO2eq**")

        # Berechnung und Speicherung der Gesamtemissionen für alternative Verkehrsmittel
        gesamtemissionen_av_umfrage_pkm = round(sum(
            st.session_state.get(f'personenkilometer_{mode_to_key_umfrage_pkm[mode]}', 0) *
            st.session_state.get(f'emission_{mode_to_key_umfrage_pkm[mode]}', 0) / 1000
            for mode in transport_modes_umfrage_pkm if mode != "verkehrsinduktion"
        ), 2)

        st.session_state['gesamtemissionen_av_umfrage_pkm'] = gesamtemissionen_av_umfrage_pkm

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Gesamtemissionen für alternative Verkehrsmittel:**")
        with col2:
            st.write(f"**{gesamtemissionen_av_umfrage_pkm} kg CO2eq**")

        # Berechnen der Personenkilometer für alternative Verkehrsmittel
        personenkilometer_gefahren_umfrage_pkm = round(sum(
            st.session_state.get(f'personenkilometer_{mode_to_key_umfrage_pkm[mode]}', 0)
            for mode in transport_modes_umfrage_pkm if mode != "verkehrsinduktion"
        ), 2)

        # Berechne die PErsonenkilometer gesamt für alternative Verkehrsmittel


        st.session_state['personenkilometer_gefahren_umfrage_pkm'] = personenkilometer_gefahren_umfrage_pkm



    ######## 8. Berechnung der Umweltwirkung alternativer Verkehrsmittel
    with st.expander("**8. Berechnung der Umweltwirkung alternativer Verkehrsmittel**"):
        st.info("""**Hinweis:** Im Folgenden wird die Umweltwirkung der alternativ genutzten Verkehrsmittel anhand von Umfragedaten im Raum (Umfragedaten, Personenkilometer) dargestellt. In der Abbildung wird der spezifische CO2-Ausstoß pro alternativen Verkehrsmittel denen anderer Verkehrsmittel gegenübergestellt. Die Kategoerie 'Sonstiges' wird durch die UBA-Quelle ("umweltfreundlich mobil!", 2022) nicht berücksichtigt.""")
        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['gesamtemissionen_av_umfrage_pkm', 'personenkilometer_gefahren_umfrage_pkm']
        if all(key in st.session_state for key in required_keys):
            gesamtemissionen_av_umfrage_pkm = st.session_state['gesamtemissionen_av_umfrage_pkm']
            personenkilometer_gefahren_umfrage_pkm = st.session_state['personenkilometer_gefahren_umfrage_pkm']

            # Berechnung der Emissionen pro Personenkilometer
            emissionen_pro_personenkilometer_av_umfrage_pkm = gesamtemissionen_av_umfrage_pkm / personenkilometer_gefahren_umfrage_pkm if personenkilometer_gefahren_umfrage_pkm > 0 else 0

            # Speichere die berechneten Werte im Sitzungszustand
            st.session_state['emissionen_pro_personenkilometer_av_umfrage_pkm'] = emissionen_pro_personenkilometer_av_umfrage_pkm

            emissionen_data = {
                'Alternative Verkehrsmittel': emissionen_pro_personenkilometer_av_umfrage_pkm * 1000,
                'Pkw - MIV (Fahrer) & MIV (Mitfahrer)': 152.86,
                '(Nahlinien-)Bus': 80.54,
                'Straßen-/Stadt-/U-Bahn': 59.30,
                'Schienen(nah)verkehr/Bahn/Zug': 58.79,
                'Motorrad': 173.3,
                'E-Bike/Pedelec/E-Lastenrad': 3.9,
                'Fahrrad/Lastenrad': 0.0,
                'Zu Fuß': 0.0
            }

            # Diagramm erstellen
            fig = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig.update_layout(
                barmode='group',
                title='Gegenüberstellung der Emissionen pro Personenkilometer nach Verkehrsmittel - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
            with col2:
                st.write(f"**{gesamtemissionen_av_umfrage_pkm} kg CO2**")
            st.session_state['gesamtemissionen_av_umfrage_pkm'] = gesamtemissionen_av_umfrage_pkm

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av_umfrage_pkm:.3f} g CO2/pkm**")

            # SPEICHERN DER GLOBALEN VARIABLEN
            st.session_state['emissionen_pro_personenkilometer_av_umfrage_pkm'] = emissionen_pro_personenkilometer_av_umfrage_pkm

        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um die Umweltwirkung der alternativen Verkehrsmittel zu berechnen.")

    st.subheader("Vergleich der spezifischen CO2-Emissionen pro Personenkilometer für das Ridepooling-System und alternative Verkehrsmittel")


######## 9. Vergleich
    with st.expander("**9. Vergleich**"):
        st.info("""**Hinweis:** Im Folgenden wird der spezifische CO2-Ausstoß pro Personenkilometer des Ridepooling-Systems mit denen der alternativ genutzten Verkehrsmittel verglichen.""")

        'initialisierung der benötigten Variablen, falls nicht vorhanden'
        if 'co2_emissionen_pro_personenkilometer_rps_umfrage_pkm' not in st.session_state:
            st.session_state['co2_emissionen_pro_personenkilometer_rps_umfrage_pkm'] = 0.0
        if 'emissionen_pro_personenkilometer_av_umfrage_pkm' not in st.session_state:
            st.session_state['emissionen_pro_personenkilometer_av_umfrage_pkm'] = 0.0
        if 'co2_emissionen_gesamt_rps_umfrage_pkm' not in st.session_state:
            st.session_state['co2_emissionen_gesamt_rps_umfrage_pkm'] = 0.0
        if 'gesamtemissionen_av_umfrage_pkm' not in st.session_state:
            st.session_state['gesamtemissionen_av_umfrage_pkm'] = 0.0
        if 'start_date' not in st.session_state:
            st.session_state['start_date'] = ""
        if 'end_date' not in st.session_state:
            st.session_state['end_date'] = ""


        # Überprüfen, ob alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = ['emissionen_pro_personenkilometer_av_umfrage_pkm', 'co2_emissionen_pro_personenkilometer_rps', 'gesamtemissionen_av_umfrage_pkm', 'start_date', 'end_date']

        if all(key in st.session_state for key in required_keys):
            co2_emissionen_pro_personenkilometer_rps = st.session_state['co2_emissionen_pro_personenkilometer_rps']
            emissionen_pro_personenkilometer_av_umfrage_pkm = st.session_state['emissionen_pro_personenkilometer_av_umfrage_pkm']

            # Erstellung des Diagramms
            emissionen_data = {
                st.session_state['name_ridepooling_system']: co2_emissionen_pro_personenkilometer_rps * 1000,
                'Alternative Verkehrsmittel': emissionen_pro_personenkilometer_av_umfrage_pkm * 1000
            }

            fig5 = go.Figure()
            for verkehrsmittel, emissionen in emissionen_data.items():
                fig5.add_trace(go.Bar(name=verkehrsmittel, x=[verkehrsmittel], y=[emissionen], marker_line_color='rgb(0,0,0)', marker_line_width=1.5, opacity=0.7))
            fig5.update_layout(
                barmode='group',
                title='Gegenüberstellung der spezifischen CO2-Emissionen pro Personenkilometer - Well-to-Wheel (WTW)*',
                legend=dict(
                    orientation="v",  # vertikale Anordnung
                    y=0.6,  # Positionierung der Legende
                    x=1.02,  # Legende rechts vom Diagramm
                    xanchor='left',
                    yanchor='top'
                ),
                width=650,
                height=650,
                yaxis_title='Emissionen [g CO2/pkm]',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig5)

            #Get co2_emissionen_gesamt_rps, start_date, end_date, gesamtemissionen_av, und runde auf 2 Dezimalstellen
            co2_emissionen_gesamt_rps = round(st.session_state['co2_emissionen_gesamt_rps'], 2)
            gesamtemissionen_av_umfrage_pkm = st.session_state['gesamtemissionen_av_umfrage_pkm']
            start_date = st.session_state['start_date']
            end_date = st.session_state['end_date']

            # Erstellung eines Textfeldes, in welchem die spezifischen CO2-Emissionen pro Personenkilometer des Ridepooling-Systems und der alternativ genutzten Verkehrsmittel verglichen werden
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen des Ridepooling-Systems:**")
            with col2:
                st.write(f"**{co2_emissionen_gesamt_rps:.2f} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen des Ridepooling-Systems pro Personenkilometer:**")
            with col2:
                st.write(f"**{co2_emissionen_pro_personenkilometer_rps:.3f} kg CO2/pkm**")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Gesamte CO2-Emissionen der alternativen Verkehrsmittel:**")
            with col2:
                st.write(f"**{gesamtemissionen_av_umfrage_pkm} kg CO2**")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**CO2-Emissionen der alternativen Verkehrsmittel pro Personenkilometer:**")
            with col2:
                st.write(f"**{emissionen_pro_personenkilometer_av_umfrage_pkm:.3f} kg CO2/pkm**")
                         
            # Erstelle ein Textfeld, in welchem je nach Ausgang des Vergleichs eine entsprechende Meldung ausgegeben wird
            if emissionen_pro_personenkilometer_av_umfrage_pkm != 0:
                if co2_emissionen_pro_personenkilometer_rps < emissionen_pro_personenkilometer_av_umfrage_pkm:
                    percentage_difference = round((emissionen_pro_personenkilometer_av_umfrage_pkm - co2_emissionen_pro_personenkilometer_rps) / emissionen_pro_personenkilometer_av_umfrage_pkm * 100, 2)
                    total_difference = round((gesamtemissionen_av_umfrage_pkm - co2_emissionen_gesamt_rps), 2)
                    st.success(f"Das Ridepooling-System weist im Vergleich zu den alternativ genutzten Verkehrsmitteln eine geringere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % niedriger als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Einsparung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                elif co2_emissionen_pro_personenkilometer_rps > emissionen_pro_personenkilometer_av_umfrage_pkm:
                    percentage_difference = round((co2_emissionen_pro_personenkilometer_rps - emissionen_pro_personenkilometer_av_umfrage_pkm) / emissionen_pro_personenkilometer_av_umfrage_pkm * 100, 2)
                    total_difference = round((co2_emissionen_gesamt_rps - gesamtemissionen_av_umfrage_pkm), 2)
                    st.error(f"Das Ridepooling-System weist im Vergleich zu den den alternativ genutzten Verkehrsmitteln eine höhere spezifische CO2-Emission pro Personenkilometer auf. Die spezifische CO2-Emission pro Personenkilometer des Ridepooling-Systems ist um {percentage_difference} % höher als bei alternativ genutzten Verkehrsmitteln. Die Gesamtemissionen des Ridepoolings betragen {co2_emissionen_gesamt_rps} kg CO2, was im Betrachtungszeitraum ({start_date} bis {end_date}) zu einer Erhöhung von {total_difference} kg CO2 im Vergleich den alternativ genutzten Verkehrsmitteln entspricht.")
                else:
                    st.warning("Das Ridepooling-System und die alternativen Verkehrsmittel weisen die gleiche spezifische CO2-Emission pro Personenkilometer auf.")
        else:
            st.error("Bitte stellen Sie sicher, dass alle erforderlichen Daten vorhanden sind, um den Vergleich der spezifischen CO2-Emissionen pro Personenkilometer durchzuführen.")


    #####
    with st.expander("**10. Export der Eingabedaten und Ergebnisse**"):
        # Stellen Sie sicher, dass alle erforderlichen Werte vorhanden sind, bevor Sie fortfahren
        required_keys = [
            'name_ridepooling_system', 'start_date', 'end_date', 'abgeschlossene_buchungen',
            'transportierte_fahrgaeste', 'vehicle_list', 'fahrzeugkilometer_leer', 'fahrzeugkilometer_besetzt',
            'fahrzeugkilometer_gesamt', 'personenkilometer_gefahren', 'benzinverbrauch_gesamt', 'dieselverbrauch_gesamt', 'stromverbrauch_gesamt',
            'oekostrom_anteil', 'benzin_emissionsdaten', 'diesel_emissionsdaten', 'strom_emissionsdaten',
            'co2_emissionen_gesamt_rps', 'co2_emissionen_pro_personenkilometer_rps', 'personenkilometer_gefahren_umfrage_pkm',
            'gesamtemissionen_av_umfrage_pkm', 'emissionen_pro_personenkilometer_av_umfrage_pkm', 'entries_umfrage_pkm'
        ]
        missing_keys = [key for key in required_keys if key not in st.session_state]
        if missing_keys:
            st.error(f"Die folgenden Schlüssel fehlen: {', '.join(missing_keys)}")
        else:
            st.write("Die Eingabedaten und Ergebnisse können als CSV-Datei exportiert werden.")
            if st.button("Exportieren"):
                # Erstellen eines DataFrames mit den Eingabedaten und Ergebnissen des Ridepooling-Systems
                data_rps = {
                    "Merkmal": ["Wert"],
                    "Ridepooling-System": [st.session_state['name_ridepooling_system']],
                    "Betrachtungszeitraum (Start)": [f"{st.session_state['start_date']}"],
                    "Betrachtungszeitraum (Ende)": [f"{st.session_state['end_date']}"],
                    "Anzahl abgeschlossener Buchungen": [st.session_state['abgeschlossene_buchungen']],
                    "Transportierte Fahrgäste": [st.session_state['transportierte_fahrgaeste']],
                    "Flotte - Fahrzeugkilometer (leer)": [st.session_state['fahrzeugkilometer_leer']],
                    "Flotte - Fahrzeugkilometer (besetzt)": [st.session_state['fahrzeugkilometer_besetzt']],
                    "Flotte - Fahrzeugkilometer (gesamt)": [st.session_state['fahrzeugkilometer_gesamt']],
                    "Flotte - Personenkilometer (gefahren)": [st.session_state['personenkilometer_gefahren']],
                    "Flotte - Benzinverbrauch (gesamt)": [st.session_state['benzinverbrauch_gesamt']],
                    "Flotte - Dieselverbrauch (gesamt)": [st.session_state['dieselverbrauch_gesamt']],
                    "Flotte - Stromverbrauch (gesamt)": [st.session_state['stromverbrauch_gesamt']],
                    "Ökostromanteil (%)": [st.session_state['oekostrom_anteil']],
                    "CO2-Emissionsdaten (Benzin)": [st.session_state['benzin_emissionsdaten']],
                    "CO2-Emissionsdaten (Diesel)": [st.session_state['diesel_emissionsdaten']],
                    "CO2-Emissionsdaten (Strom)": [st.session_state['strom_emissionsdaten']],
                    "CO2-Emissionen (gesamt)": [st.session_state['co2_emissionen_gesamt_rps']],
                    "CO2-Emissionen pro Personenkilometer": [st.session_state['co2_emissionen_pro_personenkilometer_rps']]
                }

                df_rps = pd.DataFrame(data_rps).transpose()
                df_rps.columns = df_rps.iloc[0]
                df_rps = df_rps[1:]

                # Erstellen eines DataFrames mit den Fahrzeugdaten
                if 'vehicle_list' in st.session_state and st.session_state['vehicle_list']:
                    vehicle_data = {
                        "Fahrzeugtyp": [],
                        "Benzinverbrauch (l/100km)": [],
                        "Dieselverbrauch (l/100km)": [],
                        "Stromverbrauch (kWh/100km)": [],
                        "Kilometer leer": [],
                        "Kilometer besetzt": []
                    }
                    for vehicle in st.session_state['vehicle_list']:
                        if isinstance(vehicle, dict) and all(key in vehicle for key in ['Fahrzeugtyp', 'Kilometer leer', 'Kilometer besetzt']):
                            vehicle_data["Fahrzeugtyp"].append(vehicle['Fahrzeugtyp'])
                            vehicle_data["Benzinverbrauch (l/100km)"].append(vehicle['Benzinverbrauch (l/100km)'])
                            vehicle_data["Dieselverbrauch (l/100km)"].append(vehicle['Dieselverbrauch (l/100km)'])
                            vehicle_data["Stromverbrauch (kWh/100km)"].append(vehicle['Stromverbrauch (kWh/100km)'])
                            vehicle_data["Kilometer leer"].append(vehicle['Kilometer leer'])
                            vehicle_data["Kilometer besetzt"].append(vehicle['Kilometer besetzt'])

                    df_vehicles = pd.DataFrame(vehicle_data)
                else:
                    st.error("No vehicles in the session state or 'vehicle_list' is not set.")
                    df_vehicles = pd.DataFrame()

                # Erstellen eines DataFrames mit den Emissionsdaten der alternativ genutzten Verkehrsmittel, Modal Split, Emissions
                mode_to_key_umfrage_pkm = {
                    "Verkehrsinduktion": "verkehrsinduktion",
                    "MIV (Fahrer)": "miv_fahrer",
                    "MIV (Mitfahrer)": "miv_mitfahrer",
                    "(Nahlinien-)Bus": "nahlinien_bus",
                    "Straßen-/Stadt-/U-Bahn": "strassen_stadt_u_bahn",
                    "Schienen(nah)verkehr/Bahn/Zug": "schienen_nah_verkehr_bahn_zug",
                    "Motorrad": "motorrad",
                    "E-Bike/Pedelec/E-Lastenrad": "e_bike_pedelec_e_lastenrad",
                    "Fahrrad/Lastenrad": "fahrrad_lastenrad",
                    "Zu Fuß": "zu_fuss",
                    "Sonstiges": "sonstiges"
                }

                data_av_umfrage_pkm = {
                    "Merkmal": ["Wert"],
                    "Gesamtemissionen alternative Verkehrsmittel (kg CO2eq)": [st.session_state['gesamtemissionen_av_umfrage_pkm']],
                    "Personenkilometer alternative Verkehrsmittel (km)": [st.session_state['personenkilometer_gefahren_umfrage_pkm']],
                    "CO2-Emissionen pro Personenkilometer alternative Verkehrsmittel (g CO2eq/pkm)": [st.session_state['emissionen_pro_personenkilometer_av_umfrage_pkm']]
                }

                # Hinzufügen der Modal Split Daten
                for verkehrsmittel, anteil in st.session_state['entries_umfrage_pkm'].items():
                    key = mode_to_key_umfrage_pkm.get(verkehrsmittel, verkehrsmittel)
                    data_av_umfrage_pkm[f"Modal Split Anteil für {verkehrsmittel} (%)"] = [anteil]

                # Hinzufügen der Personenkilometer und Emissionsdaten für alternative Verkehrsmittel
                for mode in st.session_state['entries_umfrage_pkm']:
                    key = mode_to_key_umfrage_pkm.get(mode, mode)
                    personenkilometer = st.session_state.get(f'personenkilometer_{key}', 0)
                    emissionsdaten = st.session_state.get(f'emission_{key}', 0)
                    data_av_umfrage_pkm[f"Personenkilometer für {mode} (km)"] = [personenkilometer]
                    data_av_umfrage_pkm[f"Emissionsdaten für {mode} (g CO2eq/pkm)"] = [emissionsdaten]

                df_av_umfrage_pkm = pd.DataFrame(data_av_umfrage_pkm).transpose()
                df_av_umfrage_pkm.columns = df_av_umfrage_pkm.iloc[0]
                df_av_umfrage_pkm = df_av_umfrage_pkm[1:]

                # Zusammenführen der DataFrames
                df_combined = pd.concat([df_rps, df_vehicles, df_av_umfrage_pkm], axis=0)
                df_combined = df_combined.replace('', np.nan)
                st.write(df_combined)

                # Export als CSV-Datei
                csv = df_combined.to_csv(index=True)
                st.download_button(label="CSV-Datei herunterladen", data=csv, file_name='eingabedaten_und_ergebnisse_umfrage_pkm.csv', mime='text/csv')

        
# Footer
st.markdown("---")
st.write("***Entwurfsfassung***")
st.write("Dieses Programm wurde  im Projekt 'Bewertung der ökologischen Effekte von Ridepooling-Systemen anhand von vier Fallbeispielen in NRW' entwickelt und durch das Ministerium für Umwelt, Naturschutz, und Verkehr des Landes Nordrhein-Westfalens gefördert. © 2024 [FH Münster](https://www.fh-muenster.de/)")
st.write("Die Berechnungen basieren auf den Annahmen und Daten, die Sie in den verschiedenen Abschnitten des Programms eingegeben haben.")
st.write("Die Ergebnisse dienen nur zu Informationszwecken und sind nicht verbindlich.")
st.write("Für Fragen oder Anregungen wenden Sie sich bitte an [peter.bruder@fh-muenster.de](mailto:peter.bruder@fh-muenster.de).")
