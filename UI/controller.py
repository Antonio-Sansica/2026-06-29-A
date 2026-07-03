import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def populate_dd_countries(self):
        self._view._ddCountry.options.clear()
        dati = self._model.getCountries()
        for dato in dati:
            self._view._ddCountry.options.append(ft.dropdown.Option(str(dato)))


    def handleCreaGrafo(self, e):
        valore_str = self._view._ddCountry.value

        if valore_str is None:
            self._view.create_alert("Attenzione: seleziona una nazione")
            return

        # 2. CHIAMATA AL MODEL
        self._model.build_graph(valore_str)

        # 3. PULIZIA SCHERMO E VERIFICA
        self._view._txt_result.controls.clear()

        if self._model.grafo.number_of_nodes() == 0:
            self._view._txt_result.controls.append(ft.Text("Nessun grafo creato con questi parametri."))
            self._view.update_page()
            return

        # 4. STAMPA DELLE RISPOSTE STANDARD
        nodi, archi = self._model.get_dettagli_grafo()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con successo!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))

        # 5. RIEMPIMENTO DELLA TENDINA NODI (TRUCCO LAMBDA E KEY)
        self._view._ddClienti.options.clear()
        nodi_ordinati = list(self._model.grafo.nodes())
        nodi_ordinati.sort(key=lambda x: x.LastName)

        for nodo in nodi_ordinati:
            self._view._ddClienti.options.append(
                ft.dropdown.Option(
                    key=str(nodo.CustomerId),
                    text=nodo.LastName
                )
            )

        self._view.update_page()

    def handleStampaInfo(self,e):

        nodo_influente, score_influenza = self._model.get_nodo_piu_influente()
        if nodo_influente is not None:
            self._view._txt_result.controls.append(
                ft.Text(f"Nodo più influente: {nodo_influente.LastName} (Score: {score_influenza})"))

        self._view._txt_result.controls.append(ft.Text("Archi di peso maggiore:", color="red"))
        top_archi = self._model.get_top_archi_peso(5)
        for u, v, dati in top_archi:
            self._view._txt_result.controls.append(ft.Text(f"{u.LastName} -> {v.LastName} ({dati['weight']})"))

        self._view.update_page()

    def handleSequenza(self,e):
        id_nodo_selezionato = self._view._ddClienti.value

        if id_nodo_selezionato is None:
            self._view.create_alert("Seleziona prima un cliente sulla tendina!")
            return

        id_nodo = int(id_nodo_selezionato)
        nodo = self._model.mappa_nodi[id_nodo]

        self._view._txt_result.controls.clear()

        # ---> OPZIONE E: Percorso con vincolo sulle proprietà dei Nodi (Es. Età decrescente)
        # === Scommenta quando la regola di avanzamento dipende dai dati dell'oggetto nodo ===
        percorso_nodi, lunghezza_max = self._model.calcola_percorso_lungo_con_vincolo_nodi(nodo)
        self._view._txt_result.controls.append(ft.Text(f"Trovato percorso lungo {lunghezza_max} clienti:"))

        for nodo in percorso_nodi:
            self._view._txt_result.controls.append(ft.Text(f"-> {nodo.LastName} (Fatturato totale: {nodo.Fatturato})"))

        self._view.update_page()
