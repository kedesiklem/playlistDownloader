Bien sûr, voici le texte corrigé en ce qui concerne l'orthographe et la grammaire :

```markdown
# README - Script playlistDownloader (Python3)

## Prérequis

1. **Python 3** : Le script a été codé avec Python 3. Vous pouvez vérifier s'il est installé avec la commande :
   
   ```bash
   python3 --version
   ```

2. **Bibliothèques Python** : Ce script utilise os, tkinter et pytube. Vous pouvez les installer avec `pip` (le gestionnaire de paquets Python) :

   ```bash
   pip install os tkinter pytube
   ```

   - `os` : Pour les opérations sur le système de fichiers.
   - `tkinter` : Pour l'interface homme-machine.
   - `pytube` : Pour interagir avec YouTube.

## Utilisation

1. Récupérez le script playlistDownloader.py.
2. Exécutez-le :

   ```bash
   python3 playlistDownloader.py
   ```
   
3. Suivez les instructions (normalement, j'ai fait quelque chose de plutôt simple à utiliser).

## Disclaimer

### C'est lent ! Il ne se passe rien ! Le script a planté ?
1. La récupération du nom des vidéos peut prendre un certain temps, normalement tout s'affiche dans le terminal dans lequel vous avez lancé le script, donc gardez-le à l'œil.
2. La fenêtre de sélection de vidéo tkinter peut se figer pendant le téléchargement, cela ne signifie pas que le script a planté (cf. 1.), je règlerai peut-être le bug si j'y pense.

### Erreur 410 (Gone) de pytube

Lors de l'utilisation de la bibliothèque `pytube` pour télécharger des vidéos depuis YouTube, il est possible de rencontrer l'erreur HTTP 410 (Gone).

Si vous rencontrez également cette erreur, je l'ai résolue en utilisant les commandes :

```bash
python -m pip install git+https://github.com/Zeecka/pytube@fix_1060
python -m pip install --upgrade pytube
```

Si cela ne suffit pas pour vous, "bon chance" --'

## Question/Retour

N'hésitez pas à demander des modifications ou même (si vous êtes motivé) à le modifier vous-même. J'ai juste créé ce script parce que je n'en trouvais pas qui fonctionnent bien ou qui ne soient pas des scams, donc amusez-vous.

## Licence

Ce projet est open source et distribué sous une licence copyleft, ce qui signifie que vous êtes libre de l'utiliser, de le modifier et de le distribuer selon vos besoins/envies.
```
