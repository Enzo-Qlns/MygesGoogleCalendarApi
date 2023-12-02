from datetime import datetime, timedelta
import base64

class utils:
    def __init__(self) -> None:
        pass

    def get_unix_timestamps_for_week(self):
        # Obtenez la date actuelle
        current_date = datetime.now()

        # Calculez le jour de la semaine (0 pour lundi, 6 pour dimanche)
        current_weekday = current_date.weekday()

        # Calculez la différence de jours pour obtenir le lundi de la semaine en cours
        days_until_monday = current_weekday if current_weekday == 0 else (8 - current_weekday)

        # Calculez la date du lundi de la semaine en cours
        monday_date = current_date - timedelta(days=days_until_monday)

        # Calculez la date du dimanche de la semaine en cours
        sunday_date = monday_date + timedelta(days=6)

        # Convertissez les dates en timestamp Unix
        monday_unix_timestamp = int(monday_date.timestamp())
        sunday_unix_timestamp = int(sunday_date.timestamp())

        return monday_unix_timestamp, sunday_unix_timestamp
    
    def get_today_and_one_year_later_timestamp_format(self):
        # Obtenez la date actuelle
        current_date = datetime.utcnow()

        # Ajoutez un an à la date actuelle
        one_year_later = current_date + timedelta(days=365)

        # Convertissez les dates en timestamp Unix
        today_timestamp = int(current_date.timestamp())
        one_year_later_timestamp = int(one_year_later.timestamp())

        return today_timestamp, one_year_later_timestamp
    
    def convert_unix_timestamp_to_iso(self, timestamp):
        # Convertissez le timestamp Unix en objet datetime
        date_object = datetime.utcfromtimestamp(timestamp)

        # Ajoutez le nombre d'heures spécifié à la date
        date_object_with_hour_addition = date_object + timedelta(hours=1)

        # Formattez la date en chaîne de caractères au format ISO
        formatted_date = date_object_with_hour_addition.strftime('%Y-%m-%dT%H:%M:%S')

        return formatted_date
    
    def decode_google_event_eid(self, htmlLink):
        return base64.b64decode(htmlLink.split('eid')[1]).decode('ascii').split(' ')[0]