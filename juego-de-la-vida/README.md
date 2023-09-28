# JUEGO DE LA VIDA

### Consigna del TP 2

#### Como utilizar:

```bash
python game.py
```

#### Opciones:

* Es posible indicarle una "dificultad" con la opcion --options. Indicara entre cuantas opciones estaremos realizando una eleccion de ARNt

Ejemplo.
```bash
python game.py --options 3 # Tendremos 4 opciones a elegir, 1 valida y 3 incorrectas
```

* Es posible utilizar un archivo FASTA con una proteina inicial con la opcion --file y utilizar alguna secuencia dada.

Ejemplo.
```bash
python game.py --file cytochromec.fasta --options 4
```

De no pasarle un file, se utilizara un .fasta de ejemplo, llamado `example.fasta`