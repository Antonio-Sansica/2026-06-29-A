import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.grafo = nx.DiGraph()

    def getCountries(self):
        return DAO.getAllCountries()

    def popola_mappa_nodi(self, country):
        self.mappa_nodi.clear()
        lista_nodi = DAO.getAllNodi(country)
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.CustomerId] = nodo


    def build_graph(self, country):
        self.grafo.clear()
        self.popola_mappa_nodi(country)

        # PASSO 2: Aggiunta Nodi (Scegli opzione Standard o Union dal DAO)
        self.grafo.add_nodes_from(self.mappa_nodi.values())

        # PASSO 3: Archi (Scegli Semplici o Ninja/Pesati dal DAO)
        archi_grezzi = DAO.getAllArchi(country, country)


        for id_1, id_2 in archi_grezzi:
            if id_1 in self.mappa_nodi and id_2 in self.mappa_nodi:
                n1 = self.mappa_nodi[id_1]
                n2 = self.mappa_nodi[id_2]

                # 1. Calcolo il peso richiesto dalla traccia (es. somma delle popolarità)
                peso_arco = n1.Fatturato + n2.Fatturato

                # 2. Decido i versi in base alla condizione della traccia
                if n1.Fatturato > n2.Fatturato:
                    self.grafo.add_edge(n1, n2, weight=peso_arco)

                elif n2.Fatturato > n1.Fatturato:
                    self.grafo.add_edge(n2, n1, weight=peso_arco)

                else:
                    self.grafo.add_edge(n1, n2, weight=peso_arco)
                    self.grafo.add_edge(n2, n1, weight=peso_arco)

    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def get_nodo_piu_influente(self):
        if self.grafo.number_of_nodes() == 0:
            return None, 0

        max_influenza = -float('inf')
        miglior_nodo = None

        for nodo in self.grafo.nodes():

            # TRUCCO NETWORKX: in_degree(weight='weight') calcola in automatico
            # la SOMMA DEI PESI di tutti gli archi che ENTRANO in questo nodo.
            peso_entrante = self.grafo.in_degree(nodo, weight='weight')

            # out_degree calcola la SOMMA DEI PESI di tutti gli archi che ESCONO.
            peso_uscente = self.grafo.out_degree(nodo, weight='weight')

            # 4. Applico la formula della traccia (Influenza = Uscenti - Entranti)
            influenza = peso_uscente - peso_entrante

            # 5. Se trovo un nuovo record, lo salvo
            if influenza > max_influenza:
                max_influenza = influenza
                miglior_nodo = nodo

        # 6. Restituisco l'oggetto nodo vincente e il suo punteggio
        return miglior_nodo, max_influenza

    def get_top_archi_peso(self, n):
        # 1. Estraggo tutti gli archi e li trasformo in lista
        lista_archi = list(self.grafo.edges(data=True))

        # 2. Li ordino in base al valore 'weight' dentro il dizionario 'data', al contrario (decrescente)
        lista_archi.sort(key=lambda edge: edge[2]['weight'], reverse=True)

        # 3. Restituisco i primi N elementi
        return lista_archi[:n]

    def calcola_percorso_lungo_con_vincolo_nodi(self, nodo_partenza):
        self._soluzione_ottima = []
        self._punteggio_ottimo = 0

        # Il percorso inizia con il nodo di partenza
        parziale = [nodo_partenza]

        self._ricorsione_cammino_vincolo_nodi(parziale)

        return self._soluzione_ottima, self._punteggio_ottimo

    def _ricorsione_cammino_vincolo_nodi(self, parziale):
        # 1. VALUTAZIONE: Stiamo cercando il percorso più LUNGO
        if len(parziale) > self._punteggio_ottimo:
            self._punteggio_ottimo = len(parziale)
            self._soluzione_ottima = copy.deepcopy(parziale)

        # 2. ESPLORAZIONE
        ultimo_nodo = parziale[-1]

        # Uso .neighbors() per i grafi non orientati (come richiesto in questo esame)
        for vicino in self.grafo.successors(ultimo_nodo):

            # VINCOLO A (La traccia chiede "Cammino Semplice"): Non ripassare sui nodi
            if vicino not in parziale:

                # VINCOLO B (Speciale): "Età strettamente decrescente"
                # Confronto l'attributo .eta (che devi aver messo nel DTO) del vicino
                # con l'attributo .eta del nodo in cui mi trovo ora.

                # Sostituisci '.eta' con l'attributo reale del tuo DTO all'esame!
                if vicino.Fatturato < ultimo_nodo.Fatturato:
                    # 3. AZIONE E BACKTRACKING
                    parziale.append(vicino)
                    self._ricorsione_cammino_vincolo_nodi(parziale)
                    parziale.pop()
