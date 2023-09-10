# README - Script playlistDownloader (Python3)

## Prérequis

1. **Python 3** : le script a été codé avec python3, vous pouvez verifier s'il est installer avec la commande :
   
   ```bash
   python3 --version
   ```

2. **Bibliothèques Python**: Ce script utilise os, tkinter et pytube. Vous pouvez les installer en utilisant `pip` (le gestionnaire de paquets Python). Exécutez les commandes suivantes pour installer les dépendances requises :

   ```bash
   pip install os tkinter pytube
   ```

   - `os`: Pour les opérations sur le système de fichiers.
   - `tkinter` : Pour l'interface homme machine.
   - `pytube`: Pour Interagir avec YouTube.

## Utilisation

1. Recuperez le script python playlistDownloader.py.
2. Exécutez le script Python :
 
   ```bash
   python3 playlistDownloader.py
   ```
   
4. Suivez les instructions du script.

## Erreur 410 (Gone) de pytube

Lors de l'utilisation de la bibliothèque `pytube` pour télécharger des vidéos depuis YouTube, il est possible de rencontrer l'erreur HTTP 410 (Gone).

Si vous rencontrez aussi cette erreur, je l'ai resolue en utilisant les commandes :

```bash
python -m pip install git+https://github.com/Zeecka/pytube@fix_1060
python -m pip install --upgrade pytube
```

Si ça ne suffit pas pour vous, bon chance --'

---

© [Kedesiklem](https://github.com/kedesiklem)
