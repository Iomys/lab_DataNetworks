# lab_DataNetworks
Laboratoire de Systèmes d'Information (SIn) de 3ème année en énergie et techniques environnementales

## Environement virtuel
En Python, on travaille souvent dans des environnements virtuels, 
ils permettent de travailler avec les mêmes versions des paquets, quels que soit la machine utilisée
et les versions installée "de base"

Dans ce projet, nous développons sur notre laptop, puis excécutons les programmes sur le raspberry-pi. L'intérêt d'un
environnement virtuel est totalement justifié.

Pour que le programme fonctionne correctement, il est nécessaire d'installer les librairies de `requirements.txt`

### Installation de virtualenv 
```bash
pip3 install virtualenv
```

### Création de l'environnement virtuel
Exécuter les commandes dans le dossier du répertoire

```bash
virtualenv -p python3 venv # création d'un environnement virtuel avec python3
source venv/bin/activate # activation de l'environnement virtuel
pip install -r requirements.txt # installation des paquets requis
```

### Désactiver l'environnement virtuel
```bash
deactivate 
```

### Activer l'environnement virtuel
```bash
source venv/bin/activate
```

## Fichier de configuration

Il est nécessaire de remplir le fichier de configuration [crendentials.toml](https://github.com/Iomys/lab_DataNetworks/blob/main/credentials.toml) avec les données du broker mqtt, de la mystrom switch et du server influxdb.

## Fonctionnement des scripts en arrière plan
Afin que les scripts fonctionnent en arrière-plan sur la raspberry-pi, nous allons créer un *service* avec systemd.

### Plug to MQTT

#### 1. Créer les fichiers de service pour les deux programmes

```bash
sudo nano /etc/systemd/system/plug_2_mqtt.service
```
#### 2. Coller la configuration en veillant à ce que le chemin du répertoire (ici `/home/pi/lab_DataNetworks`) soit le bon
```ini
[Unit]
Description=Plug to MQTT
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/home/pi/lab_DataNetworks/venv/bin/python /home/pi/lab_DataNetworks/plug_2_mqtt.py

[Install]
WantedBy=multi-user.target
```
#### 3. Activer le service
```bash
sudo systemctl daemon-reload # Recharge les fichiers de configuration
sudo systemctl enable plug_2_mqtt.service # Activer le service
sudo systemctl start plug_2_mqtt.service  # Démarrer le service (pour la première fois, ensuite il sera automatiquement activé)
```

Il est possible de vérifier le status du service en entrant `sudo systemtl status plug_2_mqtt.service`

### MQTT to influx
#### 1. Créer les fichiers de service pour les deux programmes

```bash
sudo nano /etc/systemd/system/mqtt_2_influx.service
```
#### 2. Coller la configuration en veillant à ce que le chemin du répertoire (ici `/home/pi/lab_DataNetworks`) soit le bon
```ini
[Unit]
Description=MQTT to influxdb
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/home/pi/lab_DataNetworks/venv/bin/python /home/pi/lab_DataNetworks/mqtt_2_influx.py

[Install]
WantedBy=multi-user.target
```
#### 3. Activer le service
```bash
sudo systemctl daemon-reload # Recharge les fichiers de configuration
sudo systemctl enable mqtt_2_influx.service # Activer le service
sudo systemctl start mqtt_2_influx.service  # Démarrer le service (pour la première fois, ensuite il sera automatiquement activé)
```

Il est possible de vérifier le status du service en entrant `sudo systemtl status mqtt_2_influx.service`

## Serveur Flask
Le serveur Flask est encore en développement
