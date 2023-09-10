# README - Script playlistDownloader (Python3)

## Prérequis

1. **Python 3** : le script a été codé avec python3, vous pouvez verifier s'il est installer avec la commande :
   
   ```bash
   python3 --version
   ```

2. **Bibliothèques Python**: Ce script utilise os, tkinter et pytube. Vous pouvez les installer avec `pip` (le gestionnaire de paquets Python) :

   ```bash
   pip install os tkinter pytube
   ```

   - `os`: Pour les opérations sur le système de fichiers.
   - `tkinter` : Pour l'interface homme machine.
   - `pytube`: Pour Interagir avec YouTube.

## Utilisation

1. Recuperez le script playlistDownloader.py.
2. Exécutez-le :
 
   ```bash
   python3 playlistDownloader.py
   ```
   
3. Suivez les instructions (normalement j'ai fait un truc assez simple d'utilisation).

## Disclaimer

### C'est lent ! Il se passe rien ! Le script a planté ?
1. La récuperation du nom des videos peux prendre un certain temps, normalement tout s'affiche dans le terminal dans lequel vous avez lancé de script, donc gardez le à l'oeil.
2. La fenêtre de selection de vidéo tkinter peux freeze pendant le téléchargement, ça ne veux pas dire que le script a planté (cf. 1.), je règlerais peut être le bug si j'y pense.

### Erreur 410 (Gone) de pytube

Lors de l'utilisation de la bibliothèque `pytube` pour télécharger des vidéos depuis YouTube, il est possible de rencontrer l'erreur HTTP 410 (Gone).

Si vous rencontrez aussi cette erreur, je l'ai resolue en utilisant les commandes :

```bash
python -m pip install git+https://github.com/Zeecka/pytube@fix_1060
python -m pip install --upgrade pytube
```

Si ça ne suffit pas pour vous, bon chance --'

## Question/Retour

hésitez pas à demandez des modifiactions ou même (si vous êtes chaud) à le modifier vous même, j'ai juste fait ce script parce que j'en trouvez pas qui fonctionne bien ou qui soit pas des scam donc have fun

## Licence

Ce projet est open source et distribué sous une licence copyleft, ce qui signifie que vous êtes libre de l'utiliser, le modifier et le distribuer selon vos besoins/envie.

---

© [Kedesiklem](https://github.com/kedesiklem)
