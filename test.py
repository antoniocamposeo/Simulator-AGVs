import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation


def animations(opt,file_name:str):
    matrice = opt.state_position
    # Assegniamo un colore diverso ad ogni AGV
    colors = ['red', 'blue', 'green', 'yellow', 'black']
    # Parametri del grafico
    fig, ax = plt.subplots()
    scat = ax.scatter([], [], s=120)

    # Limiti degli assi
    ax.set_xlim(-10, 40)
    ax.set_ylim(-10, 40)
    ax.set_title("Movimento dinamico degli AGV")

    ax.grid(True)
    reachable_positions = [
        (10, 10),
        (20, 10),
        (10, 20),
        (20, 20),
        (30, 20),
        (20, 30)]

    # Disegniamo le posizioni raggiungibili (griglia)
    reachable_x, reachable_y = zip(*reachable_positions)
    ax.scatter(reachable_x, reachable_y, c='gray', alpha=0.3, label='Posizioni raggiungibili')

    def avoid_overlap(positions):
        """ Evita la sovrapposizione di AGV spostando leggermente quelli nella stessa posizione. """
        new_positions = []
        shift_amount = 0.1  # Quanto spostare in caso di sovrapposizione
        seen_positions = {}

        for pos in positions:
            if pos in seen_positions:
                seen_positions[pos] += 1
                new_pos = (pos[0] + shift_amount * seen_positions[pos], pos[1])
                new_positions.append(new_pos)
            else:
                seen_positions[pos] = 0
                new_positions.append(pos)

        return new_positions

    def update(frame):
        # Otteniamo le posizioni per l'istante attuale
        positions = matrice[frame]
        # Evitiamo la sovrapposizione
        positions = avoid_overlap(positions)

        # Aggiorniamo le posizioni degli AGV nel grafico
        scat.set_offsets(positions)
        # Assegniamo i colori corrispondenti agli AGV
        scat.set_color(colors)
        return scat,

    # Creiamo l'animazione
    ani = FuncAnimation(fig, update, frames=len(matrice), blit=True, interval=1, repeat=True)
    # Salvataggio dell'animazione come GIF
    ani.save(file_name+'.gif', writer='pillow', fps=10)


def plotting(arr, speed_arr):
    # Genera dati di esempio (puoi sostituire questi con i tuoi array)
    x = np.arange(1,len(arr[0])+1)

    # Lista dei 5 array da plottare
    y_arrays = arr
    labels = []
    for i in range(len(speed_arr)):
        labels.append('Speed:' + str(speed_arr[i]))

    colors = plt.cm.viridis(np.linspace(0, 1, len(y_arrays)))  # Genera colori diversi per ogni array

    # Crea la figura con sfondo nero
    plt.figure(figsize=(10, 6), facecolor='black')

    # Plot ogni array con un colore unico
    for i, y in enumerate(y_arrays):
        plt.plot(x, y, color=colors[i], linewidth=3, label=labels[i])

    # Personalizza l'aspetto del plot
    plt.title("Comparison of Makespan - Variation of Speed - N°Machine = 3 ", color="white", fontsize=18)
    plt.xlabel("N°AGVs", color="white", fontsize=12)
    plt.ylabel("Makespan", color="white", fontsize=12)
    plt.grid(True, linestyle='--', color='gray')
    plt.gca().set_facecolor('black')  # Imposta lo sfondo del grafico su nero

    # Colora i ticks per abbinarsi allo sfondo nero
    plt.tick_params(colors='white')

    # Aggiungi la legenda per ogni array
    plt.legend(loc='upper right', fontsize=12, facecolor='black', edgecolor='white', labelcolor='white')

    # Mostra il grafico
    plt.show()


def plotting1(arr, speed_arr):
    # Genera dati di esempio (puoi sostituire questi con i tuoi array)
    x = np.linspace(0, len(arr[0]), len(arr[0]))

    # Lista dei 5 array da plottare
    y_arrays = arr
    labels = []
    for i in range(len(speed_arr)):
        labels.append('Speed:' + str(speed_arr[i]))

    # Crea un oggetto Figura per il grafico interattivo
    fig = go.Figure()

    # Aggiungi ciascuno degli array come traccia separata con una legenda
    fig.add_trace(go.Scatter(x=x, y=y_arrays[0], mode='lines', name=labels[0], line=dict(color='royalblue', width=2)))
    fig.add_trace(go.Scatter(x=x, y=y_arrays[1], mode='lines', name=labels[1], line=dict(color='firebrick', width=2)))
    fig.add_trace(go.Scatter(x=x, y=y_arrays[2], mode='lines', name=labels[2], line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=x, y=y_arrays[3], mode='lines', name=labels[3], line=dict(color='purple', width=2)))
    fig.add_trace(go.Scatter(x=x, y=y_arrays[4], mode='lines', name=labels[4], line=dict(color='orange', width=2)))

    # Personalizza il layout per rendere il grafico bello
    fig.update_layout(
        title="Dynamic Comparison of 5 Arrays",
        xaxis_title="X-axis",
        yaxis_title="Y-axis",
        template="plotly_dark",  # Tema scuro
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=0, r=0, t=40, b=40)
    )

    # Mostra il grafico interattivo
    fig.show()

    # Salva come file HTML
    fig.write_html("dynamic_plot.html")


def plotting2(arr):
    """
    :param arr: single array
    :return: Plot a single array
    """
    # Generate example data (you can replace this with your array)
    x = np.linspace(0, len(arr), len(arr))
    y = arr  # Example function, replace this with your array

    # Create a gradient color array based on y-values
    colors = plt.cm.viridis((y - y.min()) / (y.max() - y.min()))  # Viridis color map

    # Plot the array with a cool gradient style
    plt.figure(figsize=(10, 6), facecolor='black')  # Black background
    for i in range(1, len(x) - 1):
        plt.plot(x[i:i + 2], y[i:i + 2], color=colors[i], linewidth=3)

    # Customize the plot appearance
    plt.title("Time Makespan Plot", color="white", fontsize=18)
    plt.xlabel("N°AGVs", color="white", fontsize=12)
    plt.ylabel("Makespan", color="white", fontsize=12)
    plt.grid(True, linestyle='--', color='gray')
    plt.gca().set_facecolor('black')  # Set plot background to black

    # Invert ticks color to match the black background
    plt.tick_params(colors='white')

    plt.show()
