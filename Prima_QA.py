import neal
import dimod  # <--- Importiamo dimod per costruire il BQM corretto

# 1. Definiamo un problema a 3 antenne (0, 1, 2) con valori in un range ampio
linear = {0: -1.0, 1: -1.0, 2: -1.0}

quadratic = {
    (0, 1): 1.0,  # Interferenza leggera tra 0 e 1
    (1, 2): 1.0,  # Interferenza pesantissima tra 1 e 2
    (0, 2): 1.0   # Nessuna interferenza tra 0 e 2
}

# 2. Creiamo il simulatore
sampler = neal.SimulatedAnnealingSampler()

# 3. Costruiamo il modello usando dimod.BQM
bqm = dimod.BQM(linear, quadratic, dimod.BINARY)

# 4. Inviamo il modello bqm al risolutore
response = sampler.sample(bqm, num_reads=100)

# 5. Usiamo .aggregate() per raggruppare i risultati identici
response_aggregata = response.aggregate()

print("--- PANORAMA ENERGETICO COMPLETO (Dal migliore al peggiore) ---")
for sample, energy, num_occurrences in response_aggregata.data(['sample', 'energy', 'num_occurrences']):
    # Convertiamo il dizionario in una lista comoda da leggere (es. [0, 1, 0])
    stato_antenne = [sample[0], sample[1], sample[2]]
    print(f"Stato Antenne: {stato_antenne} | Energia: {energy:6.1f} | Trovata {num_occurrences} volte su 100")